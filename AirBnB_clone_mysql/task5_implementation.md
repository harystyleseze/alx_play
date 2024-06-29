Sure, let's go through the current implementation and make the necessary changes.

### Updated `file_storage.py`

1. **Add the `delete` Method:**
    - Define a method `delete(self, obj=None)` that removes the specified object from the `__objects` dictionary if it exists. If `obj` is `None`, the method should do nothing.

2. **Update the `all` Method:**
    - Modify the `all` method to accept an optional class parameter `cls`. If `cls` is provided, return only the objects of that class. If `cls` is `None`, return all objects.

### Updated `console.py`

1. **Update the `do_destroy` Method:**
    - Ensure it uses the `delete` method from the `FileStorage` class to remove objects.

2. **Update the `do_all` Method:**
    - Use the updated `all` method from `FileStorage` to filter objects by class if a class name is provided.

Here are the updated files:

### Updated `file_storage.py`

```python
#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json

class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return FileStorage.__objects
        else:
            filtered_objects = {}
            for key, value in FileStorage.__objects.items():
                if isinstance(value, cls):
                    filtered_objects[key] = value
            return filtered_objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                        self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes obj from __objects if it's inside"""
        if obj is None:
            return
        key = obj.__class__.__name__ + '.' + obj.id
        if key in FileStorage.__objects:
            del FileStorage.__objects[key]
```

### Updated `console.py`

```python
#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import shlex

class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            if pline[pline.find('(') + 1:pline.find(')')]:
                _args = pline[pline.find('(') + 1:pline.find(')')]
                # parse tokenized args
                _args = _args.replace(',', '').replace('\'', '').replace('\"', '')
                _id = _args.split()[0]
                _args = ' '.join(_args.split()[1:])

            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class"""
        if not args:
            print("** class name missing **")
            return
        try:
            args = shlex.split(args)
            class_name = args[0]
            params = args[1:]

            if class_name not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return

            new_instance = HBNBCommand.classes[class_name]()

            for param in params:
                if '=' not in param:
                    continue

                key, value = param.split('=', 1)

                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1].replace('_', ' ').replace('\\"', '"')
                elif '.' in value:
                    try:
                        value = float(value)
                    except ValueError:
                        continue
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        continue

                setattr(new_instance, key, value)

            new_instance.save()
            print(new_instance.id)
        except Exception as e:
            print("** class doesn't exist **")

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className> <param1> <param2>...\n")

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage.all()[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]
        if not c_name:
            print("** class name missing **")
            return
        if c

_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if not c_id:
            print("** instance id missing **")
            return
        key = c_name + "." + c_id
        try:
            storage.delete(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        print_list = []
        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage.all(HBNBCommand.classes[args]).items():
                print_list.append(str(v))
        else:
            for k, v in storage.all().items():
                print_list.append(str(v))
        print("[", end="")
        print(", ".join(print_list), end="")
        print("]")

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        if not args:
            print("** class name missing **")
            return
        if args not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        count = 0
        for k in storage.all(HBNBCommand.classes[args]).keys():
            count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        c_name = c_id = att_name = att_val = kwargs = ''

        # isolate cls from id
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from rest of args
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = c_name + "." + c_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and isinstance(eval(args[2]), dict):
            kwargs = eval(args[2])
            args = []  # reformat kwargs into list for processing
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:
            args = args[2].split()
        if not args:  # ensure there are arguments
            print("** attribute name missing **")
            return
        if len(args) % 2 != 0:
            print("** value missing **")
            return

        # parse params
        for i in range(0, len(args), 2):
            att_name = args[i]
            att_val = args[i + 1]

            # handle quoted arguments
            if att_name[0] == '"' and att_name[-1] == '"':
                att_name = att_name[1:-1]
            if att_val[0] == '"' and att_val[-1] == '"':
                att_val = att_val[1:-1]

            # type cast as necessary
            if att_name in HBNBCommand.types:
                att_val = HBNBCommand.types[att_name](att_val)

            # update dictionary
            new_dict = storage.all()[key]
            setattr(new_dict, att_name, att_val)
        new_dict.save()  # save updates to file

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attrName> <attrValue>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
```

### Test Script for New Features

Let's create a test script to verify the new `delete` method and the updated `all` method in `file_storage.py`. 

Create a file named `test_file_storage.py` inside the `tests/test_models/test_engine/` directory.

```python
#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py."""
import unittest
from models.base_model import BaseModel
from models.state import State
from models.engine.file_storage import FileStorage
import os

class TestFileStorage(unittest.TestCase):
    """Unittests for testing the FileStorage class."""

    def setUp(self):
        """Set up test methods."""
        self.storage = FileStorage()
        self.state = State(name="California")
        self.state.save()
        self.key = f"State.{self.state.id}"

    def tearDown(self):
        """Tear down test methods."""
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_delete_method(self):
        """Test the delete method of FileStorage"""
        self.storage.new(self.state)
        self.storage.save()
        self.assertIn(self.key, self.storage.all())
        self.storage.delete(self.state)
        self.assertNotIn(self.key, self.storage.all())
        self.storage.delete(None)  # should not raise any exception

    def test_all_method(self):
        """Test the all method with and without class filtering"""
        self.storage.new(self.state)
        self.storage.save()
        self.assertIn(self.key, self.storage.all(State))
        self.assertNotIn(self.key, self.storage.all(BaseModel))
        self.assertIn(self.key, self.storage.all())

if __name__ == "__main__":
    unittest.main()
```

This test script covers:
1. The `delete` method to ensure it correctly deletes an object and handles `None` input.
2. The `all` method to ensure it returns the correct objects when filtering by class and without any filter. 

By implementing these changes and tests, we meet all the task requirements and ensure the correctness of the new features.