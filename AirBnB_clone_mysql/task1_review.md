### Understanding the Current Implementation

**console.py**: This file contains the implementation of the command interpreter for the AirBnB clone. The main class, `HBNBCommand`, inherits from `cmd.Cmd` and provides functionalities such as creating, showing, destroying, and updating objects. It uses different commands like `create`, `show`, `all`, `update`, and `destroy` to interact with objects stored in the application.

**file_storage.py**: This file contains the `FileStorage` class, which handles the storage of objects in JSON format. It has methods to add new objects (`new`), save objects to a file (`save`), reload objects from a file (`reload`), and retrieve all objects (`all`).

### Task Requirements

To meet the task requirements, you need to update the `do_create` method in `console.py` to allow for object creation with given parameters. This involves parsing the input arguments, handling different value types (string, float, integer), and adding the necessary logic to set these values for the new object.

### Step-by-Step Guide to Implement Changes

1. **Understand the `do_create` method**: The method is responsible for creating new objects. Currently, it does not accept parameters for object attributes.

2. **Modify the Command Syntax**: Change the `do_create` method to accept additional parameters in the form of key-value pairs.

3. **Parse Parameters**: Extract and parse the parameters from the input command. You need to handle different data types:
   - **Strings**: Values enclosed in double quotes.
   - **Floats**: Values containing a dot (`.`).
   - **Integers**: Default numeric values.

4. **Handle Special Characters**: Ensure that double quotes inside string values are escaped and underscores are replaced with spaces.

5. **Set Object Attributes**: After parsing, set the extracted attributes to the new object.

6. **Skip Invalid Parameters**: If any parameter is invalid or cannot be recognized, skip it without interrupting the creation process.

7. **Add Tests**: Create tests to verify that the new feature works correctly with the `FileStorage` engine.

### Example Implementation

Here's an example of how you can modify the `do_create` method:

```python
def do_create(self, arg):
    """Creates a new instance of a class with given attributes."""
    args = arg.split()
    if not args:
        print("** class name missing **")
        return
    class_name = args[0]
    if class_name not in HBNBCommand.classes:
        print("** class doesn't exist **")
        return
    
    new_instance = HBNBCommand.classes[class_name]()
    for param in args[1:]:
        key_value = param.split('=')
        if len(key_value) != 2:
            continue
        key, value = key_value
        value = value.strip('"').replace('_', ' ')
        if value.isdigit():
            value = int(value)
        else:
            try:
                value = float(value)
            except ValueError:
                pass
        setattr(new_instance, key, value)
    
    new_instance.save()
    print(new_instance.id)
```

### Testing the Implementation

1. **Run the Console**:
   ```bash
   ./console.py
   ```

2. **Create Objects with Parameters**:
   ```bash
   (hbnb) create State name="California"
   (hbnb) create Place city_id="0001" user_id="0001" name="My_little_house" number_rooms=4 number_bathrooms=2 max_guest=10 price_by_night=300 latitude=37.773972 longitude=-122.431297
   ```

3. **Verify the Creation**:
   ```bash
   (hbnb) all State
   (hbnb) all Place
   ```

This guide should help you understand the task requirements and implement the necessary changes to `console.py` and `file_storage.py`.
