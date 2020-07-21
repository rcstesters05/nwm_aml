# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 18:33:08 2020

@author: Mahesh
"""

import requests
import json
from urllib.parse import quote
import urllib3
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



class Account:
    
    ## Environment Variable (Static)
    wellKnownEndpoint = 'https://api.natwest.useinfinite.io/.well-known/openid-configuration'
    clientServer_env = 'QZJSQLBX4k8FrzXiNpVrSBCf3xzM1MAZ6lqMYM2OBH8='
    connection_env = 'keep-alive'
    grant_type_env= 'client_credentials'
    apiUrlPrefix = 'https://ob.natwest.useinfinite.io'
    clientId_Env = 'zaUtYq__o6iGq9GPFb_VwVj8pP8a7QzgSvKOFSbMnB8='
    clientSecret_Env = 'QZJSQLBX4k8FrzXiNpVrSBCf3xzM1MAZ6lqMYM2OBH8='
    redirectUrl = 'http://localhost:8080/redirect_uri'
    encodedRedirectUrl = quote(redirectUrl)
    psuUsername = '123456789012@85949ee1-1950-46f7-8872-7311343ae8bd.example.org'
    transactionLimit = 15
    
    ## Object variables
    authorizationEndpoint = ''
    inputAccountId = ''
    systemAccountId= ''
    consentId = ''
    apiAccessToken = ''
    tokenEndpoint = ''
    
    
    def __init__(self, accountId):
        self.inputAccountId = accountId
        endpoints = self.getTokenEndpoint()
        self.tokenEndpoint = endpoints['token_endpoint']
        self.authorizationEndpoint = endpoints['authorization_endpoint']
        self.access_token = self.retrieveAccessToken()
        self.consentId = self.postAccountRequest()
        self.redirectUri = self.approveConsent()
        self.authorizationCode = self.getCodeFromRedirectUri()
        self.apiAccessToken = self.exchangeAccessToken()
        self.getSystemAccountNumber()
    
    def getTokenEndpoint(self):
      url = self.wellKnownEndpoint
      params = dict(Connection=self.connection_env)
      response = requests.get(url,params)
      json_obj = json.loads(response.text)
      endPoints = {}
      if not response.status_code:
          print('getTokenEndpoint is Failed')
      endPoints['token_endpoint'] = json_obj['token_endpoint']
      endPoints['authorization_endpoint'] = json_obj['authorization_endpoint']
      return endPoints


    def retrieveAccessToken(self):
        url = self.tokenEndpoint
        headers = {
          'Content-Type': 'application/x-www-form-urlencoded'
                  }
        payload = 'grant_type=client_credentials&client_id=zaUtYq__o6iGq9GPFb_VwVj8pP8a7QzgSvKOFSbMnB8%3D&client_secret=QZJSQLBX4k8FrzXiNpVrSBCf3xzM1MAZ6lqMYM2OBH8%3D&scope=accounts'
        response = requests.request("POST", url, headers=headers, data = payload, verify = False)
        json_obj = json.loads(response.text)
        if not response.status_code:
          print('retrieveAccessToken is Failed')
        return json_obj['access_token']
    
    def postAccountRequest(self):
        url = self.apiUrlPrefix + '/open-banking/v3.1/aisp/account-access-consents'
        payload = "{\n  \"Data\": {\n    \"Permissions\": [\n      \"ReadAccountsDetail\",\n      \"ReadBalances\",\n      \"ReadTransactionsCredits\",\n      \"ReadTransactionsDebits\",\n      \"ReadTransactionsDetail\"\n    ]\n  },\n  \"Risk\": {}\n}"
        headers = {
          'Authorization': 'Bearer '+self.access_token,
          'Content-Type': 'application/json'
              }
        response = requests.request("POST", url, headers=headers, data = payload, verify = False)
        json_obj = json.loads(response.text)
        if not response.status_code:
          print('postAccountRequest is Failed')
        return json_obj['Data']['ConsentId']
    
    def approveConsent(self):
        url = self.authorizationEndpoint+'?client_id='+self.clientId_Env+'&response_type=code id_token&scope=openid accounts&redirect_uri='+self.encodedRedirectUrl+'&state=ABC&request='+self.consentId+'&authorization_mode=AUTO_POSTMAN&authorization_username='+self.psuUsername
        #print (url)
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data = payload)
        json_obj = json.loads(response.text)
        if not response.status_code:
          print('approveConsent is Failed')
        return json_obj['redirectUri']

    def getCodeFromRedirectUri(self):
        lst = self.redirectUri.split('&')
        for splittedUri in lst:
            keyValue = splittedUri.split('=')
            authorizationCode = keyValue[1]
            if (keyValue[0].find('code')):
                break
            else:
                continue 
        return authorizationCode

    def exchangeAccessToken(self):
        url = self.tokenEndpoint
        payload = 'client_id='+self.clientId_Env+'&client_secret='+self.clientSecret_Env+'&redirect_uri='+self.redirectUrl+'&grant_type=authorization_code&code='+self.authorizationCode
        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
        response = requests.request("POST", url, headers=headers, data = payload, verify = False)
        json_obj = json.loads(response.text)
        if not response.status_code:
          print('exchangeAccessToken is Failed')
        return json_obj['access_token']
      
    def listAccount(self):
        url = self.apiUrlPrefix+'/open-banking/v3.1/aisp/accounts'
        payload = {}
        headers = {
          'Authorization': 'Bearer '+self.apiAccessToken,
          'Content-Type': 'application/json'
                  }
        response = requests.request("GET", url, headers=headers, data = payload, verify = False)
        json_obj = json.loads(response.text)
        if not response.status_code:
          print('listAccount is Failed')
        return (json_obj)

    def getSystemAccountNumber(self):
        url = self.apiUrlPrefix+'/open-banking/v3.1/aisp/accounts'
        payload = {}
        headers = {
          'Authorization': 'Bearer '+self.apiAccessToken,
          'Content-Type': 'application/json'
                  }
        response = requests.request("GET", url, headers=headers, data = payload, verify = False)
        json_obj = json.loads(response.text)
        if not response.status_code:
          print('getSystemAccountNumber is Failed')
        for acc in json_obj['Data']['Account']:
            if acc['Account'][0]['Identification'] == self.inputAccountId:
                self.systemAccountId = acc['AccountId']
        return (self.systemAccountId)    
    
    def listAccountDetails(self):
        url = self.apiUrlPrefix+'/open-banking/v3.1/aisp/accounts/'+self.systemAccountId
        payload = {}
        headers = {
                  'Authorization': 'Bearer '+self.apiAccessToken,
                  'Content-Type': 'application/json'
                  }
        response = requests.request("GET", url, headers=headers, data = payload, verify = False)
        json_obj = json.loads(response.text)
        if not response.status_code:
          print('listAccountDetails is Failed')
        
        customer = json_obj['Data']['Account'][0]['Account'][0]['Name'].split(',')
        accountDetails = {
              "AccountID": json_obj['Data']['Account'][0]['Account'][0]['Identification'],
              "Account Type": json_obj['Data']['Account'][0]['AccountSubType'],
              "Customer Name": customer[0],
              "Country": customer[1]
                          }
        return accountDetails
    
    def listAccountBalances(self):
        url = self.apiUrlPrefix+'/open-banking/v3.1/aisp/accounts/'+self.systemAccountId+'/balances'
        payload = {}
        headers = {
                  'Authorization': 'Bearer '+self.apiAccessToken,
                  'Content-Type': 'application/json'
                  }
        response = requests.request("GET", url, headers=headers, data = payload, verify = False)
        json_obj = json.loads(response.text)
        if not response.status_code:
          print('listAccountBalances is Failed')
        accountBalance = {
              "Balance": json_obj['Data']['Balance'][0]['Amount']['Amount'] + ' ' + json_obj['Data']['Balance'][0]['Amount']['Currency'] 
              #"Balance Currency": json_obj['Data']['Balance'][0]['Amount']['Currency']
                          }
        return accountBalance
    
    def getTransactions(self):
        url = self.apiUrlPrefix+'/open-banking/v3.1/aisp/accounts/'+self.systemAccountId+'/transactions'
        payload = {}
        headers = {
                  'Authorization': 'Bearer '+self.apiAccessToken,
                  'Content-Type': 'application/json'
                  }
        response = requests.request("GET", url, headers=headers, data = payload, verify = False)
        json_obj = json.loads(response.text)
        if not response.status_code:
          print('getTransactions is Failed')
        
        transactions = []
        for index, transact in zip(range(self.transactionLimit),json_obj['Data']['Transaction']):
            transaction= {
              #"TransactionId": transact['TransactionId'],
              "TransactionDate": datetime.strptime(transact['BookingDateTime'],"%Y-%m-%dT%H:%M:%S.%fZ")
              .strftime("%d-%m-%Y"),
              #"Status": transact['Status'],
              #"Type": transact['Balance']['CreditDebitIndicator'],
              #"Transaction Amount": transact['Amount']['Amount'] + ' ' +transact['Amount']['Currency'],
              "Balance Amount": transact['Balance']['Amount']['Amount'] + ' ' +transact['Balance']['Amount']['Currency']
                          }
            transactions.append(transaction)
                          
        return transactions
    
    def getAccountDetails(self):
        accountDetails = self.listAccountDetails();
        accountDetails['Balance'] = self.listAccountBalances()['Balance']
        return accountDetails
    
    def getAccountDetailsAML(self,transactionAmount,transactionCurrency):
        accountDetails = self.listAccountDetails();
        accountDetails['creditorCountry'] = accountDetails['Country']
        accountDetails['creditorName'] = accountDetails['Customer Name']
        accountDetails['creditorAccountID'] = accountDetails['AccountID']
        accountDetails['transactionAmount'] = transactionAmount
        accountDetails['transactionCurrency'] = transactionCurrency
        
        del accountDetails['Account Type']
        del accountDetails['Customer Name']
        del accountDetails['Country']
        del accountDetails['AccountID']
        return accountDetails
 
    
        
    
    
    
