from quantopian.algorithm import attach_pipeline, pipeline_output, order_optimal_portfolio
from quantopian.pipeline import Pipeline
from quantopian.pipeline.factors import CustomFactor, SimpleMovingAverage, AverageDollarVolume, RollingLinearRegressionOfReturns
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.data import morningstar
from quantopian.pipeline.filters.morningstar import IsPrimaryShare
from quantopian.pipeline.classifiers.morningstar import Sector
import numpy as np
import pandas as pd 
from quantopian.pipeline.filters import Q1500US
import quantopian.experimental.optimize as opt

MAX_GROSS_LEVERAGE = 1.0
NUM_LONG_POSITIONS = 300
NUM_SHORT_POSITIONS = 300
MAX_SHORT_POSITION_SIZE = 2*1.0/(NUM_LONG_POSITIONS + NUM_SHORT_POSITIONS)
MAX_LONG_POSITION_SIZE = 2*1.0/(NUM_LONG_POSITIONS + NUM_SHORT_POSITIONS)
MAX_SECTOR_EXPOSURE = 0.10 
MAX_BETA_EXPOSURE = 0.20

class Reversion(CustomFactor):
   inputs =[USEquityPricing.close]
   window_length = 60

def compute(self, today, assets, out, prices):
   out[:] = -prices[-1] / np.mean(prices, axis=0)

def make_pipeline():
   reversion = Reversion()
   sector = Sector()
   universe = Q1500US()
   factor_rank = reversion.rank(mask=universe).zscore()

longs = factor_rank.top(NUM_LONG_POSITIONS)
shorts = factor_rank.bottom(NUM_SHORT_POSITIONS)

long_short_screen = (longs | shorts)

beta = 0.66 * RollingLinearRegressionOfReturns(
   target=sid(8554),
   returns_length=5,
   regression_length=260,
   mask=long_short_screen
).beta + 0.33*1.0

pipe = Pipeline(
   columns={
      'longs': longs,
      'shorts': shorts,
        'factor_rank': factor_rank,
        'reversion': reversion,
      'sector': sector,
      'market_beta': beta
   },
   screen=long_short_screen
)
return pipe

def initialize(context):
   set_commission(commission.PerShare(cost=0.0, min_trade_cost=0))
   set_slippage(slippage.VolumeShareSlippage(volume_limit=1, price_impact=0))
   context.spy = sid(8554)

attach_pipeline(make_pipeline(), 'long_short_equity_template')

schedule_function(func=rebalance,
      date_rule=date_rules.month_start(),
      time_rule=time_rules.market_open(hours=0, minutes=30),
      half_days=True)
schedule_function(func=recording_statements,
      date_rule=date_rules.every_day(),
      time_rule=time_rules.market_close(),
      half_days=True)
def before_trading_start(context, data):
   context.pipeline_data = pipeline_output('long_short_equity_template')


def recording_statements(context, data):
   record(num_positions=len(context.portfolio.positions))

def rebalance(context, data):
   pipeline_data = context.pipeline_data
   todays_universe = pipeline_data.index

risk_factor_exposures = pd.DataFrame(
   {
      'market_beta':pipeline_data.market_beta.fillna(1.0)
   }
)

objective = opt.MaximizeAlpha(pipeline_data.factor_rank)

constraints = []
constraints.append(opt.MaxGrossLeverage(MAX_GROSS_LEVERAGE))
constraints.append(opt.DollarNeutral())
constraints.append(
      opt.NetPartitionExposure.with_equal_bounds(
      labels=pipeline_data.sector,
      min=-MAX_SECTOR_EXPOSURE,
      max=MAX_SECTOR_EXPOSURE,
   )
)
neutralize_risk_factors = opt.WeightedExposure(
   loadings=risk_factor_exposures,
   min_exposures={'market_be-MAX_BETA_EXPOSURE},
   max_exposures={'market_beMAX_BETA_EXPOSURE}
)
constraints.append(neutralize_risk_factors)
constraints.append(
   opt.PositionConcentration.with_equal_bounds(
      min=-MAX_SHORT_POSITION_SIZE,      max=MAX_LONG_POSITION_SIZE
   )
)

order_optimal_portfolio(
   objective=objective,
   constraints=constraints,
   universe=todays_universe
)