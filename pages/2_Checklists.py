import streamlit as st
import datetime
import smtplib
import ssl
from email.message import EmailMessage

sender_email = st.secrets["from_email"]
password = st.secrets["email_password"]

# Blocklist of emails from Streamlit secrets (comma-separated string)
BLOCKED_EMAILS = set(email.strip().lower() for email in st.secrets.get("blocklist", "").split(",") if email.strip())

st.title("Checklists")



with st.form("walkaround_form"):
    st.subheader("Walkaround checklist (Glider)")

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
    email = st.text_input("Email address to send checklist to", "", help="Enter an email address to receive a copy of the completed checklist, this will not be retained")
    submitted = st.form_submit_button("✅ Complete Checklist")

# Show result after submission
if submitted:
    # Anti-spam: allow sending only once every 5 minutes per session
    now = datetime.datetime.now()
    last_sent = st.session_state.get("last_email_sent")
    cooldown = datetime.timedelta(minutes=5)
    if last_sent and now - last_sent < cooldown:
        st.warning("You can only send a checklist email once every 5 minutes. Please wait before trying again.")
    elif email and email.strip().lower() in BLOCKED_EMAILS:
        st.error("This email address is blocked from receiving checklist emails.")
    else:
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

        # Format checklist data for email
        def format_checklist_for_email(data):
            lines = []
            lines.append(f"Checklist completed on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            for section, items in data:
                lines.append(f"**{section}**")
                for label, checked in items:
                    mark = "✅" if checked else "❌"
                    lines.append(f"{mark} {label}")
                lines.append("")  # Blank line between sections
            # Add improved footer
            lines.append("---")
            lines.append(
                "If you did not request this email, you can safely ignore it. "
                "You are receiving this because someone (likely you) requested a checklist from prebrief.streamlit.app.\n"
                "If you believe you are receiving these emails in error or are being spammed, please contact prebrief_abuse@heelas.uk."
            )
            return "\n".join(lines)

        # Send email if address provided
        if email:
            msg = EmailMessage()
            msg["Subject"] = "Your Completed Prebrief Checklist"
            msg["From"] = sender_email
            msg["To"] = email
            msg.set_content(format_checklist_for_email(checklist_data))

            # Optional: Add a prettier HTML version
            html_lines = [
                f"<h2>Checklist completed on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</h2>"
            ]
            for section, items in checklist_data:
                html_lines.append(f"<h3>{section}</h3><ul>")
                for label, checked in items:
                    mark = "✅" if checked else "❌"
                    html_lines.append(f"<li>{mark} {label}</li>")
                html_lines.append("</ul>")
            # Add improved HTML footer
            html_lines.append("<hr>")
            html_lines.append(
                "<p style='font-size:small;color:gray;'>"
                "If you did not request this email, you can safely ignore it. "
                "You are receiving this because someone (likely you) requested a checklist from "
                "<a href='https://prebrief.streamlit.app'>prebrief.streamlit.app</a>.<br>"
                "If you believe you are receiving these emails in error or are being spammed, "
                "please contact <a href='mailto:prebrief_abuse@heelas.uk'>prebrief_abuse@heelas.uk</a>."
                "</p>"
            )
            msg.add_alternative("\n".join(html_lines), subtype="html")

            try:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.stackmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.send_message(msg)
                st.info("Checklist sent to your email!")
                st.session_state["last_email_sent"] = now  # Update last sent time
            except Exception as e:
                st.error(f"Failed to send email: {e}")


