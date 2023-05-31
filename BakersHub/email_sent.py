import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SendMailOTP:
    def __init__(self):
        # SMTP server and port for GoDaddy
        self.smtp_server = 'smtpout.secureserver.net'
        self.smtp_port = 465
        # Sender's email credentials
        self.sender_email = 'support@bakershub.in'
        self.sender_password = 'Navkar@108'
        
        
    def send(self,email,otp):
        # Recipient email address
        self.recipient_email = email

        # Email subject and content
        self.subject = 'OTP - Verification for pasword change'
        self.username = "Baker's Hub Support"
        self.body = f'<h3><u>{otp}</u> is your otp to change password.</h3>'

        try:
            # Create the email message
            self.message = MIMEMultipart()
            self.message['From'] = f'{self.username} <{self.sender_email}>'
            self.message['To'] = self.recipient_email
            self.message['Subject'] = self.subject
            self.message.attach(MIMEText(self.body, 'html'))

            # Set up the SMTP connection and send the email
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                # Login to the email account
                server.login(self.sender_email, self.sender_password)

                # Send the email
                server.sendmail(self.sender_email, self.recipient_email, self.message.as_string())
            
            return True
                
        except:
            return False
