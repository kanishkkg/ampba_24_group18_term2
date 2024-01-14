import streamlit as st
# import sys
# sys.path.append(r"C:\Users\kanis\OneDrive - Indian School of Business\Desktop\ISB\github_codes\ampba_24_group18_term2\fp1\code\"")
import supporting_functions as sf
import pandas as pd
import time
import requests
from PIL import Image
import io

def display_image(url):
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))
    st.image(img, caption='Image', use_column_width='auto')


# Function to display the introduction page
st.title("Food Recommendation Survey")
st.write("""
This survey generates a personalized 
""")

st.header("User Details")

# Mood question
mood_options = ['Happy/Cheerful','Sad','Angry/Frustrated','Neutral/Calm/Relaxed','Tired']
mood = st.radio("How's your mood today?", mood_options)

# Cuisine preference question
cusine_options = ['Beverage','Chinese','Dessert','French','Healthy Food','Indian','Italian','Japanese','Mexican','Snack']
cuisine_preferences = st.radio("On any given day, which cuisine do you prefer?",\
                               cusine_options)

# Food allergy question
food_allergies_options = ['Not Allergic to any food item', 'Peanut/Tree Nuts',\
                          'Seafood', 'Milk', 'Egg', 'Gluten', 'Soy']
    
food_allergies = st.multiselect(
    "Do you have any food allergies? If yes, then do select all the items you're allergic to",
    food_allergies_options)
# print(food_allergies)
other_allergies = st.text_input("Other allergies (please specify)")
food_allergies += [other_allergies]

st.header("Food Ratings")
st.write("Select the food item (Food Item 1)")
st.write("Please select any random food item which you have tasted. We will be asking for a rating in the next question")

# Dropdown for selecting a food item
food_item_options = ['Chicken Minced Salad','Japanese Curry Arancini With Barley Salsa',\
                     'Baked Multigrain Murukku','Baked Namak Para','Spinach And Feta Crepes',\
                    'Mixed Berry & Banana Smoothie','Khichdi','Steam Bunny Chicken Bao',\
                    'Meat Lovers Pizza','Chicken Parmigiana With Tomato Sauce',\
                    'Caramelized Sesame Smoked Almonds','Detox Haldi Tea',\
                    'Grilled Lemon Margarita','Filter Coffee','Peri Peri Chicken Satay',\
                    'Chicken Biryani','Buldak (Hot And Spicy Chicken)',\
                    'Spicy Chicken Masala','Chilli Chicken','Chicken Tenders',\
                    'Chicken And Mushroom Lasagna','Chicken Roulade','Chicken Shami Kebab',\
                    'Fish With White Sauce','Chettinad Fish Fry','Spanish Fish Fry',\
                    'Green Cucumber Shots','Veg Fried Rice','Chicken Paella',\
                    'Vegetable Pulao','Vegetable Bruschetta','Egg And Cheddar Cheese Sandwich',\
                    'Egg In A Blanket','Kaju Katli','Mixed Vegetable Soup','Chocolate Lava Cake',\
                    'Gulab Jamun','Assorted Rice Kheer Sushi','Dry Fruit Cake',\
                    'Vegetable Manchurian','Baked Wild Berry Cheesecake','Mexican Pizza',\
                    'Fruit Cube Salad','Veg Hakka Noodles','Pasta In Cheese Sauce',\
                    'Butter Chicken','Chicken Tikka Masala','Channa Masala','Jeera Alu',\
                    'Garlic Naan','Egg Curry With Tomatoes And Cilantro','Prawn Katsu Curry',
                    'Sweet And Sour Chicken Fried Rice','Fresh Corn Tortillas']

food_item_1 = st.selectbox("Select any food item you want to rate", food_item_options, key=1).lower()
rating_1 = st.slider("Rate the food item on a scale of 1 to 10", 1, 10, 5, key=2)

food_item_2 = st.selectbox("Select any food item you want to rate", food_item_options, key=3).lower()
rating_2 = st.slider("Rate the food item on a scale of 1 to 10", 1, 10, 5, key=4)

food_item_3 = st.selectbox("Select any food item you want to rate", food_item_options, key=5).lower()
rating_3 = st.slider("Rate the food item on a scale of 1 to 10", 1, 10, 5, key=6)


# Submit button
if st.button('Submit Survey'):
    
    # Update the page state to show recommendations
    sim_user = sf.sim_user(mood, cuisine_preferences)
    food_ids = sf.get_food_id([food_item_1, food_item_2, food_item_3])

    survey_response = pd.DataFrame({'user_id': [sim_user, sim_user, sim_user],
                                    'food_id': food_ids,
                                    'rating': [rating_1, rating_2, rating_3]})
    
    response = sf.prediction(survey_response)
    output = sf.postprocessing(response, allergies = food_allergies)

    with st.spinner("Processing your responses..."):
        time.sleep(10)

    st.write("We would recommend you the following items:")
    output['food_name'] = output['food_name'].rename('Food Recommendations', inplace=True).str.title()
    for i in range(len(output)):
        st.write(output['food_name'].iloc[i])
        # output['image_url'].iloc[i].apply(display_image)
        display_image(output['image_url'].iloc[i])

    sf.writeback_to_sql_retraining(survey_response)
    
# Feedback survey section

time.sleep(15)

st.write("Did you like the recommendations?")     
thumbs_up = st.button("👍 Thumbs Up")     
thumbs_down = st.button("👎 Thumbs Down")
fb_survey = pd.DataFrame({'yes':[0],
                          'no': [0]})
     
if thumbs_up:
    fb_survey['yes'] = 1
    st.write("Great! We're glad you liked the recommendations.")
    st.write("Thanks for taking the survey, do try again!")
    # st.rerun()

 
elif thumbs_down:
    fb_survey['no'] = 1
    st.write("Sorry to hear that. We'll try to do better next time.")
    st.write("Thanks for taking the survey, do try again!")
    # st.rerun()
    
sf.writeback_fb_data(fb_survey)
        
    

             
    


