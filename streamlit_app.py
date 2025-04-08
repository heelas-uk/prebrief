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
        st.write(f"**ICAO Code:** {airport.get('icaoCode', 'Nil')}")
        st.write(f"**IATA Code:** {airport.get('iataCode', 'Nil')}")
        # Define mapping of type numbers to human-readable descriptions
        airport_type_map = {
            0: "Airport (civil/military)",
            1: "Glider Site",
            2: "Airfield Civil",
            3: "International Airport",
            4: "Heliport Military",
            5: "Military Aerodrome",
            6: "Ultra Light Flying Site",
            7: "Heliport Civil",
            8: "Aerodrome Closed",
            9: "Airport resp. Airfield IFR",
            10: "Airfield Water",
            11: "Landing Strip",
            12: "Agricultural Landing Strip",
            13: "Altiport"
        }

        # Get the type number
        airport_type_number = airport.get("type", None)
        # Get the description using the map
        airport_type_text = airport_type_map.get(airport_type_number, "Unknown Type")

        st.write(f"**Type:** {airport_type_text}")
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

            # Frequency type mapping
            frequency_type_map = {
                0: "Approach",
                1: "APRON",
                2: "Arrival",
                3: "Center",
                4: "CTAF",
                5: "Delivery",
                6: "Departure",
                7: "FIS",
                8: "Gliding",
                9: "Ground",
                10: "Information",
                11: "Multicom",
                12: "Unicom",
                13: "Radar",
                14: "Tower",
                15: "ATIS",
                16: "Radio",
                17: "Other",
                18: "AIRMET",
                19: "AWOS",
                20: "Lights",
                21: "VOLMET",
                22: "AFIS"
            }

            # Get the frequency type description
            freq_type_number = freq.get("type", None)
            freq_type_text = frequency_type_map.get(freq_type_number, "Unknown Type")

            st.write(f"**Type:** {freq_type_text}")


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
                # Turn direction mapping
                turn_direction_map = {
                    0: "Right",
                    1: "Left",
                    2: "Both"
                }

                # Get the turn direction description
                turn_direction_value = runway.get("turnDirection", None)
                if airport_type_number == 4  or airport_type_number == 7:
                    turn_direction_text = turn_direction_map.get(turn_direction_value, "N/A")
                else:
                    turn_direction_text = turn_direction_map.get(turn_direction_value, "Unknown perhaps you could help us by contributing at openaip.net thanks")

                st.markdown(f"**Turn Direction:** {turn_direction_text}")
            
            with col2:
                st.markdown(f"**Length:** {dim.get('length', {}).get('value', 'N/A')} m")
                st.markdown(f"**Width:** {dim.get('width', {}).get('value', 'N/A')} m")
                
                # Runway surface composition mapping
                surface_composition_map = {
                    0: "Asphalt",
                    1: "Concrete",
                    2: "Grass",
                    3: "Sand",
                    4: "Water",
                    5: "Bituminous tar or asphalt (\"earth cement\")",
                    6: "Brick",
                    7: "Macadam or tarmac (crushed rock)",
                    8: "Stone",
                    9: "Coral",
                    10: "Clay",
                    11: "Laterite",
                    12: "Gravel",
                    13: "Earth",
                    14: "Ice",
                    15: "Snow",
                    16: "Protective laminate (rubber)",
                    17: "Metal",
                    18: "Landing mat (aluminium)",
                    19: "Pierced steel planking",
                    20: "Wood",
                    21: "Non-bituminous mix",
                    22: "Unknown"
                }

                # Get surface description
                surface_type = surface.get("mainComposite", None)
                surface_text = surface_composition_map.get(surface_type, "Unknown")

                st.markdown(f"**Surface:** {surface_text}")



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
