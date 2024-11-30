import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import os

# Define your email sender and receiver
sender_email = os.environ['SenderEmail']
receiver_email = os.environ['ReceiverEmail']
password = os.environ['EmailPass']

async def send_property_email_update(propertyString):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "New property added!"
    msg.attach(MIMEText(str(propertyString), 'plain'))

    # Connect to the Gmail SMTP server and send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Start TLS for security
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        logging.info("Email sent successfully!")
    except Exception as e:
        logging.info(f"Error: {e}")
    finally:
        server.quit()

