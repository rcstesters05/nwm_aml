#!/usr/bin/env python
# coding: utf-8

#import plotly.graph_objects as go
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
import json
from Account import Account
from AML import AML
import datetime
import matplotlib.pyplot as plt

def accountDetails():
    outputWindow.show()
    account1 = Account(str(checkAccountBox.text()))
    opDict=account1.getAccountDetails()
    op=open('Account_Details.html').read()
    op=op.replace('idVal',opDict['AccountID'])
    op=op.replace('typeVal',opDict['Account Type'])
    op=op.replace('nameVal',opDict['Customer Name'])
    op=op.replace('balanceVal',opDict['Balance'])
    outputWindow.setHtml(op)

def validationCheck(paymentDetails):
    if(limitCheck.isChecked()):
        open('Limit_Check.txt','w').write("Yes")
    else:
        open('Limit_Check.txt','w').write("No")
    if(countryCheck.isChecked()):
        open('Country_Check.txt','w').write("Yes")
    else:
        open('Country_Check.txt','w').write("No")
    if(userCheck.isChecked()):
        open('User_Check.txt','w').write("Yes")
    else:
        open('User_Check.txt','w').write("No")

    account = Account(paymentDetails['BeneficiaryAcc'])
    aml = AML(account.getAccountDetailsAML(paymentDetails['Amount'], paymentDetails['Currency']))
    return aml.validateAml();

def transactionDetails():
    outputWindow.show()
    account1 = Account(str(checkAccountBox.text()))
    opList=account1.getTransactions()
    noOfTr=len(opList)
    #op=open('Table_Header.html','r').read()
    #rowHtml=open('Table_Row.html','r').read()
    dates=[]
    y_vals=[]
    for row in range(noOfTr):
        dates.append(opList[row]['TransactionDate'])
        balVal=(opList[row]['Balance Amount']).split(" ")
        y_vals.append(float(balVal[0]))
    x_vals = [datetime.datetime.strptime(d,"%d-%m-%Y").date() for d in dates]
    #formatter = mdates.DateFormatter("%Y-%m-%d")
    #formatter = mdates.DateFormatter("%Y-%m-%d")
    #formatter = mdates.DateFormatter("%Y-%m-%d")
    #formatter = mdates.DateFormatter("%Y-%m-%d")


    #fig = go.Figure(data=go.Scatter(x=x_vals, y=y_vals))
    #fig.update_layout(title='Balance Trend for Account No. '+str(checkAccountBox.text()),
     #              xaxis_title='Dates',
     #              yaxis_title='Balance (in '+str(balVal[1])+')')
    #fig.show()
    #fig.write_image("graph.png")


    fig=plt.figure()
    fig.suptitle('Balance Trend for Account No. '+ str(checkAccountBox.text()))
    plt.xlabel('Dates')
    plt.ylabel(str(balVal[1]))
    plt.xticks(rotation=30)
    plt.plot(x_vals, y_vals)
    plt.savefig('graph.png')
    #    op+=rowHtml
    #    op=op.replace('ITEM1',opList[row]['TransactionId']).replace('ITEM2',opList[row]['Status']).replace('ITEM3',opList[row]['Type']).replace('ITEM4',opList[row]['Transaction Amount']).replace('ITEM5',opList[row]['Balance Amount'])
    #op+="</tbody>    </table>    <p>&nbsp;</p>"
    #outputWindow.setHtml(op)
    outputWindow.setHtml(open('Graph.html','r').read())
    
def getBalanceTrend():
    op=open('Graph.html','r').read()
    outputWindow.show()
    outputWindow.setHtml(op)



def transactionDetailss():
    outputWindow.show()
    #outputTable.setRowCount(5)
    #outputTable.setColumnCount(5)
    #outputTable.setHorizontalHeaderLabels(['Transaction Id','Status','Type','Transaction Amount','Balance Amount'])
    #outputTable.horizontalHeader().setStretchLastSection(True) 
    #outputTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents) 
    #for i in range(5):
    #    item1=QtWidgets.QTableWidgetItem("asdf-fdf-37737484883239939-hjsdsfas8338384-3434")
    #    item1.setTextAlignment(Qt.AlignHCenter)
    #    item2=QtWidgets.QTableWidgetItem("Booked")
    #    item2.setTextAlignment(Qt.AlignHCenter)
    #    item3=QtWidgets.QTableWidgetItem("Credit")
    #    item3.setTextAlignment(Qt.AlignHCenter)
    #    item4=QtWidgets.QTableWidgetItem("24 GBP")
    #    item4.setTextAlignment(Qt.AlignHCenter)
    #    item5=QtWidgets.QTableWidgetItem("330 GBP")
    #    item5.setTextAlignment(Qt.AlignHCenter)
    #    outputTable.setItem(i,0,item1)
    #    outputTable.setItem(i,1,item2)
    #    outputTable.setItem(i,2,item3)
    #    outputTable.setItem(i,3,item4)
    #    outputTable.setItem(i,4,item5)


