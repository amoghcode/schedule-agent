import json 

def load_db(filename):
    with open(filename) as file:
        data = json.load(file)
    return data 

def save_db(filename, data):
    with open(filename,"w") as file:
        json.dump(data, file)

print(load_db())

