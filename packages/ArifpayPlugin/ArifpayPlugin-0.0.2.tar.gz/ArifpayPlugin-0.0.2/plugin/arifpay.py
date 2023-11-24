import uuid
import os 
import requests
import json
import uuid
from dotenv import load_dotenv
import requests
load_dotenv()
BASE_URL=os.environ.get("Base_url")
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

    def make_payment(self, payment_info):
        required_fields = [
            "cancelUrl",
            "successUrl",
            "errorUrl",
            "notifyUrl",
            "paymentMethods",
            "items",
            "beneficiaries",
        ]

        missing_fields = []
        for field in required_fields:
            if not payment_info.get(field):
                missing_fields.append(field)
        if missing_fields:
            missing_fields_obj = {}
            for field in missing_fields:
                missing_fields_obj[field] = f"{field} is a required field please enter this field"
            return missing_fields_obj
        payment_info['nonce'] = str(uuid.uuid4())
        payment_info['expireDate'] = self.expireDate
        payment_info = self.change_to_number(payment_info)
        print(payment_info)

        if not missing_fields:
            url = BASE_URL + MakePayment_url
            body= json.dumps(payment_info),
            options = {
             
                    "Content-Type": "application/json",
                    "x-arifpay-key": self.API_key,
            }

            response = requests.post(url=url,headers=options,data=body)
