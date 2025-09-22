import requests,datetime,os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

os.chdir('Bakers-Hub')
smtp_server = 'smtpout.secureserver.net'
smtp_port = 465
# Sender's email credentials
sender_email = 'support@bakershub.in'
temp_tem = 'Navkar@108'
sender_password = temp_tem
url='https://www.bakershub.in/get_user_data/'
header = {'token':'9054413199'}

today_date = datetime.date.today().strftime("%d/%m/%B")
with open("logs/email_sent_log.txt",'a') as success_file:
    success_file.write(f'\n\n### --- {today_date} --- ###\n')

def success_entries(sent,email,name):
    with open("logs/email_sent_log.txt",'a') as success_file:
            date_time = datetime.datetime.now()
            success_file.write(f'[{date_time}] -> [{sent}] - [{name}]/[{email}]\n')

data = requests.get(url,headers=header)
data = data.json()
all_data = data['all_data']
for user in all_data:
    today = datetime.date.today()
    try:
        if user['is_premium']:
            premium_end_date = str(user['premium_end_date'])
            premium_end_date = premium_end_date.split('/')
            premium_end_date = datetime.date(day=int(premium_end_date[0]),month=int(premium_end_date[1]),year=int(premium_end_date[2]))
            remaining_days = int((premium_end_date - today).days)
            if remaining_days == -1 or remaining_days == -3 or remaining_days == -5:
                # Premium Ended
                today = datetime.datetime.today().strftime("%d/%m/%Y - %H:%M")
                recipient_email = user['email']
                message = MIMEMultipart()
                message['From'] = f"Baker's Hub <{sender_email}>"
                message['To'] = recipient_email
                message['Subject'] = f"Subscription Renewal"
                body=f'''
                <h3>Hello {user['name']},</h3>
                <h3>
                We hope this message finds you well. We wanted to bring to your attention that your subscription for Baker's Hub has expired.<br><br>
                To continue accessing the exclusive benefits and services you enjoyed as a premium user, we kindly request you to renew your subscription promptly.<br><br>
                Renewing is quick and easy. Simply visit our app and follow the steps to reinstate your subscription. Don't miss out on all the features and resources available to you.<br><br>
                If you have any questions or need assistance, our dedicated customer support team is here to help. Reach out to us at support@bakershub.in or reply to this email.<br><br>
                Thank you for your past subscription and we look forward to having you back as a valued member soon!<br><br><br>
                Regards,<br>
                Baker's Hub<br>
                www.bakershub.in<br>
                </h3>
                <small>{today}</small>
                '''
                message.attach(MIMEText(body, 'html'))
                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                    # Login to the email account
                    server.login(sender_email, sender_password)
                    # Send the email
                    server.sendmail(sender_email, recipient_email, message.as_string())
                success_entries(sent='Premium Ended',email=user['email'],name=user['name'])

            elif remaining_days == 0:
                # Premium ending today
                    today = datetime.datetime.today().strftime("%d/%m/%Y - %H:%M")
                    recipient_email = user['email']
                    message = MIMEMultipart()
                    message['From'] = f"Baker's Hub <{sender_email}>"
                    message['To'] = recipient_email
                    message['Subject'] = f"Premium will end today!"
                    body=f'''
                    <h3>Hello {user['name']},</h3>
                    <h3>
                    We hope this message finds you well. We wanted to bring to your attention that your subscription for Baker's Hub will expire today.<br><br>
                    To continue accessing the exclusive benefits and services you enjoyed as a premium user, we kindly request you to renew your subscription promptly.<br><br>
                    Renewing is quick and easy. Simply visit our app and follow the steps to reinstate your subscription. Don't miss out on all the features and resources available to you.<br><br>
                    If you have any questions or need assistance, our dedicated customer support team is here to help. Reach out to us at support@bakershub.in or reply to this email.<br><br>
                    Thank you for your past subscription and we look forward to having you back as a valued member soon!<br><br><br>
                    Regards,<br>
                    Baker's Hub<br>
                    www.bakershub.in<br>
                    </h3>
                    <small>{today}</small>
                    '''
                    message.attach(MIMEText(body, 'html'))
                    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                        # Login to the email account
                        server.login(sender_email, sender_password)

                        # Send the email
                        server.sendmail(sender_email, recipient_email, message.as_string())
                    success_entries(sent='Premium Ending Today',email=user['email'],name=user['name'])

            elif remaining_days <= 5:
                if remaining_days % 2 == 0:
                    # Premium ending in 5 days or less
                    today = datetime.datetime.today().strftime("%d/%m/%Y - %H:%M")
                    recipient_email = user['email']
                    message = MIMEMultipart()
                    message['From'] = f"Baker's Hub <{sender_email}>"
                    message['To'] = recipient_email
                    message['Subject'] = f"Premium will end soon!"
                    body=f'''
                    <h3>Hello {user['name']},</h3>
                    <h3>
                    We hope this message finds you well. We wanted to bring to your attention that your subscription for Baker's Hub will expire in {remaining_days} days.<br><br>
                    To continue accessing the exclusive benefits and services you enjoyed as a premium user, we kindly request you to renew your subscription promptly.<br><br>
                    Renewing is quick and easy. Simply visit our app and follow the steps to reinstate your subscription. Don't miss out on all the features and resources available to you.<br><br>
                    If you have any questions or need assistance, our dedicated customer support team is here to help. Reach out to us at support@bakershub.in or reply to this email.<br><br>
                    Thank you for your past subscription and we look forward to having you back as a valued member soon!<br><br><br>
                    Regards,<br>
                    Baker's Hub<br>
                    www.bakershub.in<br>
                    </h3>
                    <small>{today}</small>
                    '''
                    message.attach(MIMEText(body, 'html'))
                    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                        # Login to the email account
                        server.login(sender_email, sender_password)

                        # Send the email
                        server.sendmail(sender_email, recipient_email, message.as_string())
                    success_entries(sent=f'Premium Ending in {remaining_days} days',email=user['email'],name=user['name'])

        else:
            free_end_date = str(user['free_end_date'])
            free_end_date = free_end_date.split('/')
            free_end_date = datetime.date(day=int(free_end_date[0]),month=int(free_end_date[1]),year=int(free_end_date[2]))
            remaining_days = int((free_end_date - today).days)

            if remaining_days == 13:
                today = datetime.datetime.today().strftime("%d/%m/%Y - %H:%M")
                recipient_email = user['email']
                message = MIMEMultipart()
                message['From'] = f"Baker's Hub <{sender_email}>"
                message['To'] = recipient_email
                message['Subject'] = f"Upgrade to premium"
                body=f'''
                <h3>Hello {user['name']},</h3>
                <h3>
                We hope you're enjoying your experience with Baker's Hub. We wanted to inform you that your free trial will be ending in just {remaining_days} days.<br><br>
                During your trial period, you've had access of the incredible features and benefits our premium subscription offers. Now is the perfect time to take your experience to the next level by upgrading to our premium plan.<br><br>
                With our premium subscription, you'll unlock a world of perks, including:<br>
                <ul>
                <li>Access to advanced features that enhance your productivity and efficiency.</li>
                <li>Unlimited usage of premium content, ensuring you never miss out on valuable resources.</li>
                <li>Priority customer support to address any queries or concerns promptly.</li>
                <li>Seamless integration with additional tools and services to streamline your workflow.</li>
                <li>Ad-free experience, allowing you to focus on what matters most.</li>
                </ul><br>
                Don't miss this opportunity to supercharge your Baker's Hub experience. Upgrade to premium today and continue enjoying all the benefits you've come to love.<br><br>
                To upgrade, simply visit our app and select the premium plan that suits your needs. Act now to make the most of this exclusive offer before your free trial expires.<br><br>
                If you have any questions or need assistance with the upgrade process, our dedicated support team is ready to assist you. Reach out to us at support@bakershub.in or reply to this email.<br><br>
                Thank you for choosing Baker's Hub. We appreciate your interest in our premium subscription and look forward to serving you as a valued premium member.<br><br>
                Regards,<br>
                Baker's Hub<br>
                www.bakershub.in<br>
                </h3>
                <small>{today}</small>
                '''
                message.attach(MIMEText(body, 'html'))
                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                    # Login to the email account
                    server.login(sender_email, sender_password)

                    # Send the email
                    server.sendmail(sender_email, recipient_email, message.as_string())
                success_entries(sent='14 Days Free Trial',email=user['email'],name=user['name'])

            elif remaining_days == -1 or remaining_days == -3 or remaining_days == -5:
                #Free trial ended
                today = datetime.datetime.today().strftime("%d/%m/%Y - %H:%M")
                recipient_email = user['email']
                message = MIMEMultipart()
                message['From'] = f"Baker's Hub <{sender_email}>"
                message['To'] = recipient_email
                message['Subject'] = f"Upgrade to premium"
                body=f'''
                <h3>Hello {user['name']},</h3>
                <h3>
                We hope you're enjoying your experience with Baker's Hub. We wanted to inform you that your free trial has ended.<br><br>
                During your trial period, you've had access of the incredible features and benefits our premium subscription offers. Now is the perfect time to take your experience to the next level by upgrading to our premium plan.<br><br>
                With our premium subscription, you'll unlock a world of perks, including:<br>
                <ul>
                <li>Access to advanced features that enhance your productivity and efficiency.</li>
                <li>Unlimited usage of premium content, ensuring you never miss out on valuable resources.</li>
                <li>Priority customer support to address any queries or concerns promptly.</li>
                <li>Seamless integration with additional tools and services to streamline your workflow.</li>
                <li>Ad-free experience, allowing you to focus on what matters most.</li>
                </ul><br>
                Don't miss this opportunity to supercharge your Baker's Hub experience. Upgrade to premium today and continue enjoying all the benefits you've come to love.<br><br>
                To upgrade, simply visit our app and select the premium plan that suits your needs. Act now to make the most of this exclusive offer before your free trial expires.<br><br>
                If you have any questions or need assistance with the upgrade process, our dedicated support team is ready to assist you. Reach out to us at support@bakershub.in or reply to this email.<br><br>
                Thank you for choosing Baker's Hub. We appreciate your interest in our premium subscription and look forward to serving you as a valued premium member.<br><br>
                Regards,<br>
                Baker's Hub<br>
                www.bakershub.in<br>
                </h3>
                <small>{today}</small>
                '''
                message.attach(MIMEText(body, 'html'))
                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                    # Login to the email account
                    server.login(sender_email, sender_password)

                    # Send the email
                    server.sendmail(sender_email, recipient_email, message.as_string())
                success_entries(sent='Free Trial Ended',email=user['email'],name=user['name'])

            elif remaining_days <=5 and remaining_days > 0:
                if remaining_days % 2 == 0:
                    #ending in 5 days
                    today = datetime.datetime.today().strftime("%d/%m/%Y - %H:%M")
                    recipient_email = user['email']
                    message = MIMEMultipart()
                    message['From'] = f"Baker's Hub <{sender_email}>"
                    message['To'] = recipient_email
                    message['Subject'] = f"Upgrade to premium"
                    body=f'''
                    <h3>Hello {user['name']},</h3>
                    <h3>
                    We hope you're enjoying your experience with Baker's Hub. We wanted to inform you that your free trial will be ending in just {remaining_days} days.<br><br>
                    During your trial period, you've had access of the incredible features and benefits our premium subscription offers. Now is the perfect time to take your experience to the next level by upgrading to our premium plan.<br><br>
                    With our premium subscription, you'll unlock a world of perks, including:<br>
                    <ul>
                    <li>Access to advanced features that enhance your productivity and efficiency.</li>
                    <li>Unlimited usage of premium content, ensuring you never miss out on valuable resources.</li>
                    <li>Priority customer support to address any queries or concerns promptly.</li>
                    <li>Seamless integration with additional tools and services to streamline your workflow.</li>
                    <li>Ad-free experience, allowing you to focus on what matters most.</li>
                    </ul><br>
                    Don't miss this opportunity to supercharge your Baker's Hub experience. Upgrade to premium today and continue enjoying all the benefits you've come to love.<br><br>
                    To upgrade, simply visit our app and select the premium plan that suits your needs. Act now to make the most of this exclusive offer before your free trial expires.<br><br>
                    If you have any questions or need assistance with the upgrade process, our dedicated support team is ready to assist you. Reach out to us at support@bakershub.in or reply to this email.<br><br>
                    Thank you for choosing Baker's Hub. We appreciate your interest in our premium subscription and look forward to serving you as a valued premium member.<br><br>
                    Regards,<br>
                    Baker's Hub<br>
                    www.bakershub.in<br>
                    </h3>
                    <small>{today}</small>
                    '''
                    message.attach(MIMEText(body, 'html'))
                    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                        # Login to the email account
                        server.login(sender_email, sender_password)

                        # Send the email
                        server.sendmail(sender_email, recipient_email, message.as_string())
                    success_entries(sent=f'Free Trial Ending in {remaining_days} days',email=user['email'],name=user['name'])

    except Exception as error:
        with open("logs/email_error_log.txt",'a') as error_file:
            date_time = datetime.datetime.now()
            error_file.write(f'[{date_time}] -> [{user["user_id"]}/{user["name"]}] : [{url}] [{error}] - At Line {(error.__traceback__).tb_lineno} - [{user["email"]}]\n')
            # File name - tb_frame.f_code.co_filename