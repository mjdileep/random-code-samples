import time
from opcua import Client
import pandas as pd

url = 'opc.tcp://localhost:5011/IcoFwxServer' # OPC server (here i have used OPC server by iconics)
client = Client(url, timeout=2)
"""
client._username = "user"
client._password = "passward@007"
"""
client.connect()
tags = pd.read_csv("tags.csv")


success = 0
errors = 0
batch_size = 5
t = time.time()
nodes = []
for tag in tags["Tag"].to_list():
    try:
        node = client.get_node(tag)
        nodes.append(node)
        success+=1
    except:
        errors+=1

print("time:",time.time()-t)
print("Errors:",errors)
print("Success:",success)

values = []
print("Reading values.....")
t = time.time()
for i in range(0, len(nodes), batch_size):
    print(i)
    try:
        v = client.get_values(nodes[i:i+batch_size])
        values+=v
    except:
        print("Retrying.....")
        try:
            v = client.get_values(nodes[i:i+batch_size])
            values+=v
        except:
            print("error:",i,":",i)
    
    print("Time:",time.time()-t)
print("Time:",time.time()-t)
print(values)