def anomalyAccounts():
    op=open('Anomaly_Account.html','r').read().replace('DDMMYYYY',datetime.datetime.now().strftime("%d-%m-%Y"))
    outputWindow.setHtml(op)


def maheshFunction(inputJson):
    outputDataSet={"blocked":True,"reason":"Country is Sanctioned"}
    outputJson=json.dumps(outputDataSet)
    outputWindow.setPlainText(inputJson+outputJson)
    return(outputJson)


def validate():
    inputDataSet={"PayeeAccount":str(acc1Box.text()),"BeneficiaryAcc":str(acc2Box.text()),"Currency":currencyBox.currentText(),"Amount":str(amountBox.value())}
    #inputJson=json.dumps(inputDataSet)
    outputDataSet=validationCheck(inputDataSet)
    approvedVal=outputDataSet['approved']
    reason=outputDataSet['reason']
    reasonList=reason.split(",")
    if(approvedVal=="False"):
        op=open('Payment_Blocked.html','r').read()
        reasonText="<ul>"
        for i in reasonList:
            reasonText+='<li style="text-align: left;"><em>'+str(i)+'</em></li>'
        reasonText+='</ul>'
        op=op.replace('REASON',reasonText)
        outputWindow.show()
        outputWindow.setHtml(op)
    else:
        op=open('Payment_Approved.html','r').read()
        outputWindow.show()
        outputWindow.setHtml(op)

    


def clearAll():
    acc1Box.clear()
    acc2Box.clear()
    currencyBox.setCurrentIndex(0)
    amountBox.setValue(100)
    outputWindow.clear()
    outputWindow.show()
    checkAccountBox.clear()
    limitCheck.setChecked(False)
    userCheck.setChecked(False)
    countryCheck.setChecked(False)


#Set Window Label
app = QtWidgets.QApplication([])
#window = uic.loadUi("C:\\Users\\13gur\\Desktop\\Hackathon\\mainwindow.ui")
window = uic.loadUi("mainwindow.ui")
window.setWindowTitle("NWM Anti-Money Laundering")

#Set Window icon
window.setWindowIcon(QtGui.QIcon('icon.png'))

#Add Header Image
headerLabel=window.findChild(QtWidgets.QLabel,'heading')
pixmap=QtGui.QPixmap('nw.png')
headerLabel.setPixmap(pixmap)
#headerLabel.resize(pixmap.width(),pixmap.height())


#Identify Elements

#Left Widgets
acc1Box=window.findChild(QtWidgets.QLineEdit,'account1')
acc2Box=window.findChild(QtWidgets.QLineEdit,'account2')
currencyBox=window.findChild(QtWidgets.QComboBox,'currencyBox')
currencyBox.addItems(["Select Currency...","INR","GBP","USD","EUR"])
amountBox=window.findChild(QtWidgets.QSpinBox,'amountBox')


#Bottom Buttons
validateButton=window.findChild(QtWidgets.QPushButton,'validateButton')
validateButton.clicked.connect(validate)
clearButton=window.findChild(QtWidgets.QPushButton,'clearButton')
clearButton.clicked.connect(clearAll)
limitCheck=window.findChild(QtWidgets.QCheckBox,'limitCheck')
countryCheck=window.findChild(QtWidgets.QCheckBox,'countryCheck')
userCheck=window.findChild(QtWidgets.QCheckBox,'userCheck')

#Output Widgets
outputWindow=window.findChild(QtWidgets.QTextEdit,'outputWindow')
outputWindow.show()

#Right Widgets
checkAccountBox=window.findChild(QtWidgets.QLineEdit,'checkAccount')
accountDetailsBtn=window.findChild(QtWidgets.QPushButton,'accountDetails')
accountDetailsBtn.clicked.connect(accountDetails)
transactionDetailsBtn=window.findChild(QtWidgets.QPushButton,'transactionDetails')
transactionDetailsBtn.clicked.connect(transactionDetails)
anomalyAccountsBtn=window.findChild(QtWidgets.QPushButton,'anomalyAccounts')
anomalyAccountsBtn.clicked.connect(anomalyAccounts)

#Execute 
window.show()
app.exec_()


