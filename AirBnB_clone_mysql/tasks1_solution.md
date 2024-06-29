### Current Implementation

The provided `console.py` file contains the command interpreter for the AirBnB clone project. It supports various commands to create, show, destroy, update objects, and interact with the storage system. The `file_storage.py` file defines the `FileStorage` class, which manages storing and retrieving objects in JSON format.

### Task Requirements

You need to update the `do_create` method in `console.py` to allow creating objects with parameters passed through the command line. Additionally, add appropriate tests to ensure the functionality works as expected.

### Concepts and Steps to Implement the Changes

#### Understanding the Question

You need to modify the `do_create` method to accept additional parameters in the format `key=value` during object creation. These parameters will be parsed and assigned to the created object. Ensure the implementation supports different types of values (strings, integers, floats) and handles edge cases.

#### Steps to Implement the Changes

1. **Update `do_create` Method:**
    - **Parse Parameters:** Split the input arguments to separate the class name from the parameters.
    - **Validate Parameters:** Ensure parameters follow the required syntax and types.
    - **Create Object:** Use the parsed parameters to create an object of the specified class.
    - **Save Object:** Store the created object using the `FileStorage` class.

2. **Add Tests:**
    - **Unit Tests:** Create tests to verify object creation with different types of parameters.
    - **Edge Cases:** Add tests for invalid inputs and ensure the program handles them gracefully.

### Detailed Steps

1. **Parsing Parameters:**
    - Split the input string to separate the class name from the rest of the parameters.
    - For each parameter, split it by the `=` sign to get the key and value.
    - Process the value to handle strings (with quotes), integers, and floats.

2. **Validate Parameters:**
    - Ensure the class name is valid and exists in the available classes.
    - Check each parameter to ensure it follows the required format.
    - Convert and escape values as needed (e.g., handle quotes and underscores).

3. **Create and Save Object:**
    - Use the class name to instantiate an object.
    - Set the attributes of the object using the parsed parameters.
    - Save the object using the `new` and `save` methods of `FileStorage`.

4. **Write Unit Tests:**
    - Create tests to verify successful object creation with valid parameters.
    - Add tests to handle invalid parameters and ensure the program skips them.

### Implementing the Changes

Here are the modified versions of `console.py` and `file_storage.py` with the required changes.

#### Modified `console.py`

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
        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if not c_id:
            print("** instance id missing **")
            return
        key = c_name + "." + c_id
        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        print_list =

 []
        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage.all().items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for k, v in storage.all().items():
                print_list.append(str(v))
        print("[", end="")
        print(", ".join(print_list), end="")
        print("]")

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all objects of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        if args:
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k in storage.all().keys():
                if k.split('.')[0] == args:
                    count += 1
        print(count)

    def help_count(self):
        """ Help information for the count command """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        c_name = c_id = att_name = att_val = kwargs = ''

        # isolate class name
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # key = <class-name>.<object-id>
        key = c_name + "." + c_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and isinstance(eval(args[2]), dict):
            kwargs = eval(args[2])
            args = []  # reformat kwargs into list for ease of extraction
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:
            args = args[2]
            if args and args[0] == '\"':  # reformat args
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            # if att_name was not quoted arg
            if not att_name and args[0] != ' ':
                att_name = args[0]
            # check for quoted val arg
            if args[2] and args[2][0] == '\"':
                att_val = args[2][1:args[2].find('\"', 1)]
            else:
                att_val = args[2]

            # if att_val was not quoted arg
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]

            args = [att_name, att_val]

        # retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # iterate through attr names and values
        for i in range(0, len(args), 2):
            att_name = args[i]
            att_val = args[i + 1]

            if not att_name:  # check for None
                continue
            if not att_val:  # check for None
                continue

            # type cast as necessary
            if att_name in HBNBCommand.types:
                att_val = HBNBCommand.types[att_name](att_val)

            # update dictionary with name, val pair
            new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # save updates to file

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")

if __name__ == "__main__":
    HBNBCommand().cmdloop()
```

#### Modified `file_storage.py`

```python
#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json

class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """Returns a dictionary of models currently in storage"""
        return FileStorage.__objects

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
```

### Test Script

#### `test_console.py`

```python
#!/usr/bin/python3
"""Unit tests for the HBNB console"""
import unittest
from console import HBNBCommand
from models import storage
from models.state import State
import os

class TestHBNBCommand(unittest.TestCase):
    """Test cases for the HBNBCommand class"""

    def setUp(self):
        """Set up test environment"""
        self.console = HBNBCommand()

    def tearDown(self):
        """Tear down test environment"""
        del self.console
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_create_with_params(self):
        """Test creating an object with parameters"""
        self.console.onecmd('create State name="California"')
        obj = storage.all()["State.1"]
        self.assertEqual(obj.name, "California")

    def test_create_with_invalid_params(self):
        """Test creating an object with invalid parameters"""
        self.console.onecmd('create State name="California" invalid_param')
        obj = storage.all()["State.1"]
        self.assertEqual(obj.name, "California")
        with self.assertRaises(AttributeError):
            getattr(obj, 'invalid_param')

if __name__ == "__main__":
    unittest.main()
```

This test script verifies that the `do_create` method works as expected by creating objects with and without valid parameters.
