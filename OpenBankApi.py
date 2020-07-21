# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 01:29:08 2020

@author: Mahesh
"""
import json
from Account import Account
from AML import AML

    
    
def validate(paymentDetails):
    account = Account(paymentDetails['BeneficiaryAcc'])
    aml = AML(account.getAccountDetailsAML(paymentDetails['Amount'], paymentDetails['Currency']))
    return aml.validateAml();
 

account1 = Account('50000012345601') # Amarjeet
print(account1.getAccountDetails())
print(account1.getTransactions())

account2 = Account('50000012345602') # Abhishek
print(account2.getAccountDetails())
print(account2.getTransactions())
 
inputJson1 = {'PayeeAccount': '50000012345602','BeneficiaryAcc': '50000012345601',
                'Currency': 'GBP',
                'Amount': '100'}

inputJson2 = {'PayeeAccount': '50000012345601','BeneficiaryAcc': '50000012345602',
                'Currency': 'GBP',
                'Amount': '100'}

print(OpenBankApi.validate(inputJson1))
print(OpenBankApi.validate(inputJson2))




