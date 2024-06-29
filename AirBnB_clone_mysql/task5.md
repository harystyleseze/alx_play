5. Delete object
mandatory
Score: 0.0% (Checks completed: 0.0%)
Update FileStorage: (models/engine/file_storage.py)

Add a new public instance method: def delete(self, obj=None): to delete obj from __objects if it’s inside - if obj is equal to None, the method should not do anything
Update the prototype of def all(self) to def all(self, cls=None) - that returns the list of objects of one type of class. Example below with State - it’s an optional filtering
guillaume@ubuntu:~/AirBnB_v2$ cat main_delete.py
#!/usr/bin/python3
""" Test delete feature
"""
from models.engine.file_storage import FileStorage
from models.state import State

fs = FileStorage()

# All States
all_states = fs.all(State)
print("All States: {}".format(len(all_states.keys())))
for state_key in all_states.keys():
    print(all_states[state_key])

# Create a new State
new_state = State()
new_state.name = "California"
fs.new(new_state)
fs.save()
print("New State: {}".format(new_state))

# All States
all_states = fs.all(State)
print("All States: {}".format(len(all_states.keys())))
for state_key in all_states.keys():
    print(all_states[state_key])

# Create another State
another_state = State()
another_state.name = "Nevada"
fs.new(another_state)
fs.save()
print("Another State: {}".format(another_state))

# All States
all_states = fs.all(State)
print("All States: {}".format(len(all_states.keys())))
for state_key in all_states.keys():
    print(all_states[state_key])        

# Delete the new State
fs.delete(new_state)

# All States
all_states = fs.all(State)
print("All States: {}".format(len(all_states.keys())))
for state_key in all_states.keys():
    print(all_states[state_key])

guillaume@ubuntu:~/AirBnB_v2$ ./main_delete.py
All States: 0
New State: [State] (b0026fc6-116f-4d1a-a9cb-6bb9b299f1ce) {'name': 'California', 'created_at': datetime.datetime(2017, 11, 10, 1, 13, 32, 561137), 'id': 'b0026fc6-116f-4d1a-a9cb-6bb9b299f1ce'}
All States: 1
[State] (b0026fc6-116f-4d1a-a9cb-6bb9b299f1ce) {'name': 'California', 'created_at': datetime.datetime(2017, 11, 10, 1, 13, 32, 561137), 'id': 'b0026fc6-116f-4d1a-a9cb-6bb9b299f1ce'}
Another State: [State] (37705d25-8903-4318-9303-6d6d336a22c1) {'name': 'Nevada', 'created_at': datetime.datetime(2017, 11, 10, 1, 13, 34, 619133), 'id': '37705d25-8903-4318-9303-6d6d336a22c1'}
All States: 2
[State] (b0026fc6-116f-4d1a-a9cb-6bb9b299f1ce) {'name': 'California', 'created_at': datetime.datetime(2017, 11, 10, 1, 13, 32, 561137), 'id': 'b0026fc6-116f-4d1a-a9cb-6bb9b299f1ce'}
[State] (37705d25-8903-4318-9303-6d6d336a22c1) {'name': 'Nevada', 'created_at': datetime.datetime(2017, 11, 10, 1, 13, 34, 619133), 'id': '37705d25-8903-4318-9303-6d6d336a22c1'}
All States: 1
[State] (37705d25-8903-4318-9303-6d6d336a22c1) {'name': 'Nevada', 'created_at': datetime.datetime(2017, 11, 10, 1, 13, 34, 619133), 'id': '37705d25-8903-4318-9303-6d6d336a22c1'}
guillaume@ubuntu:~/AirBnB_v2$ 
Repo:

GitHub repository: AirBnB_clone_v2
File: models/engine/file_storage.py
