import requests
import random
import razorpay

def sendotp(mobilenumber):
    otp=random.randint(1000,9999)
    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = f"variables_values={otp}&route=otp&numbers={mobilenumber}"
    headers = {
        'authorization': "jGMpbHuHOq35AFV26oha2gX3IoLfW2WaS8urwhDQkr1ihpkhKOsMrwAYDzES",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

    import http.client

    conn = http.client.HTTPSConnection("d7sms.p.rapidapi.com")

    headers = {
        'Token': "undefined",
        'X-RapidAPI-Key': "151ad70285msh597648138d24f0ep187c02jsn57c0c507846e",
        'X-RapidAPI-Host': "d7sms.p.rapidapi.com"
        }

    conn.request("POST", "/messages/v1/balance", headers=headers)
    return otp

user1={}
otp=1
cart={}
send=False


def generateRazorpay(total,orderid):
    client = razorpay.Client(auth=("rzp_test_NGcaol52IYnJlE", "gkZTEBj16uIheoeMGeB8MTAb"))

    DATA = {
        "amount": total,
        "currency": "INR",
        "receipt": str(orderid),
        "notes": {
            "key1": "value3",
            "key2": "value2"
        }
    }
    data=client.order.create(data=DATA)
    return data

class Sales:
        def __init__(self,name,soldquantity,price,totprice,img):
            self.name=name
            self.soldqn=soldquantity
            self.price=price
            self.totprice=totprice
            self.img=img
dat=""