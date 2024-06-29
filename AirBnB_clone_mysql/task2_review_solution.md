### Understanding the Task

The task requires writing a SQL script (`setup_mysql_dev.sql`) that will set up a MySQL server for the project. Specifically, the script should:

1. Create a database named `hbnb_dev_db`.
2. Create a new user `hbnb_dev` with a password `hbnb_dev_pwd`.
3. Grant all privileges on the `hbnb_dev_db` database to the `hbnb_dev` user.
4. Grant SELECT privilege on the `performance_schema` database to the `hbnb_dev` user.
5. Ensure the script does not fail if the database or user already exists.

### Step-by-Step Guide

1. **Understand MySQL Basics**: Before writing the script, it's important to understand basic MySQL commands for creating databases, users, and granting privileges.

2. **Create the Database**: Use the `CREATE DATABASE` command to create the `hbnb_dev_db` database. Ensure you include a check to avoid errors if the database already exists.

3. **Create the User**: Use the `CREATE USER` command to create the `hbnb_dev` user with the specified password. Include a check to handle the case where the user already exists.

4. **Grant Privileges**: Use the `GRANT` command to:
   - Grant all privileges on `hbnb_dev_db` to `hbnb_dev`.
   - Grant SELECT privilege on `performance_schema` to `hbnb_dev`.

5. **Combine Commands in a Script**: Combine all the above steps into a single SQL script (`setup_mysql_dev.sql`) that can be executed to set up the MySQL server.

### Explanation of Concepts

1. **Creating a Database**:
   - **Command**: `CREATE DATABASE`
   - **Purpose**: This command creates a new database in the MySQL server.
   - **Why**: The project needs a dedicated database (`hbnb_dev_db`) to store data.

2. **Creating a User**:
   - **Command**: `CREATE USER`
   - **Purpose**: This command creates a new user with specified credentials.
   - **Why**: The project requires a specific user (`hbnb_dev`) to access and manipulate the database.

3. **Granting Privileges**:
   - **Command**: `GRANT`
   - **Purpose**: This command assigns specific privileges to a user on a database.
   - **Why**: Granting all privileges on `hbnb_dev_db` allows `hbnb_dev` to perform all necessary operations. Granting SELECT privilege on `performance_schema` provides read-only access to performance-related information.

4. **Error Handling**:
   - **Command**: `IF NOT EXISTS`
   - **Purpose**: This clause prevents errors if the database or user already exists.
   - **Why**: To ensure the script runs smoothly without failing due to pre-existing database or user.

### Example Steps to Implement the Script

1. **Start by Creating the Database**:
   - Use `CREATE DATABASE IF NOT EXISTS hbnb_dev_db;`

2. **Create the User**:
   - Use `CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';`

3. **Grant All Privileges on the Database**:
   - Use `GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';`

4. **Grant SELECT Privilege on performance_schema**:
   - Use `GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';`

5. **Finalize the Script**:
   - Combine all the commands into a single file named `setup_mysql_dev.sql`.

### Example Script

Here is an example of how the SQL script should look:

```sql
-- Create database
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create user
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant all privileges on hbnb_dev_db
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- Grant SELECT privilege on performance_schema
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- Apply the changes
FLUSH PRIVILEGES;
```

### Running the Script

1. **Save the Script**: Save the above SQL commands in a file named `setup_mysql_dev.sql`.
2. **Execute the Script**:
   - Open a terminal and navigate to the directory containing the script.
   - Run the command:
     ```bash
     cat setup_mysql_dev.sql | mysql -hlocalhost -uroot -p
     ```
   - Enter the MySQL root password when prompted.

### Expected Output

- The script should execute without errors.
- The `hbnb_dev_db` database should be created.
- The `hbnb_dev` user should be created with the specified password.
- The `hbnb_dev` user should have all privileges on `hbnb_dev_db` and SELECT privilege on `performance_schema`.

By following this guide, you should be able to create a script that sets up the MySQL server according to the task requirements.
