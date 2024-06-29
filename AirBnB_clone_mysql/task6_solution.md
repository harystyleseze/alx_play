Sure, let's update the `console.py` and `file_storage.py` files to support the new storage engine `db_storage.py` and ensure the switch between file and database storage as per the provided instructions.

### Updated `__init__.py`

First, we update the `__init__.py` to handle switching between file and database storage.

```python
# __init__.py
#!/usr/bin/python3
"""This module instantiates a storage object"""
import os

type_storage = os.getenv('HBNB_TYPE_STORAGE')

if type_storage == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
```

### Updated `file_storage.py`

Here's the updated `file_storage.py` to ensure it meets the requirements:

```python
# file_storage.py
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

### New `db_storage.py`

Next, create the new `db_storage.py` file to handle database storage using SQLAlchemy.

```python
# db_storage.py
#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base

class DBStorage:
    """This class manages storage of hbnb models in MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiates a new DBStorage object"""
        from os import getenv
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')

        self.__engine = create_engine(f'mysql+mysqldb://{HBNB_MYSQL_USER}:{HBNB_MYSQL_PWD}@{HBNB_MYSQL_HOST}/{HBNB_MYSQL_DB}', pool_pre_ping=True)

        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in database"""
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        if cls is None:
            classes = [User, Place, State, City, Amenity, Review]
        else:
            classes = [cls]

        objects = {}
        for cls in classes:
            query = self.__session.query(cls)
            for obj in query.all():
                key = obj.__class__.__name__ + '.' + obj.id
                objects[key] = obj

        return objects

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reloads data from the database"""
        from models.base_model import Base
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
```

### Updated `console.py`

Here’s the updated `console.py` file to support both storage engines.

```python
# console.py
#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.__init__ import storage
from models.base_model import BaseModel
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
        """

 Prints the help documentation for EOF """
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

### Test Scripts

Here are the test scripts for the new feature.

#### `test_db_storage.py`

```python
# test_db_storage.py
#!/usr/bin/python3
"""Test suite for DBStorage class"""
import unittest
import os
from models import storage
from models.base_model import BaseModel
from models.user import User

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "Testing DBStorage only")
class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    def setUp(self):
        """Set up for the tests"""
        self.storage = storage
        self.new_user = User(email="test@test.com", password="password")
        self.new_user.save()

    def tearDown(self):
        """Tear down for the tests"""
        self.storage.delete(self.new_user)
        self.storage.save()

    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIsInstance(self.storage.all(), dict)

    def test_new(self):
        """Test that new adds an object to the database"""
        user = User(email="new@test.com", password="password")
        self.storage.new(user)
        self.storage.save()
        self.assertIn(user, self.storage.all(User).values())

    def test_save(self):
        """Test that save properly saves objects to the database"""
        self.new_user.email = "update@test.com"
        self.storage.save()
        updated_user = self.storage.all(User)[self.new_user.__class__.__name__ + '.' + self.new_user.id]
        self.assertEqual(updated_user.email, "update@test.com")

    def test_delete(self):
        """Test that delete properly deletes objects from the database"""
        self.storage.delete(self.new_user)
        self.storage.save()
        self.assertNotIn(self.new_user, self.storage.all(User).values())

    def test_reload(self):
        """Test that reload properly reloads objects from the database"""
        self.storage.reload()
        self.assertIn(self.new_user, self.storage.all(User).values())
```

#### `test_file_storage.py`

```python
# test_file_storage.py
#!/usr/bin/python3
"""

Test suite for FileStorage class"""
import unittest
import os
from models import storage
from models.base_model import BaseModel
from models.user import User

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', "Testing FileStorage only")
class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    def setUp(self):
        """Set up for the tests"""
        self.storage = storage
        self.new_user = User(email="test@test.com", password="password")
        self.new_user.save()

    def tearDown(self):
        """Tear down for the tests"""
        self.storage.delete(self.new_user)
        self.storage.save()

    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIsInstance(self.storage.all(), dict)

    def test_new(self):
        """Test that new adds an object to the storage"""
        user = User(email="new@test.com", password="password")
        self.storage.new(user)
        self.storage.save()
        self.assertIn(user, self.storage.all(User).values())

    def test_save(self):
        """Test that save properly saves objects to the file"""
        self.new_user.email = "update@test.com"
        self.storage.save()
        self.storage.reload()
        updated_user = self.storage.all(User)[self.new_user.__class__.__name__ + '.' + self.new_user.id]
        self.assertEqual(updated_user.email, "update@test.com")

    def test_delete(self):
        """Test that delete properly deletes objects from the storage"""
        self.storage.delete(self.new_user)
        self.storage.save()
        self.assertNotIn(self.new_user, self.storage.all(User).values())

    def test_reload(self):
        """Test that reload properly reloads objects from the file"""
        self.storage.reload()
        self.assertIn(self.new_user, self.storage.all(User).values())
```

These changes ensure that the project meets the requirements for supporting both file storage and database storage with SQLAlchemy.
