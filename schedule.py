import json 

def load_db(filename):
    with open(filename) as file:
        data = json.load(file)
    return data 

def save_db(filename, data):
    with open(filename,"w") as file:
        json.dump(data, file)

data1 = load_db("schedule.json")

print(data1)
data1["tasks"].append({"name": "maths assignment", "deadline": "10th June", "priority": "urgent"})
save_db("schedule.json",data1)


