import subprocess,datetime,os,pytz

def convert_to_ist(utc_time):
    utc = pytz.timezone('UTC')
    ist = pytz.timezone('Asia/Kolkata')

    utc_dt = utc.localize(utc_time)
    ist_dt = utc_dt.astimezone(ist)

    return ist_dt

def create_database_backup():
    backup_file = 'backup.json'
    command = f'python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > {backup_file}'
    os.chdir('Bakers-Hub')

    try:
        subprocess.run(command, shell=True, check=True)
        with open('logs/backup_log.txt','a') as backup_log:
            utc_time = datetime.datetime.now()
            # Convert UTC time to IST
            ist_time = convert_to_ist(utc_time)
            date_time = ist_time.strftime("%d/%m/%Y - %H:%M")
            backup_log.write(f"    [{date_time}]-> Database backup created successfully.\n")
    except subprocess.CalledProcessError as e:
        with open('logs/backup_log.txt','a') as backup_log:
            utc_time = datetime.datetime.now()
            # Convert UTC time to IST
            ist_time = convert_to_ist(utc_time)
            date_time = ist_time.strftime("%d/%m/%Y - %H:%M")
            backup_log.write(f"xxxx[{date_time}]-> Backup creation failed. Error: {e}.\n")

create_database_backup()