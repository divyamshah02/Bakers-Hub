import datetime,pytz,os
os.chdir('Bakers-Hub')

def convert_to_ist(utc_time):
    utc = pytz.timezone('UTC')
    ist = pytz.timezone('Asia/Kolkata')

    utc_dt = utc.localize(utc_time)
    ist_dt = utc_dt.astimezone(ist)

    return ist_dt

utc_time = datetime.datetime.now()
utc_time = utc_time - datetime.timedelta(days=1)
# Convert UTC time to IST
ist_time = convert_to_ist(utc_time)
today = ist_time.strftime("%d %B, %Y")
with open('logs/access_log.txt','r') as access_file:
    today_data = access_file.readlines()

with open('logs/all_access_log.txt','r') as all_access_file_read:
    all_data = all_access_file_read.readlines()

with open('logs/all_access_log.txt','w') as all_access_file:
    all_access_file.write(f'## {today} ##\n')
    for data in today_data:
        all_access_file.write(data)

    all_access_file.write('\n\n')
    for a_data in all_data:
        all_access_file.write(a_data)

with open('logs/access_log.txt','w') as erase_file:
    erase_file.write('')