### Understanding the Question

The task is to modify the `FileStorage` class in the `models/engine/file_storage.py` file to add two new methods and update an existing one. These changes will allow us to delete objects from storage and filter objects by class when retrieving them.

### Task Breakdown

1. **Add a `delete` Method:**
    - This method will remove an object from storage if it exists. If the object is `None`, the method will do nothing.

2. **Update the `all` Method:**
    - Modify the `all` method to accept an optional class parameter. If a class is provided, the method should return only the objects of that class. If no class is provided, it should return all objects.

### Concepts Needed

1. **Instance Methods:**
    - Methods that operate on an instance of the class. They can access and modify the instance’s attributes.

2. **Dictionary Manipulation:**
    - You need to add, remove, and filter items in the `__objects` dictionary, which stores all objects.

3. **Class Filtering:**
    - Filtering objects based on their class type.

### Step-by-Step Guide

#### Step 1: Adding the `delete` Method

1. **Define the Method:**
    - Create a method `delete(self, obj=None)` inside the `FileStorage` class.
  
2. **Check if `obj` is None:**
    - If `obj` is `None`, the method should return immediately without doing anything.

3. **Delete Object from `__objects`:**
    - Construct the key for the object in the `__objects` dictionary using the format `<class name>.<id>`.
    - Remove the object from the dictionary if it exists.

#### Step 2: Updating the `all` Method

1. **Modify Method Signature:**
    - Change the method signature from `def all(self)` to `def all(self, cls=None)`.

2. **Filter by Class:**
    - If `cls` is `None`, return the entire `__objects` dictionary.
    - If `cls` is provided, iterate over `__objects` and include only objects of the given class in the returned dictionary.

### Detailed Steps for Each Method

#### `delete` Method

1. **Define Method:**
    ```python
    def delete(self, obj=None):
    ```

2. **Check for None:**
    ```python
    if obj is None:
        return
    ```

3. **Construct Key and Delete Object:**
    ```python
    key = obj.__class__.__name__ + '.' + obj.id
    if key in self.__objects:
        del self.__objects[key]
    ```

#### `all` Method

1. **Modify Signature:**
    ```python
    def all(self, cls=None):
    ```

2. **Return All Objects if `cls` is None:**
    ```python
    if cls is None:
        return self.__objects
    ```

3. **Filter Objects by Class:**
    ```python
    filtered_objects = {}
    for key, value in self.__objects.items():
        if isinstance(value, cls):
            filtered_objects[key] = value
    return filtered_objects
    ```

### Putting It All Together

1. **Open the `file_storage.py` file.**
2. **Add the `delete` method as described.**
3. **Update the `all` method as described.**
4. **Test the changes by writing a script similar to `main_delete.py` and verify the behavior.**

### Testing Your Changes

1. **Create Objects:**
    - Verify that objects can be created and saved.

2. **Retrieve Objects:**
    - Use the updated `all` method to retrieve all objects or filter by class.

3. **Delete Objects:**
    - Use the `delete` method to remove objects and verify they no longer exist in storage.

By following these steps, you should be able to implement the required changes and ensure they work as expected.
