import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime as dt

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



class SendMail:
    def __init__(self):
        # SMTP server and port for GoDaddy
        self.smtp_server = 'smtpout.secureserver.net'
        self.smtp_port = 465
        # Sender's email credentials
        self.sender_email = 'support@bakershub.in'
        temp_tem = 'Navkar@108'
        self.sender_password = temp_tem


    def send_otp(self,email,otp):
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

    def send_support(self,data):
        try:
            today = dt.datetime.today().strftime("%d/%m/%Y - %H:%M")
            self.recipient_email = self.sender_email
            self.message = MIMEMultipart()
            self.message['From'] = f'Support <{self.sender_email}>'
            self.message['To'] = self.recipient_email
            self.message['Subject'] = data['subject']
            self.body = f'''<h3>
From Email: {data['email']}</h3>
<br><h3>User Data :<br><h4>
Ticket Number: {data['tid']}<br>
Email: {data['user_mail']}<br>
User Id: {data['user_id']}<br>
Name: {data['user_name']}<br>
Premium: {data['is_premium']} - {data['ending_on']}<br>
Profile Link: www.bakershub.in/admin/user_0/userprofile/{data['user_no']} </h4>
<h4>Issue:<br>{data['problem']}</h4>
<h5>{today}</h5>
            '''
            self.message.attach(MIMEText(self.body, 'html'))
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                    # Login to the email account
                    server.login(self.sender_email, self.sender_password)

                    # Send the email
                    server.sendmail(self.sender_email, self.recipient_email, self.message.as_string())
            return today
        except:
            return None

    def support_user(self,data):
            try:
                today = dt.datetime.today().strftime("%d/%m/%Y - %H:%M")
                self.recipient_email = data['email']
                self.message = MIMEMultipart()
                self.message['From'] = f"Baker's Hub Support <{self.sender_email}>"
                self.message['To'] = self.recipient_email
                self.message['Subject'] = f"[##{data['tid']}##] Support Request Recieved"
                self.body=f'''
                <h3>Hello {data['user_name']},</h3>
                <h4>
                Thank you for reaching out,<br><br>
                Your ticket has been created for Issue: <br>
                <u>{data['subject']}</u><br>
                and has been allocated ticket ID <u>{data['tid']}</u>.<br>
                We strive to solve your problem as quickly as possible.<br><br>
                Regards,<br>
                Baker's Hub<br>
                www.bakershub.in<br></h4>
                <small>{today}</small>
                '''
                self.message.attach(MIMEText(self.body, 'html'))
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                    # Login to the email account
                    server.login(self.sender_email, self.sender_password)

                    # Send the email
                    server.sendmail(self.sender_email, self.recipient_email, self.message.as_string())
                return True
            except:
                return False

def trail():
    import smtplib
    to = 'divyamshah1234@gmail.com'
    user = 'support@sweetmist.in'#your secureserver mail_id(godaddy)
    pwd = 'Navkar@108'

    smtpserver = smtplib.SMTP("smtpout.asia.secureserver.net",80)
    smtpserver.ehlo
    smtpserver.login(user, pwd)
    header = 'To:' + to + '\n' + 'From: ' + user + '\n' + 'Subject:testing \n'
    print("header")
    msg = header + '\n Thank you for registring.\n\n'
    smtpserver.sendmail(user, to, msg)
    print('done!')
    smtpserver.close()
