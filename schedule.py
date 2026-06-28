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

data_in_dict = { 
"tasks": [  { "name": "physics assignemnt", "deadline": "10th June", "priority": "urgent" }  ], 
"events":[ {"name":"Team meeting", "date":"5th July", "time":"5pm","duration(hours)":1}]  
}

save_db("schedule.json",data_in_dict)


