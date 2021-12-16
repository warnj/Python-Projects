import os
from os import walk

# SOURCE_PATH = 'C:/Users/warnj/Downloads/'
SOURCE_PATH = 'D:/OneDrive/Documents/Money/Pay/Justin/Salesforce/'

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

def renamePayslip(filename):
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

_, _, filenames = next(walk(SOURCE_PATH))
for filename in filenames:
    renamePayslip(filename)
