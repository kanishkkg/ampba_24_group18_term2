import streamlit as st

# Streamlit webpage title
st.title('Sample Survey')

# Start of the survey
st.header('Please fill out this survey')

# Sample questions
name = st.text_input('What is your name?')
age = st.slider('How old are you?', 0, 100, 25)
favorite_color = st.selectbox('What is your favorite color?', 
                              ['Red', 'Green', 'Blue', 'Yellow', 'Other'])
feedback = st.text_area('Do you have any suggestions for our services?')

# Submit button
if st.button('Submit'):
    st.success('Survey submitted successfully!')
    # You can process the data here or store it

# Display the input data (optional)
st.write('Your Input:')
st.write('Name:', name)
st.write('Age:', age)
st.write('Favorite Color:', favorite_color)
st.write('Feedback:', feedback)
