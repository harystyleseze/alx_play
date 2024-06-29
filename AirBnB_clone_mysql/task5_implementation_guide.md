To implement the changes required to meet the task requirements in both `console.py` and `file_storage.py`, follow these steps:

### Step 1: Update `FileStorage` in `file_storage.py`

1. **Add the `delete` Method:**
    - Define a method `delete(self, obj=None)` that removes the specified object from the `__objects` dictionary if it exists. If `obj` is `None`, the method should do nothing.

2. **Update the `all` Method:**
    - Modify the `all` method to accept an optional class parameter `cls`. If `cls` is provided, return only the objects of that class. If `cls` is `None`, return all objects.

#### Implementation Details for `file_storage.py`

1. **Add the `delete` Method:**
    ```python
    def delete(self, obj=None):
        """Deletes obj from __objects if it's inside"""
        if obj is None:
            return
        key = obj.__class__.__name__ + '.' + obj.id
        if key in FileStorage.__objects:
            del FileStorage.__objects[key]
    ```

2. **Update the `all` Method:**
    ```python
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
    ```

### Step 2: Update `HBNBCommand` in `console.py`

1. **Update the `do_destroy` Method:**
    - Ensure it uses the `delete` method from the `FileStorage` class to remove objects.

2. **Update the `do_all` Method:**
    - Use the updated `all` method from `FileStorage` to filter objects by class if a class name is provided.

#### Implementation Details for `console.py`

1. **Update the `do_destroy` Method:**
    ```python
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
    ```

2. **Update the `do_all` Method:**
    ```python
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
    ```

### Step 3: Add Tests for the New Features

1. **Create Test Cases for `delete` Method:**
    - Ensure that objects are properly deleted from the `FileStorage`.
    - Verify that attempting to delete `None` does nothing.

2. **Create Test Cases for the Updated `all` Method:**
    - Ensure that filtering by class works correctly.
    - Verify that without a class, all objects are returned.

#### Example Test Cases in `tests/test_models/test_engine/test_file_storage.py`

1. **Test `delete` Method:**
    ```python
    def test_delete_method(self):
        """Test the delete method of FileStorage"""
        fs = FileStorage()
        new_state = State(name="California")
        fs.new(new_state)
        fs.save()
        key = 'State.' + new_state.id
        self.assertIn(key, fs.all())
        fs.delete(new_state)
        self.assertNotIn(key, fs.all())
        fs.delete(None)  # should not raise any exception
    ```

2. **Test the Updated `all` Method:**
    ```python
    def test_all_method(self):
        """Test the all method with and without class filtering"""
        fs = FileStorage()
        new_state = State(name="California")
        new_city = City(name="San Francisco")
        fs.new(new_state)
        fs.new(new_city)
        fs.save()
        self.assertIn('State.' + new_state.id, fs.all(State))
        self.assertNotIn('City.' + new_city.id, fs.all(State))
        self.assertIn('City.' + new_city.id, fs.all())
    ```

By following these steps, you will implement the required changes and ensure that your `FileStorage` and `HBNBCommand` classes meet the task requirements.
