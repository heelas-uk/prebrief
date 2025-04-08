import streamlit as st
import requests
import pandas as pd
import re
import datetime

st.title("Prebrief")
st.badge("You as the pilot in command are responsible for the safety of the flight, this DOES NOT replace due diligence", icon=":material/emergency_home:", color="red")
st.badge("This app uses OPENAIP data, please feel free to contribute at openaip.net ", icon=":material/info:")
search = st.text_input("Search for an airport", "UPV")

# API call to get airport data
url = f'https://api.core.openaip.net/api/airports?page=1&limit=1000&sortDesc=true&country=GB&searchOptLwc=true&search={search}'
headers = {
    'accept': 'application/json',
    'x-openaip-api-key': st.secrets["key"]
}
response = requests.get(url, headers=headers)
data = response.json()

# Function to get METAR data
API_KEY = st.secrets["weather"]

def get_metar(icao):
    headers = {"X-API-Key": API_KEY}
    primary_url = f"https://api.checkwx.com/metar/{icao}/decoded"
    response = requests.get(primary_url, headers=headers).json()
    if response.get("data"):
        return response
    fallback_url = f"https://api.checkwx.com/metar/{icao}/nearest/decoded"
    return requests.get(fallback_url, headers=headers).json()

def decode_clouds_from_metar(raw_metar):
    cloud_amounts = {
        'FEW': 'Few (1–2 oktas)',
        'SCT': 'Scattered (3–4 oktas)',
        'BKN': 'Broken (5–7 oktas)',
        'OVC': 'Overcast (8 oktas)',
        'NSC': 'No significant cloud',
        'VV': 'Vertical visibility (sky obscured)'
    }

    cloud_types = {
        'TCU': 'Towering Cumulus',
        'CB': 'Cumulonimbus'
    }

    cloud_emojis = {
        'FEW': '🌤️',
        'SCT': '⛅',
        'BKN': '🌥️',
        'OVC': '☁️',
        'NSC': '🌞',
        'VV': '🌫️'
    }

    type_emojis = {
        'TCU': '⛰️',
        'CB': '⛈️'
    }

    if 'CAVOK' in raw_metar:
        return ['🌞 CAVOK: Clear skies, visibility OK']
    
    if 'NCD' in raw_metar:
        return ['🌤️ No significant clouds detected']

    cloud_groups = re.findall(r'\b(FEW|SCT|BKN|OVC|NSC|VV)(\d{3})(CB|TCU)?\b', raw_metar)

    decoded_clouds = []
    for amount, height, ctype in cloud_groups:
        amount_desc = cloud_amounts.get(amount, amount)
        height_ft = int(height) * 100
        base_emoji = cloud_emojis.get(amount, '☁️')
        type_desc = cloud_types.get(ctype, '')
        type_emoji = type_emojis.get(ctype, '')

        cloud_str = f"{base_emoji} {amount_desc} at {height_ft} ft"
        if ctype:
            cloud_str += f" ({type_desc}) {type_emoji}"
        decoded_clouds.append(cloud_str)

    return decoded_clouds

def get_wind_emoji(speed):
    if speed is None:
        return "❓"
    if speed < 5:
        return "🍃"
    elif speed < 15:
        return "🌬️"
    else:
        return "💨"

def get_temp_emoji(temp):
    if temp is None:
        return "❓"
    if temp < 0:
        return "❄️"
    elif temp < 15:
        return "🫕"
    elif temp < 25:
        return "🌤️"
    else:
        return "🔥"

def extract_obs_time(raw_metar):
    # Regex pattern to extract the observation time (hhmmZ format)
    match = re.search(r'\d{4}Z', raw_metar)
    if match:
        # Extract the time (hhmmZ), remove the 'Z' and format it
        obs_time = match.group(0)[:-1]  # Remove 'Z' (e.g., '082050' -> '082050')
        # Convert to 24-hour format time (hh:mm UTC)
        formatted_time = datetime.datetime.strptime(obs_time, '%H%M').strftime('%H:%M UTC')
        return formatted_time
    return "N/A"  # Return "N/A" if no match is found

# Display airport data and METAR details
if data["items"]:
    airport = data["items"][0]

    st.markdown("---")
    st.header(f"✈️ {airport['name']} ({airport.get('icaoCode', '')})")

    # General Info
    st.subheader("📍 General Info")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Country:** {airport.get('country', 'N/A')}")
        st.write(f"**ICAO Code:** {airport.get('icaoCode', 'Nil')}")
        st.write(f"**IATA Code:** {airport.get('iataCode', 'Nil')}")
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
        airport_type_number = airport.get("type", None)
        airport_type_text = airport_type_map.get(airport_type_number, "Unknown Type")
        st.write(f"**Type:** {airport_type_text}")
    with col2:
        st.write(f"**Private:** {'✅ Yes' if airport.get('private') else '❌ No'}")
        st.write(f"**PPR Required:** {'✅ Yes' if airport.get('ppr') else '❌ No'}")
        st.write(f"**Skydive Activity:** {'✅ Yes' if airport.get('skydiveActivity') else '❌ No'}")
        st.write(f"**Winch Only:** {'✅ Yes' if airport.get('winchOnly') else '❌ No'}")

    st.markdown(f"📝 **Remarks:** {airport.get('remarks', 'None')}")

    # METAR Data
    icao_code = airport.get('icaoCode', '')
    if icao_code:
        metar_data = get_metar(icao_code)
        if metar_data and "data" in metar_data:
            metar = metar_data["data"][0]
            st.subheader("🌤️ METAR Report")
            st.markdown(f"`{metar.get('raw_text', 'N/A')}`")

            col1, col2, col3 = st.columns(3)

            # Temperature
            temp = metar.get("temperature", {}).get("celsius")
            with col1:
                st.metric(f"{get_temp_emoji(temp)} Temperature", f"{temp} °C" if temp is not None else "N/A")

            # Wind
            wind = metar.get("wind", {})
            wind_speed = wind.get("speed_kts")
            wind_dir = wind.get("degrees")
            with col2:
                st.metric(f"{get_wind_emoji(wind_speed)} Wind", f"{wind_dir}° at {wind_speed} kt" if wind_speed and wind_dir else "N/A")
            
            # Visibility
            visibility = metar.get("visibility", {}).get("meters")
            with col3:
                st.metric("👁️ Visibility", f"{visibility} m" if visibility else "N/A")

            # Clouds
            col4 = st.columns(1)
            with col4[0]:
                decoded_clouds = decode_clouds_from_metar(metar.get("raw_text", ""))
                for cloud in decoded_clouds:
                    st.metric("Clouds", cloud)

            # Observation Time
            obs_time = extract_obs_time(metar.get("raw_text", ""))
            st.markdown(f"🕒 Observation Time: {obs_time}")

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
            with col2:
                st.markdown(f"**Length:** {dim.get('length', {}).get('value', 'N/A')} m")
            with col3:
                st.markdown(f"**TORA:** {tora.get('value', 'N/A')} m")

else:
    st.info("No runway data available.")
