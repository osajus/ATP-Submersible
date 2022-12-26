import json



thisdict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

print(thisdict)

data_string = json.dumps(thisdict) #data serialized
data_loaded = json.loads(data_string) #data loaded
print(type(data_string))
print(data_string)
print(type(data_loaded))
print(data_loaded)
