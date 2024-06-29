3. MySQL setup development
mandatory
Score: 0.0% (Checks completed: 0.0%)
Write a script that prepares a MySQL server for the project:

A database hbnb_dev_db
A new user hbnb_dev (in localhost)
The password of hbnb_dev should be set to hbnb_dev_pwd
hbnb_dev should have all privileges on the database hbnb_dev_db (and only this database)
hbnb_dev should have SELECT privilege on the database performance_schema (and only this database)
If the database hbnb_dev_db or the user hbnb_dev already exists, your script should not fail
guillaume@ubuntu:~/AirBnB_v2$ cat setup_mysql_dev.sql | mysql -hlocalhost -uroot -p
Enter password: 
guillaume@ubuntu:~/AirBnB_v2$ echo "SHOW DATABASES;" | mysql -uhbnb_dev -p | grep hbnb_dev_db
Enter password: 
hbnb_dev_db
guillaume@ubuntu:~/AirBnB_v2$ echo "SHOW GRANTS FOR 'hbnb_dev'@'localhost';" | mysql -uroot -p
Enter password: 
Grants for hbnb_dev@localhost
GRANT USAGE ON *.* TO 'hbnb_dev'@'localhost'
GRANT SELECT ON `performance_schema`.* TO 'hbnb_dev'@'localhost'
GRANT ALL PRIVILEGES ON `hbnb_dev_db`.* TO 'hbnb_dev'@'localhost'
guillaume@ubuntu:~/AirBnB_v2$ 
Repo:

GitHub repository: AirBnB_clone_v2
File: setup_mysql_dev.sql
