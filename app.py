from pymongo import MongoClient
import streamlit as st
import pandas as pd
import string
import random

# myclient = pymongo.MongoClient("mongodb://10.105.76.163:27017/")
myclient = MongoClient('mongodb+srv://owlhacks-project.kptrr.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509',

                     authMechanism="MONGODB-X509",

                     tls=True,

                     tlsCertificateKeyFile='../../../Desktop/mongosh-2.3.1-linux-x64/X509-cert-7237033286341438670.pem')

mydb = myclient["Owlhacks-Project"]

mycol = mydb["scores"]

# mycol.delete_many({})

mylist = [
    { "name": "Amy", "address": "Apple st 652", "time": 3},
    { "name": "Hannah", "address": "Mountain 21", "time": 4},
    { "name": "Michael", "address": "Valley 345", "time": 5},
    { "name": "Sandy", "address": "Ocean blvd 2", "time": 1},
    { "name": "Betty", "address": "Green Grass 1", "time": 2.6},
    { "name": "Richard", "address": "Sky st 331", "time": 8},
    { "name": "Susan", "address": "One way 98", "time": 6},
    { "name": "Vicky", "address": "Yellow Garden 2", "time": 7},
    { "name": "Ben", "address": "Park Lane 38", "time": 39823984},
    { "name": "William", "address": "Central st 954", "time": 38},
    { "name": "Chuck", "address": "Main Road 989", "time": 39},
    { "name": "Viola", "address": "Sideway 1633", "time": 0}
]

# mycol.insert_many(mylist)

# def sortFunc(e):
    # return e["time"]
time_values = []
user_values = []
data = mycol.find().sort('time')
for x in data:
    time_values.append(x["time"])
    user_values.append(x["name"]+" "+random.choice("😀🤣😇🤩😛🤪🤗😏😌🥳🧐😲"))
    print(x)

print(time_values)
print(user_values)
# for x in mycol.find():
#     data.append(x)
# data.sort(key=sortFunc)

# Accessing the "time" values
# time_values = sorted([item['time'] for item in mylist])
# user_values = [item['name'] for item in mylist]
# Print the time values

# res = {}
# for key in time_values:
#     for value in user_values:
#         res[key] = value
#         user_values.remove(value)
#         break
# print(data)

df = pd.DataFrame({
  'Username': user_values,
  'Best Time': time_values
})

df
