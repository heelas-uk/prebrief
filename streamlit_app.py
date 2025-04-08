import streamlit as st
import requests
import pandas as pd
st.title("Prebrief")
st.badge("You as the pilot in command are responsible for the safety of the flight, this DOES NOT replace due dillegence", icon=":material/emergency_home:", color="red")
st.badge("This app uses OPENAIP data, please feel free to contribute at openaip.net ", icon=":material/info:")
search = st.text_input("Search for an airport", "UPV")

# API call
url = 'https://api.core.openaip.net/api/airports?page=1&limit=1000&sortDesc=true&country=GB&searchOptLwc=true&search=' + search
headers = {
    'accept': 'application/json',
    'x-openaip-api-key': st.secrets["key"]
}
response = requests.get(url, headers=headers)
data = response.json()

# Airport data
if data["items"]:
    airport = data["items"][0]

    st.markdown("---")
    st.header(f"✈️ {airport['name']} ({airport.get('icaoCode', 'N/A')})")

    # General Info
    st.subheader("📍 General Info")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Country:** {airport.get('country', 'N/A')}")
        st.write(f"**ICAO Code:** {airport.get('icaoCode', 'N/A')}")
        st.write(f"**IATA Code:** {airport.get('iataCode', 'N/A')}")
        st.write(f"**Type:** {airport.get('type', 'N/A')}")
        st.write(f"**Magnetic Declination:** {airport.get('magneticDeclination', 'N/A')}°")
    with col2:
        st.write(f"**Private:** {'✅ Yes' if airport.get('private') else '❌ No'}")
        st.write(f"**PPR Required:** {'✅ Yes' if airport.get('ppr') else '❌ No'}")
        st.write(f"**Skydive Activity:** {'✅ Yes' if airport.get('skydiveActivity') else '❌ No'}")
        st.write(f"**Winch Only:** {'✅ Yes' if airport.get('winchOnly') else '❌ No'}")

    st.markdown(f"📝 **Remarks:** {airport.get('remarks', 'None')}")

    # Map
    coords = airport.get("geometry", {}).get("coordinates", [None, None])
    if coords and coords[0] and coords[1]:
        st.subheader("🗺️ Location")
        st.map(pd.DataFrame({'lat': [coords[1]], 'lon': [coords[0]]}))

    # Frequencies
    st.subheader("📡 Frequencies")
    for freq in airport.get("frequencies", []):
        with st.expander(freq.get("name", "Unnamed Frequency")):
            st.write(f"**Value:** {freq['value']} MHz")
            st.write(f"**Type:** {freq['type']}")
            st.write(f"**Public Use:** {'Yes' if freq.get('publicUse') else 'No'}")
            if freq.get("remarks"):
                st.write(f"**Remarks:** {freq['remarks']}")

else:
    st.warning("No airport data found.")

# Runways
st.subheader("🛬 Runways")

runways = airport.get("runways", [])
if runways:
    for runway in runways:
        with st.expander(f"Runway {runway.get('designator')}"):
            dim = runway.get("dimension", {})
            tora = runway.get("declaredDistance", {}).get("tora", {})
            lda = runway.get("declaredDistance", {}).get("lda", {})
            surface = runway.get("surface", {})

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**True Heading:** {runway.get('trueHeading', 'N/A')}°")
                st.markdown(f"**Aligned True North:** {'✅ Yes' if runway.get('alignedTrueNorth') else '❌ No'}")
                st.markdown(f"**Turn Direction:** {runway.get('turnDirection', 'N/A')}")
            
            with col2:
                st.markdown(f"**Length:** {dim.get('length', {}).get('value', 'N/A')} m")
                st.markdown(f"**Width:** {dim.get('width', {}).get('value', 'N/A')} m")
                st.markdown(f"**Surface:** {surface.get('mainComposite', 'N/A')}")

            with col3:
                st.markdown(f"**TORA:** {tora.get('value', 'N/A')} m")
                st.markdown(f"**LDA:** {lda.get('value', 'N/A')} m")
                st.markdown(f"**Main Runway:** {'✅ Yes' if runway.get('mainRunway') else '❌ No'}")

            st.markdown("---")
            col4, col5 = st.columns(2)
            with col4:
                st.markdown(f"**Take Off Only:** {'✅ Yes' if runway.get('takeOffOnly') else '❌ No'}")
            with col5:
                st.markdown(f"**Landing Only:** {'✅ Yes' if runway.get('landingOnly') else '❌ No'}")
else:
    st.info("No runway data available.")
