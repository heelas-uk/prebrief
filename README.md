# Prebrief

A simple Streamlit app that provides preliminary airfield information.

What it can do:

Provide aerodrome information based on openAIP API and provide a map interface with a folium frontend and clickable runway and helipad information.

Provide METAR (fancy way for saying what the weather is at an airport) information from the airport or the nearest airport.

Provide the radio frequencies and runway information of an airport.

Email you a copy of a glider walkaround checklist you have completed. No you cannot spam anyone with this.

In certain countries the app also provides a link to a detailed site wich provides weather information.

AI was used for portions including spellchecking and debugging all code was reviewed by a human. 


### How to run it on your own machine

Note you will need a OPENAIP API key which can be obtained for free this willl have to be put in the st.secrets 

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run Home.py
   ```
