import streamlit as st
st.title("This is a starting point")
st.write("This is myfirts streamlit app")

name = st.text_input("What is syour name?")
if name:
    st.success(f"welcome {name} 🌟")

if st.button("click!"):
    st.balloons()
    st.write("button is clicked!") 