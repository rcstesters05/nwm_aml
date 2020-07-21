# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 00:32:42 2020

@author: Mahesh
"""

import csv

class AML:
    
    # Static Data
    userBlackListedFile = 'Blacklisted_Customers.csv'
    accountBlackListedFile = 'Blacklisted_Accounts.csv'
    currencythresholdfile = 'currencyThresholdAmount.csv'
    sactionedcountryfile = 'sactionedCountryList.csv'
    #cashheavybusinessfile = 'cashheavybusinessfile.csv'

    
    # Variables
    transactionAmount = ''
    transactionCurrency  = ''
    creditorCountry = ''
    creditorName = ''
    creditorAccountID = ''
    amlFlag = 'False'
    amlDescription = ''
    response = {}
    
    
    def __init__(self, paymentDetails):
         self.transactionAmount = paymentDetails['transactionAmount']
         self.transactionCurrency = paymentDetails['transactionCurrency']
         self.creditorCountry = paymentDetails['creditorCountry']
         self.creditorName = paymentDetails['creditorName']
         self.creditorAccountID = paymentDetails['creditorAccountID']
    
    #def isThresholdAmountBreached()
    
    def isUserBlackListed(self):
        with open(self.userBlackListedFile, 'r') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                if (dict(row)['CreditorName']==self.creditorName and dict(row)['BlacklistFlag']=='Y'):
                    return True
                else:
                    continue
        return False
    
    def isAccountBlackListed(self):
        with open(self.accountBlackListedFile, 'r') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                if (dict(row)['Account_Number']==self.creditorAccountID and dict(row)['Country']==self.creditorCountry):
                    if(dict(row)['BlacklistFlag']=='Y'):
                        return True
                    
                    else:
                        return False
                else:
                    continue
        return False
    
    def isTransactionAmtLimitExceed(self):
        with open(self.currencythresholdfile, 'r') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                if (dict(row)['Currency']==self.transactionCurrency):
                    if (int(self.transactionAmount) > int(dict(row)['ThresholdAmount'])):
                        return True
                    else:
                        return False
                else:
                    continue
        return False

    def isCountrySanctioned(self):
        with open(self.sactionedcountryfile, 'r') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                if (dict(row)['Country']==self.creditorCountry):
                    if (dict(row)['Sactioned'] == 'Y'):
                        #Check if Account is blacklisted
                        # Account is Blacklisted
                        if (self.isAccountBlackListed()):
                            self.amlDescription = 'Account is blacklisted within a sanctioned country'
                            return True
                        # Account is not Blacklisted
                        else:
                            return False
                    else:
                        return False
                else:
                    continue
        return False
    
    def validateAml(self):
        limitCheckOverride=open('Limit_Check.txt','r').read()
        countryCheckOverride=open('Country_Check.txt','r').read()
        userCheckOverride=open('User_Check.txt','r').read()
        reasonList=[]
        self.amlFlag='True'
        if(self.isTransactionAmtLimitExceed() and limitCheckOverride=="No"):
            self.amlFlag = 'False'
            self.amlDescription = 'Transaction Amount exceeds Threshold Limit,'
            reasonList.append(self.amlDescription)
        if(self.isCountrySanctioned() and countryCheckOverride=="No"):
            self.amlFlag = 'False'
            reasonList.append(self.amlDescription)
        if(self.isUserBlackListed() and userCheckOverride=="No"):
            self.amlFlag = 'False'
            self.amlDescription = 'User is blacklisted'
            reasonList.append(self.amlDescription)
                        
        self.response['approved'] = self.amlFlag
        self.response['reason'] = ",".join(reasonList)
        return self.response
