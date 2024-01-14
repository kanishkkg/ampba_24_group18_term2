# Database connection parameters
host = 'localhost'
user = 'root'
password = 'password'
db = 'mydatabase'

import urllib.request
import json
import pandas as pd
import pymysql



def sim_user(mood, cuisine_preferences):
    '''
    Function to find similar users as the current user

    Parameters
    ----------
    mood : string
        DESCRIPTION.
    cuisine_preferences : string
        DESCRIPTION.

    Returns
    -------
    user_id : int
        DESCRIPTION.

    '''
    # Opening database connection
    connection = pymysql.connect(host=host, user=user, password=password, db=db)
    cursor = connection.cursor()
    
    sql = '''
    select * 
    from all_user_attribute
    where user_id >= 2000
    '''
    cursor.execute(sql)
    data = cursor.fetchall()
    
    user_data = pd.DataFrame(data, columns=['user_id', 'mood', 'cuisine'])
    
    # Finding user id with the same mood and cuisine
    user_id = user_data[(user_data['mood'].str.lower() == mood.lower().strip()) \
                        & (user_data['cuisine'].str.lower() == cuisine_preferences.lower().strip())]['user_id'].iloc[0]
        
    cursor.close()
    
    return user_id


def get_food_id(food_list):
    # Opening database connection
    connection = pymysql.connect(host=host, user=user, password=password, db=db)
    cursor = connection.cursor()
    
    sql = '''
    select food_id, lower(name) as name
    from food_details_trimmed
    '''
    cursor.execute(sql)
    data = cursor.fetchall()
    
    food_data = pd.DataFrame(data, columns=['food_id', 'food_name'])
    
    food_ids = []
    
    for food in food_list:
        for _ , name in food_data.iterrows():
            if food.lower() == name['food_name'].lower():
                food_ids.append(name['food_id'])
                continue

    
    cursor.close()
    return food_ids

def get_food_details(food_ids):
    # Opening database connection
    connection = pymysql.connect(host=host, user=user, password=password, db=db)
    cursor = connection.cursor()
    
    sql = '''
    select food_id, lower(name) as name, ingridients, image_url
    from food_details_trimmed
    '''
    cursor.execute(sql)
    data = cursor.fetchall()
    
    food_data = pd.DataFrame(data, columns=['food_id', 'food_name', 'ingridients', 'image_url'])
    
    details = pd.DataFrame({'food_id': [],
                            'food_name': [],
                            'ingridients': [],
                            'image_url': []})
    
    for food in food_ids:
        for _ , name in food_data.iterrows():
            if int(food) == int(name['food_id']):
                details = pd.concat([details, pd.DataFrame({'food_id': [name['food_id']],
                                                            'food_name': name['food_name'],
                                                            'ingridients': name['ingridients'],
                                                            'image_url': name['image_url']})])
                continue
               
    cursor.close()
    
    return details
    
def prediction(user_data):
    '''
    Function to call the Azure ML API and generate food recommendation

    Parameters
    ----------
    user_data : Pandas DataFrame
        DataFrame containing the user_id, food_id and the rating.

    Returns
    -------
    Raw response from the API endpoint.

    '''
    
    try:
        
        data =  {
        
                "Inputs": {
        
                        "input1":
                        {
                            "ColumnNames": ["user_id", "food_id", "rating"],
                            "Values": [[ str(user_data['user_id'][0]), str(user_data['food_id'][0]), str(user_data['rating'][0]) ], 
                                       [ str(user_data['user_id'][1]), str(user_data['food_id'][1]), str(user_data['rating'][1])]]
                        },        },
                    "GlobalParameters": {
        }
            }
    
        body = str.encode(json.dumps(data))
    
    except Exception as e:
        print(f"Error occurred while creating the dataframe {e}")
        return e
    
    url = 'https://ussouthcentral.services.azureml.net/workspaces/6142da2b2fe84187b8cf3862f855c550/services/37d9bed5ff9b45058d4ea12550dd5be1/execute?api-version=2.0&details=true'
    api_key = 'Rj3dtDbyciqVN/eFHnU4DKLgRlX82Fl3U0qeZiR7JoCRF81K121YHnEfaoxLv/ZgJQMnmx1Cv3JN+AMC6zQ1Sg==' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
    
    try:
    
        req = urllib.request.Request(url, body, headers) 
        response = urllib.request.urlopen(req)
    
        result = response.read()
        return result
    
    except Exception as error:
        print("The request failed with status code: " + str(error))
        return str(error)
    
def postprocessing(user_reco, allergies=[]):
    '''
    Function to remove food recommendations which have allergic
    ingidients

    Parameters
    ----------
    user_reco : pandas DataFrame
        contains the food items which the user was recommended.

    Returns
    -------
    Final 5 recommendations after removing allergic items

    '''
    
    # Things left -
    # Clean the results
    # Remove allergies
    # Add images
    
    json_string = user_reco.decode()
    data = json.loads(json_string)
    extracted_values = data["Results"]["output1"]["value"]["Values"][0]
    food_ids = extracted_values[1:]
    
    food_details = get_food_details(food_ids)
    
    final_recs = pd.DataFrame({'food_id': [],
                            'food_name': [],
                            'ingridients': [],
                            'image_url': []})
    # Removing allergic food items
    # print(allergies)
    try:
        if (len(allergies[0]) == 0):
            final_recs = food_details
        else:
            for allergy in allergies:
                # print(allergy)
                for _, row in food_details.iterrows():
                    # print(row['ingridients'])
                    if allergy.lower() in row['ingridients'].lower():
                        continue
                    else:
                        final_recs = pd.concat([final_recs, pd.DataFrame({'food_id': [row['food_id']],
                                                                    'food_name': row['food_name'],
                                                                    'ingridients': row['ingridients'],
                                                                    'image_url': row['image_url']})])
    except:
        final_recs = food_details

    return final_recs.head(3)

def writeback_to_sql_retraining(survey_response):
    # Opening database connection
    connection = pymysql.connect(host=host, user=user, password=password, db=db)
    cursor = connection.cursor()
    
    sql = """
    create table if not exists retrain_data (
        user_id int ,
        food_id varchar(255),
        rating varchar(255)
    )
    """
    cursor.execute(sql)
    
    upload_vals = survey_response.values.tolist()
    
    # Insert data into the table
    sql = "INSERT INTO retrain_data (user_id, food_id, rating) VALUES (%s, %s, %s)"
    cursor.executemany(sql, upload_vals)
    
    connection.commit()
    cursor.close()
    
def writeback_fb_data(fb_survey):
    # Opening database connection
    connection = pymysql.connect(host=host, user=user, password=password, db=db)
    cursor = connection.cursor()
    
    sql = """
    create table if not exists fb_survey (
        yes int ,
        no int
    )
    """
    cursor.execute(sql)
    
    upload_vals = fb_survey.values.tolist()
    
    # Insert data into the table
    sql = "INSERT INTO fb_survey (yes, no) VALUES (%s, %s)"
    cursor.executemany(sql, upload_vals)
    
    connection.commit()
    cursor.close()
