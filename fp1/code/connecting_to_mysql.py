# Step 1: Install MySQL coomunity edition on your local by visiting this website 
# https://dev.mysql.com/downloads/windows/installer/8.0.html
# Finish the setup by installing all the components for MySQL

# Step 3: Set up your credentials for MySQL server

# Step 2: Open MySQL workbench and create a database called 'mydatabase'
# command - create database mydatabase

# Step 4: Run the following script, with your own credentials

# Step 5: Go back to your workbench and check if the table was created or not

import pymysql

# Database connection parameters
host = 'localhost'
user = 'root'
password = 'password'
db = 'mydatabase'

# Connect to the database
connection = pymysql.connect(host=host, user=user, password=password, db=db)

try:
    with connection.cursor() as cursor:
        # Create a new table (if it doesn't exist)
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            age INT
        )
        """
        cursor.execute(sql)

        # Sample dataset
        dataset = [("Kanishk", 26), ("Bhavik", 25), ("Sindhu", 20), ("Megha", 22)]

        # Insert data into the table
        sql = "INSERT INTO users (name, age) VALUES (%s, %s)"
        for data in dataset:
            cursor.execute(sql, data)

        # Commit changes
        connection.commit()

finally:
    # Close the connection
    connection.close()
