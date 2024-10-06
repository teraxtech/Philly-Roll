from pymongo import MongoClient
import streamlit as st
import pandas as pd
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import json
import traceback

# myclient = pymongo.MongoClient("mongodb://10.105.76.163:27017/")
myclient = MongoClient('mongodb+srv://owlhacks-project.kptrr.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509',
                       authMechanism="MONGODB-X509",
                       tls=True,
                       tlsCertificateKeyFile='../../../Desktop/mongosh-2.3.1-linux-x64/X509-cert-7237033286341438670.pem')

mydb = myclient["Owlhacks-Project"]

mycol = mydb["scores"]

mycol.delete_many({})

mylist = [
    {"name": "Amy", "monuments": "Apple st 652", "time": 3},
    {"name": "Hannah", "monuments": "Mountain 21", "time": 4},
    {"name": "Michael", "monuments": "Valley 345", "time": 5},
    {"name": "Sandy", "monuments": "Ocean blvd 2", "time": 1},
    {"name": "Betty", "monuments": "Green Grass 1", "time": 2.6},
    {"name": "Richard", "monuments": "Sky st 331", "time": 8},
    {"name": "Susan", "monuments": "One way 98", "time": 6},
    {"name": "Vicky", "monuments": "Yellow Garden 2", "time": 7},
    {"name": "Ben", "monuments": "Park Lane 38", "time": 39823984},
    {"name": "William", "monuments": "Central st 954", "time": 38},
    {"name": "Chuck", "monuments": "Main Road 989", "time": 39},
    {"name": "Viola", "monuments": "Sideway 1633", "time": 0}
]

x = mycol.insert_many(mylist)
# def reload():
time_values = []
user_values = []
monument_values = []
data = mycol.find().sort('time')
for x in data:
    time_values.append(x["time"])
    monument_values.append(x["monuments"])
    user_values.append(random.choice("😀🤣😇🤩😛🤪🤗😏😌🥳🧐😲")+" "+x["name"])

print(time_values)
print(user_values)

st.title('Leaderboard')

time = st.table(pd.DataFrame({
    'Username': user_values,
    'Monuments renovated': monument_values,
    'Best time': time_values
}))

def run_server(port):

    class Server(BaseHTTPRequestHandler):

        # def do_GET(self):
        #     self.send_response(200)
        #     self.send_header("Content-type", "text/html")
        #     self.end_headers()
        #     self.wfile.write("""
        #     <html><head><title>GET</title></head>
        #     <body style="display: grid; place-items: center;">
        #     <form method="POST">
        #     <p>Blue: <input name="blue" value="robin's egg"></p>
        #     <p>Green: <input name="green" value="sea foam"></p>
        #     <p>Red: <input name="red" type="range" min="0" max ="100" step="0.01" value="27.76"></p>
        #     <p><button>Submit</button></p>
        #     </form>
        #     </body></html>
        # """.encode("utf-8"))

        def do_PUT(self):
            length = int(self.headers.get('content-length'))
            field_data = self.rfile.read(length)
            fields = parse.parse_qs(str(field_data,"UTF-8"))
            print(fields)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(("""
            <html><head><title>POST</title></head>
            <body style="display: grid; place-items: center;">
            <pre>%s</pre>
            </body></html>\n
            """ % (json.dumps(fields, indent=2))).encode("UTF-8"))

            try:
                if isinstance(fields["time"][0], str) and isinstance(int(fields["time"][0]), int) and isinstance(fields["name"][0], str):
                    fields["time"]=int(fields["time"][0])
                    fields["name"]=fields["name"][0]
                    fields["monuments"]=fields["monuments"][0]

# , "monuments": fields["monuments"]
                    print(mycol.find_one({"name": fields["name"]}))
                    print(not mycol.find_one({"name": fields["name"]}))
                    if not mycol.find_one({"name": fields["name"], "monuments": fields["monuments"]}):
                        print(mycol.insert_one(fields))

                    if fields["time"] < mycol.find_one({"name": fields["name"], "monuments": fields["monuments"]})["time"]:
                        mycol.update_one({"name": fields["name"], "monuments": fields["monuments"]}, { "$set": {"time": fields["time"]} })

                    user_values = []
                    monument_values = []
                    time_values = []
                    data = mycol.find().sort('time')
                    for x in data:
                        monument_values.append(x["monuments"])
                        user_values.append(random.choice("😀🤣😇🤩😛🤪🤗😏😌🥳🧐😲")+" "+x["name"])
                        time_values.append(x["time"])

                    print(time_values)
                    print(user_values)

                    time.table(pd.DataFrame({
                        'Username': user_values,
                        'Monuments destroyed': monument_values,
                        'Best Time': time_values
                    }))
                else:
                    print("invalid message recieved")
                    print(fields)
                    print(type(fields["time"][0]))
                    print(type(fields["name"][0]))
            except Exception as e:
                print("something went wrong")
                traceback.print_exc()

    handler_class = Server
    httpd = HTTPServer(('', port), handler_class)
    print('Browse to http://localhost:%s' % port)
    httpd.serve_forever() 

if __name__ == '__main__':
    run_server(8888)
