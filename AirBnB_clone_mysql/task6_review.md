### Explanation of the Task

The task involves updating a project to switch its storage system from a file-based system to a database system using SQLAlchemy. SQLAlchemy is a powerful tool that helps manage databases in Python by providing an ORM (Object-Relational Mapping), which allows you to work with database records as if they were regular Python objects.

In simple terms, you will:
1. Update some of your model classes to include database-specific attributes.
2. Create a new storage engine that interacts with a MySQL database instead of files.
3. Ensure your project can switch between using the file-based storage and the new database storage by using environment variables.

### Step-by-Step Guide

#### 1. Understand BaseModel Updates

**Concepts:**
- **Declarative Base:** This is the base class for all models using SQLAlchemy. It helps define what columns and relationships the models have.
- **Columns:** These are the attributes of your database table.
- **Primary Key:** A unique identifier for each record in a table.
- **Datetime:** A data type to store dates and times.

**Steps:**
- **Create a Declarative Base:** Define a base for all your SQLAlchemy models using `declarative_base()`.
- **Add SQLAlchemy Columns:** Update `BaseModel` to include columns for `id`, `created_at`, and `updated_at`.
- **Move Initialization Logic:** Change where you initialize new models to ensure they are properly added to storage.
- **Update `to_dict` Method:** Make sure the dictionary representation of models doesn't include SQLAlchemy-specific metadata.
- **Add `delete` Method:** Include a method to remove instances from storage.

#### 2. Update the City Model

**Concepts:**
- **Inheritance:** The City model will inherit from both `BaseModel` and the SQLAlchemy base.
- **Table Name:** This is how SQLAlchemy knows what table in the database the model corresponds to.
- **Foreign Key:** This links one table to another (e.g., linking cities to states).

**Steps:**
- **Set Table Name:** Define a `__tablename__` for the City model.
- **Add Columns:** Include columns for `name` and `state_id`, with `state_id` being a foreign key.

#### 3. Update the State Model

**Concepts:**
- **Relationships:** Define how different tables/models are related (e.g., states have many cities).
- **Cascade Delete:** Automatically delete related records (e.g., deleting a state should delete all its cities).

**Steps:**
- **Set Table Name:** Define a `__tablename__` for the State model.
- **Add Columns:** Include a column for `name`.
- **Define Relationships:** Add a relationship to link states to cities and ensure cascading deletes.

#### 4. Create the DBStorage Engine

**Concepts:**
- **Engine:** Connects to the database.
- **Sessions:** Handle transactions with the database.
- **Environment Variables:** Store sensitive data like database credentials outside your code for security.

**Steps:**
- **Initialize the Engine:** Create an engine connected to the MySQL database.
- **Session Management:** Set up sessions to handle database transactions.
- **CRUD Operations:** Implement methods for creating, reading, updating, and deleting records.

#### 5. Update Initialization Logic

**Concepts:**
- **Conditional Logic:** Use environment variables to determine which storage system to use (file-based or database).

**Steps:**
- **Import Storage Engines:** Conditionally import and initialize `FileStorage` or `DBStorage` based on the environment variable `HBNB_TYPE_STORAGE`.
- **Reload Storage:** Ensure storage is properly set up and ready to use.

#### 6. Testing

**Concepts:**
- **Environment Variables:** Use them to switch between storage types during testing.
- **SQL Queries:** Check the database directly to ensure data is being stored correctly.

**Steps:**
- **Create States and Cities:** Use the command-line interface to create and view states and cities.
- **Verify Data:** Use SQL queries to confirm data is correctly saved in the database.

### Summary
By following these steps, you will transition your project from using a file-based storage system to a more robust and scalable database storage system using SQLAlchemy. This allows you to leverage the power of SQL databases while keeping your code clean and maintainable.
