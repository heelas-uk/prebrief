import streamlit as st
import datetime

st.title("Checklists")

with st.form("walkaround_form"):
    st.subheader("Walkaround checklist")

    st.write("### Airframe")
    airframe_1 = st.checkbox("Check external damage to aircraft", help="Start at the nose and move clockwise")
    airframe_2 = st.checkbox("Ensure a DI and positive control check has been completed", help="This does not require the physical book a brief will suffice")
    airframe_3 = st.checkbox("Ensure that noted defects will not affect the safety of the flight or have suitable mitigation")

    st.write("### Ballast")
    ballast_1 = st.checkbox("Check ballast weight is correct")
    ballast_2 = st.checkbox("Check ballast is secure and correctly positioned")
    ballast_3 = st.checkbox("Check ballast placard and that your intended loading is within limits")

    st.write("### Controls")
    controls_1 = st.checkbox("Move all controls to the fullest extents and check for full and free movement")
    controls_2 = st.checkbox("**Visually check there is movement**")

    st.write("### Dolly")
    dolly_1 = st.checkbox("Remove all tail, wing dollies, tow bars, and control locks")

    st.write("### Environment/Eventualities")
    env_1 = st.checkbox("Assess the weather or the difference since you last flew")
    env_2 = st.checkbox("Mentally prepare for a launch failure given the environment")
    env_3 = st.checkbox("Scan above for other aircraft that could later pose a hazard")

    # Submit button at the bottom
    submitted = st.form_submit_button("✅ Complete Checklist")

# Show result after submission
if submitted:
    st.success("Checklist complete ✅")
    # Gather checklist data
    checklist_data = [
        ("Airframe", [
            ("Check external damage to aircraft", airframe_1),
            ("Ensure a DI and positive control check has been completed", airframe_2),
            ("Ensure that noted defects will not affect the safety of the flight or have suitable mitigation", airframe_3),
        ]),
        ("Ballast", [
            ("Check ballast weight is correct", ballast_1),
            ("Check ballast is secure and correctly positioned", ballast_2),
            ("Check ballast placard and that your intended loading is within limits", ballast_3),
        ]),
        ("Controls", [
            ("Move all controls to the fullest extents and check for full and free movement", controls_1),
            ("Visually check there is movement", controls_2),
        ]),
        ("Dolly", [
            ("Remove all tail, wing dollies, tow bars, and control locks", dolly_1),
        ]),
        ("Environment/Eventualities", [
            ("Assess the weather or the difference since you last flew", env_1),
            ("Mentally prepare for a launch failure given the environment", env_2),
            ("Scan above for other aircraft that could later pose a hazard", env_3),
        ]),
    ]

