Arifpay Python plugin 
A package used to integrate to the arifpays gateway .

How to use
After installing the package use following import:

from ArifpayPlugin import Arifpay

Then use following code:

arifpay= Arifpay("Api key","expiredate")
response=arifpay.Make_payement(payment_info)
print(response)

2023-package/app/README.md at main · ArjanCodes/2023-package