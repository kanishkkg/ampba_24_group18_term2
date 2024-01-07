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
    mood = st.radio("How's your mood today?", ['Happy', 'Tired', 'Angry'])
    # You can add more questions here

    if st.button('Submit Survey'):
        st.success('Survey submitted successfully!')
        # Process or store the survey data here

# Main app logic
if 'page' not in st.session_state:
    st.session_state.page = 1

if st.session_state.page == 1:
    intro_page()
    if st.button("Next"):
        st.session_state.page = 2
elif st.session_state.page == 2:
    survey_page()
