Anti-Money Laundering
=====================

Introduction
------------

Money laundering is the illegal process of concealing the origins of money obtained illegally by passing it through a sequence of banking transfers & make it appear as clean money. And it is a major problem for banks to handle and early detect the illegal transfers. It attracts fines to the tune of billions of dollars to banks worldwide.

Anti-Money Laundering (AML) GUI solution enables financial institutions to apply risk based multi level checks to monitor customer behavior for suspected criminal financial activities via automated process.
It also supports reporting capabilities for regulatory requirements.
In addition,package also provides API solution which enables financial institutions to integrate the solution with their existing payments gateways.

Objective
------------
To guide the users with step by step installation of the solution. Thereafter, it also contains few Use Cases (Ref. Section- **Sample Tests**) with instructions for better user experience. 

Pre-requisites
--------------

* You should have Anaconda Navigator with Python 3.6 or higher installed on your system. You can download and install Anaconda Navigator from [here](https://www.anaconda.com/products/individual).
* You should have AML API code downloaded in your system. You can download it from [here](https://github.com/rcstesters05), if not done already.
* To check the version of python, open Anaconda Prompt from start menu and use command
    ``` nowrap
    python --version
    ```
* Postman should be installed in your system. You can download it from [here](https://www.postman.com/downloads/), if not present already.

Installation
------------

### Install

First, install the dependencies (if not already installed) using 'Anaconda Prompt' (from start menu):

``` nowrap
pip install PyQt5
``` 
``` nowrap
pip install matplotlib
```

### Running the app

Next, when 'Anaconda Prompt' is already open, then

``` nowrap
cd <location_of_AML_API_directory> 
```
Next, to run the GUI application, use command:

``` nowrap
python NWM_AML.py
```

OR, to run the AML API, use command:
``` nowrap
python NWM_AML_API.py
```

### Features

The application has been designed to showcase primarily the Anti-Money Laundering API capability along with some other useful features. 

* **GUI Application** - A User Interface driven platform using inputs similar to table below. Entering appropriate input and clicking Validate on GUI app calls the AML API in the backend and performs three-layered AML checks. Basis these checks, the payment is VALIDATED SUCCESSFULLY or MARKED FOR REVIEW which can be seen in the GUI Output Box.

  

|Payee Account| Beneficiary Account | Currency    | Amount    |
|-------------| ------------------- | --------    | ------    |
|Payee Account Number| Beneficiary Account Number     | GBP/USD/INR/EUR         | Integer (0-999999)      |

Three Override Checks have been provided for overriding layered checks of AML for further processing post Review by User.

* **AML Microservice** - Published new AML microservice which can be integrated with any payments platform or gateway for initial money laundering checks on the beneficiary side.

  Some features have been **additionally** added in the GUI to complement the broader business objective. They have been described further down below. 
  
1.  **Get Account Details** - To retrieve the account details of customer.
      Uses:
       * Help to quickly check the details of suspicious customer.
2.  **Get Balance Trend** - Displays a line-graph showing Customer's Account balance variation over time of an Account's Balance. 
    Uses :
    * Helps in integrating data mining algorithms for improvising the Money laundering checks.
    * Helps in cross selling other banking products to customers.
3. **Get Anomaly Accounts** - Displays all such accounts which have AML-Flagged transactions under Pending Approval state.
    Uses : 
    * Can be used Regulatory reporting.
    * Data-collection for Machine-Learning model


#### Sample Test 1: Testing the AML GUI Application

1. Click on Clear button.
2. Enter below information in relevant left pane input boxes :

    |Payee Account| Beneficiary Account | Currency    | Amount    |Override Check|Expected Output|
    |-------------| ------------------- | --------    | ------    |---|---------------|
    |50000012345601| 50000012345601     | GBP         | 1000      |N|Payment **Validated** Successfully|
    |50000012345601| 50000012345602     | USD         | 20000     |N|Payment **UNDER REVIEW** due to 'Transaction Amount exceeds Threshold Limit'|
    |50000012345601| 50000012345602     | USD         | 20000     |Y|Payment **Validated** Successfully|
    |50000012345602| 50000012345601     | GBP         | 2500     |N|Payment **UNDER REVIEW** due to 'Account is blacklisted within a sanctioned country'|

3. Then, Click on 'Validate' button at the bottom of the screen.
4. Finally, verify the response from AML API in Output Box

#### Sample Test 2: Testing the 'Get Account Details' feature

1. Click on Clear button.
2. Enter Account Number in **AccountToCheck(A/c - 50000012345601)** field at the right pane of screen
3. Then, Click on 'Get Account Details' button.
4. Validate the response in Output Box

#### Sample Test 3: Testing the 'Get Balance Trend' feature

1. Click on Clear button.
2. Enter Account Number in **AccountToCheck(A/c- 50000012345601)** field at the right pane of screen
3. Then, Click on 'Get Balance Trend' button.
4. Validate the balance movement in graphical form shown in Output Box

#### Sample Test 4: Testing the 'Get Anomaly Accounts' feature

1. Click on Clear button.
2. Perform several AML Checks using aforementioned testing approach. 
3. Then, Click on 'Get Anomaly Accounts' button.
4. Validate the result in Output Box.

#### Sample Test 5: Testing the AML Microservice

1. Launch 'Anaconda Prompt'
2. Go to the Codebase directory and Run command - 
    ```nowrap
    python NWM_AML_API.py
    ```
2. Launch Postman in your system
4. Run the below API using body as shown below:
    ```nowrap
    GET - http://127.0.0.0:5000/getALMStatus
    ```

    And pass API Body in json format like:
    
    ```nowrap
    {
    "PayeeAccount":50000012345601,
    "BeneficiaryAcc":50000012345602,
    "Currency":"GBP",
    "Amount":10000
    "Limit_Override":"False",
    "Country_Override":"False",
    "User_Override":"False"
    }
    ```
5. Finally, click on Send Button and validate Response from API.

### Glossary

1. Data Mining - The practice of analysing the large data in order to generate new information.
2. To get familiar with the terms, you can check the [glossary](https://bankofapis.com/glossary)