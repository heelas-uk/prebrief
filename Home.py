import streamlit as st
st.title("Prebrief")
st.badge("You as the pilot in command are responsible for the safety of the flight, this DOES NOT replace due diligence", icon=":material/emergency_home:", color="red")
st.badge("This app uses OPENAIP data, please feel free to contribute at openaip.net ", icon=":material/info:")
st.markdown("<div style='text-align: center'> This project was made to so that I could simplify my pre-flight routine. Ultimately, it probably provides too much information however this information is helpful if you are going to a new site.</div>", unsafe_allow_html=True)
with st.expander("License"):
    st.text("Data license - OpenAIP")