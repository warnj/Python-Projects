import os
from os import walk

# SOURCE_PATH = 'C:/Users/warnj/Downloads/'
SOURCE_PATH = 'D:/OneDrive/Documents/Money/Pay/'

def renameDiscover(filename):
    if filename.endswith('.pdf') and filename.startswith('Discover-Statement'):
        print(filename)
        year = filename[19:23]
        month = filename[23:25]
        print('year', year)
        print('month', month)
        newName = year+'_'+month+'_Discover.pdf'
        os.rename(SOURCE_PATH+filename, SOURCE_PATH+newName)

def renameChase(filename):
    if filename.endswith('.pdf') and filename.startswith('20') and 'statements' in filename:
        print(filename)
        year = filename[0:4]
        month = filename[4:6]
        print('year', year)
        print('month', month)
        newName = year+'_'+month+'_Chase.pdf'
        os.rename(SOURCE_PATH+filename, SOURCE_PATH+newName)

def renamePayslipOld(filename):
    if filename.endswith('.pdf') and filename.startswith('2'):
        print(filename)
        year = filename[0:4]
        month = filename[5:7]
        day = filename[8:10]
        # print('year', year)
        # print('month', month)
        # print('day', day)
        if 'bonus' in filename:
            newName = 'SFDC_Payslip_' + year + '_' + month + '_' + day + '_bonus.pdf'
        else:
            newName = 'SFDC_Payslip_' + year+'_'+month+'_'+day+'.pdf'
        print('new name', newName)
        os.rename(SOURCE_PATH+filename, SOURCE_PATH+newName)

def renameSalesforcePayslip(filename):
    if filename.endswith('.pdf') and filename[0:4] == "SFDC" and filename[13] != '2':
        print(filename)
        year = filename[19:23]
        month = filename[13:15]
        day = filename[16:18]
        suffix = filename[23:-4]
        # print('year', year)
        # print('month', month)
        # print('day', day)
        # print('suffix', suffix)
        if suffix:
            newName = 'SFDC_Payslip_' + year + '_' + month + '_' + day + '_' + suffix + '.pdf'
        else:
            newName = 'SFDC_Payslip_' + year+'_'+month+'_'+day+'.pdf'
        print('new name', newName)
        os.rename(SOURCE_PATH+filename, SOURCE_PATH+newName)

months = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12',
}
def renameADPPayslip(filename):
    if filename.endswith('.pdf') and filename.startswith('Statement for'):
        print(filename)
        year = filename[-8:-4]
        month = filename[14:17]
        day = filename[18:-10]
        print('year "{}"'.format(year))
        print('month "{}"'.format(month))
        print('day "{}"'.format(day))
        if len(day) == 1: day = '0'+day
        month = months[month]
        newName = 'Cruise_Payslip_' + year+'_'+month+'_'+day+'.pdf'
        print('new name', newName)
        os.rename(SOURCE_PATH+filename, SOURCE_PATH+newName)

_, _, filenames = next(walk(SOURCE_PATH))
for filename in filenames:
    renameADPPayslip(filename)
