
import pymysql
import pandas as pd

# Database connection parameters
host = 'localhost'
user = 'root'
password = 'password'
db = 'mydatabase'

# Connect to the database
connection = pymysql.connect(host=host, user=user, password=password, db=db)

try:
    with connection.cursor() as cursor:
        
        # Uploading all user attributes
        
        # dropping table
        sql = """
        drop table if exists all_user_attribute
        """
        cursor.execute(sql)
        
        sql = """
        CREATE TABLE all_user_attribute (
            user_id INT ,
            mood VARCHAR(255),
            cuisine varchar(255)
        )
        """
        cursor.execute(sql)

        all_user = pd.read_csv(r"C:\Users\kanis\OneDrive - Indian School of Business\Desktop\ISB\github_codes\ampba_24_group18_term2\fp1\model_inputs\all_user_attributes.csv")
        upload_vals = all_user.values.tolist()
        

        # Insert data into the table
        sql = "INSERT INTO all_user_attribute (user_id, mood, cuisine) VALUES (%s, %s, %s)"
        cursor.executemany(sql, upload_vals)
        
        # Uploading food details
        
        # dropping table
        sql = """
        drop table if exists food_details_trimmed
        """
        cursor.execute(sql)
        
        sql = """
        CREATE TABLE food_details_trimmed (
            food_id INT ,
            name VARCHAR(255),
            c_type varchar(255),
            veg_non varchar(255),
            ingridients varchar(1000),
            image_url varchar(500)
        )
        """
        cursor.execute(sql)

        food_details = pd.read_csv(r"C:\Users\kanis\OneDrive - Indian School of Business\Desktop\ISB\github_codes\ampba_24_group18_term2\fp1\model_inputs\food_details_with_images.csv")
        upload_vals = food_details.values.tolist()
        

        # Insert data into the table
        sql = "INSERT INTO food_details_trimmed (food_id, name, c_type, veg_non, ingridients, image_url) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.executemany(sql, upload_vals)

        # Commit changes
        connection.commit()

finally:
    # Close the connection
    connection.close()
