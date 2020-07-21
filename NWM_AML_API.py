
# def AMLStat(json_input):
#     inp=json.dumps(json_input)
#     inp1=json.loads(inp)
#     return inp1[1:3]


import json
from flask import Flask, jsonify,request
from Account import Account
from AML import AML

app=Flask(__name__)
# jsonobj=[{'PayeeAccount':''},{'BeneficiaryAcct':''},{'Currency':''},{'Amount':''}]

def validationCheck(paymentDetails):
    account = Account(paymentDetails['BeneficiaryAcc'])
    aml = AML(account.getAccountDetailsAML(paymentDetails['Amount'], paymentDetails['Currency']))
    return aml.validateAml();

@app.route("/getALMStatus",methods=['GET'])

def ALMCheck():
    #jsonobj={'PayeeAccount' : request.json['PayeeAccount']},{'BeneficiaryAcc' : request.json['BeneficiaryAcc']},{'Currency' : request.json['Currency']},{'Amount' : request.json['Amount']}
    inputDataSet={"PayeeAccount":str(request.json['PayeeAccount']),"BeneficiaryAcc":str(request.json['BeneficiaryAcc']),"Currency":request.json['Currency'],"Amount":str(request.json['Amount'])}
    if(str(request.json['Limit_Override'])=="True"):
        open('Limit_Check.txt','w').write("Yes")
    else:
        open('Limit_Check.txt','w').write("No")
    if(str(request.json['Country_Override'])=="True"):
        open('Country_Check.txt','w').write("Yes")
    else:
        open('Country_Check.txt','w').write("No")
    if(str(request.json['User_Override'])=="True"):
        open('User_Check.txt','w').write("Yes")
    else:
        open('User_Check.txt','w').write("No")

    #Change the Function name(AMLStat) with Mahesh's Function to calculate the ALM Check
    json_process=validationCheck(inputDataSet)
    #json_process=AMLStat(jsonobj)
    if(json_process['approved']=="True"):
        json_process['reason']=""
    json_process['reason']=json_process['reason'].replace(",,",",")
    return jsonify(json_process)

if(__name__=="__main__"):
    app.run()
