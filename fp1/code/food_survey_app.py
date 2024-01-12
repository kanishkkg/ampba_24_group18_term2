import streamlit as st

# Function to display the introduction page
def intro_page():
    st.title("Food Recommendation Survey")
    st.write("""
    In the next few sections, we would like to ask you to rate some of the food items (of your choosing) on a scale of 1 - 10.

    The collected survey responses will be used to train a food recommendation model, by clicking next you agree to let us use your filled data for training purposes.

    Please do not share any PII information.
    """)

# Function to display the survey page
def survey_page():
    st.header("User Details")

    # Mood question
    mood = st.radio("How's your mood today?", ['Happy', 'Tired', 'Angry'])

    # Cuisine preference question
    cuisine_preferences = st.multiselect(
        "On any given day, which cuisine do you prefer?",
        ["Italian (like Pizza, Pasta etc.)", 
         "Japanese (like Sushi, Ramen etc.)", 
         "Indian (like Curry, Biryani etc.)"]
    )

    # Food allergy question
    food_allergies = st.multiselect(
        "Do you have any food allergies? If yes, then do select all the items you're allergic to",
        ["Not Allergic to any food item", "Peanut/Tree Nuts", "Seafood", "Dairy"]
    )

    if st.button('Next - Food Ratings'):
        st.session_state.page = 3

# Function to display the food ratings page
def food_ratings_page():
    st.header("Food Ratings")
    st.write("Select the food item (Food Item 1)")
    st.write("Please select any random food item which you have tasted. We will be asking for a rating in the next question")

    # Dropdown for selecting a food item
    food_item = st.selectbox(
        "Food Item",
        ["Food1", "Food2", "Food3"]
    )

    # Rating scale
    rating = st.slider("Rate the food item on a scale of 1 to 10", 1, 10)

    if st.button('Submit Rating'):
        st.success(f'You rated {food_item} a {rating} out of 10')
        # Process or store the rating here

# Main app logic
if 'page' not in st.session_state:
    st.session_state.page = 1

if st.session_state.page == 1:
    intro_page()
    if st.button("Next - User Details"):
        st.session_state.page = 2
elif st.session_state.page == 2:
    survey_page()
elif st.session_state.page == 3:
    food_ratings_page()
