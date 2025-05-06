import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to send email
def send_email(recipient, subject, body):
    # Gmail Login Credentials
    sender_email = "classytamil@gmail.com"
    sender_password = "t@Mil#2k4"  # Use the generated App Password here

    # SMTP Server setup
    smtp_server = "smtp.gmail.com"
    smtp_port = 465  # SSL Port

    # Prepare the email content
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the Gmail SMTP server
        print("Attempting to login...")
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            print("Login successful!")
            server.sendmail(sender_email, recipient, msg.as_string())
            print("Email sent successfully!")
    except smtplib.SMTPAuthenticationError as e:
        print("SMTP Authentication Error:")
        print("Check if the username, password, or app password is correct.")
        print(f"Error: {e}")
    except smtplib.SMTPConnectError as e:
        print("SMTP Connection Error:")
        print("Could not connect to the SMTP server. Please check your connection and settings.")
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Example usage
send_email("tamil1004k@gmail.com", "Verification Code", "Your verification code is: 123456")
