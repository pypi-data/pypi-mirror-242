import requests
import uuid
import os
import json
from dotenv import load_dotenv
load_dotenv()
Base_url= os.environ.get("Base_url")
MakePayment_url=os.environ.get("MakePayment_url")
class ArifPay:
    def __init__(self, API_key, expireDate):
        self.API_key = API_key
        self.expireDate = expireDate

    def change_to_number(self, data):
        for item in data['items']:
            item['quantity'] = int(item['quantity'])
            item['price'] = float(item['price'])
        for benef in data['beneficiaries']:
            benef['amount'] = float(benef['amount'])
        return data

    def Make_payment(self, payment_info):
        requiredFields = [
            "cancelUrl",
            "successUrl",
            "errorUrl",
            "notifyUrl",
            "paymentMethods",
            "items",
            "beneficiaries",
        ]

        missingFields = []
        for field in requiredFields:
            if not payment_info.get(field):
                missingFields.append(field)

        if len(missingFields) > 0:
            missingFieldsObj = {}
            for field in missingFields:
                missingFieldsObj[field] = f"{field} is a required field please enter this field"
            return missingFieldsObj

        payment_info['nonce'] = str(uuid.uuid4())
        payment_info['expireDate'] = self.expireDate
        payment_info = self.change_to_number(payment_info)
        print(payment_info)

        if len(missingFields) == 0:
            url = Base_url + MakePayment_url
            options = {
                    "Content-Type": "application/json",
                    "x-arifpay-key": self.API_key,
                    }

            response = requests.post(url,headers=options,json=payment_info)
            if response.status_code==200:
                return json.loads(response.text)
            else:
                error={}
                error["satus"]=response.status_code
                error["message"]=response.text
                return error
arifpay= ArifPay("G8FbER8zZ9uco5tLuVnNKycJwXzvJTyo","2025-02-01T03:45:27")
paymentInfo= {
    "cancelUrl": "https://example.com",
    "errorUrl": "http://error.com",
    "notifyUrl": "https://gateway.arifpay.net/test/callback",
    "successUrl": "http://example.com",
    "paymentMethods": [
      "TELEBIRR"
    ],
    "expireDate": "2025-02-01T03:45:27",
    "items": [
        {
            "name": "ሙዝ",
            "quantity": 1,
            "price": 1,
            "description": "Fresh Corner preimuim Banana.",
            "image": "https://4.imimg.com/data4/KK/KK/GLADMIN-/product-8789_bananas_golden-500x500.jpg"
        },
        {
            "name": "ሙዝ",
            "quantity": 1,
            "price": 1,
            "description": "Fresh Corner preimuim Banana.",
            "image": "https://4.imimg.com/data4/KK/KK/GLADMIN-/product-8789_bananas_golden-500x500.jpg"
        }
    ],
    "beneficiaries": [
        {
            "accountNumber": "01320811436100",
            "bank": "AWINETAA",
            "amount": 2.0
        }
    ],
}
response= arifpay.Make_payment(paymentInfo)
print(response)
         

