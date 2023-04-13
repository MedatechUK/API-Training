import yaml
import requests
from flask import Flask, request
import json

app = Flask(__name__)

with open("config.yml", "r") as file:
    data = yaml.safe_load(file)

print(data['priority']['url'])
print(data['priority']['company'])

vurl = data['priority']['url']
vcompany = data['priority']['company']
uid = data['priority']['userID']
pwd = data['priority']['password']


# GET-------------

def getData():
    vinputURL = vurl + vcompany + "/" + \
        "ORDERS('SO220419')/ORDERITEMS_SUBFORM?$select=PARTNAME,ORDI"
    # print(vinputURL)
    response = requests.get(vinputURL, auth=(uid, pwd))
    # check more about the response objects attribute in python.
    print(response.json())   # Print whole data
    # print individual data
    data = response.json()['value']
    for i in range(len(data)):
        print(data[i]['PARTNAME'])


# POST----------------

def postData():
    vinputURL = vurl + vcompany + "/" + "ORDERS"
    jsoninput = {
        "DOCNO": "PR16000050",
        "ORDERITEMS_SUBFORM": [
            {
                "PARTNAME": '01057201-Arch',
                "TQUANT": 2,
                "DUEDATE": "2023-04-11T14:12:22.793Z"
            }
        ]
    }

    response = requests.post(vinputURL, auth=(uid, pwd), json=jsoninput)
    print(response.json())


# PATCH/UPDATE----------------

def patchData():
    vinputURL = vurl + vcompany + "/" + \
        "ORDERS('SO230016')/ORDERITEMS_SUBFORM(KLINE=1)"

    jsoninput = {
        "TQUANT": 30
    }
    response = requests.patch(vinputURL, auth=(uid, pwd), json=jsoninput)

    print(response.json())


# DELETE-----

def deleteData():
    vinputURL = vurl + vcompany + "/" + \
        "ORDERS('SO230016')/ORDERITEMS_SUBFORM(KLINE=1)"
    response = requests.delete(vinputURL, auth=(uid, pwd))

    print(response.text)


# ROUTE-----


def routeData():
    vinputURL = vurl + vcompany


@app.route("/<inputdata>")
def orderinfo(inputdata):
    response = requests.get(vinputURL + "/" + inputdata, auth=(uid, pwd))
    return response.json()


# getData()
# postData()
# patchData()
# deleteData()
# routeData()

"""
inptdict = [
    {'PARTNAME': 'PS-APP001', 'ORDI': 11003},
    {'PARTNAME': 'PS-1126', 'ORDI': 11004},
    {'PARTNAME': 'PS-MAINT-ANN', 'ORDI': 11006}]

count = 0
for name in inptdict:
    count = count + 1
    name['PARTNAME'] = name['PARTNAME'] + str(count)


print(inptdict)

"""

# Create a POST API Endpoint in Flask:
# Posting data from thrid party/Postman to the below route

vinputURL = vurl + vcompany
v3rdpartyURL = data['priority']['url3rdpary']


@app.route("/order", methods=["POST"])
def order_info():
    # print(request.get_json())  # print json to console
    jpayload = request.get_json()
    print(jpayload)

    # return request.get_json()  # return back to json

    # process the data in priority format.

    # repsonse = requests.post(vinputURL, auth=(uid, pwd), json=jsoninput)
    # print(response.json())

    # del jpayload["uid"]
    # del jpayload["brand"]
    jpayload.pop("uid")
    jpayload.pop("brand")  # delete the whole key and value
    # delete the key and update the existing Value with new key
    jpayload["PARTNAME"] = str(jpayload.pop("id"))
    jpayload["PARTDES"] = jpayload.pop("equipment")
    print(jpayload)

    response = requests.post(f"{vinputURL}/LOGPART",
                             auth=(uid, pwd), json=jpayload)
    return response.json()


if __name__ == "__main__":
    app.run(debug=True)
