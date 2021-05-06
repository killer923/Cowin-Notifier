import datetime
import time
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#############################################
####  CONFIGURE THIS PART ###################
#############################################
MIN_ALERT_SEATS = 4
MIN_AGE = 18   # Use `18` for 18-45 and `45` for 45+ 
PINCODE = 110001  # Enter pincode of district
NOTIFY_TO = "@gmail.com"   # Email address to send alert to  
RUN_FREQUENCY_IN_SEC = 60 * 60   # 15 min . Please don't use very low values
FROM = "@outlook.com" # use outlook.com email only
PASS = ""
#############################################
#############################################

while True:
    print("=====================================================")
    print("=====================================================")
    print("=====================================================")
    print("Sleeping for " + str(RUN_FREQUENCY_IN_SEC) + " seconds....")
    print("=====================================================")
    print("=====================================================")
    print("=====================================================")
    time.sleep(RUN_FREQUENCY_IN_SEC)
    date = datetime.datetime.today().strftime('%d-%m-%Y')
    url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=' + str(PINCODE) + '&date=' + date
    available_centers = set()
    print("Fetching : "+ url)

    # create session
    common_headers = {
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'origin': 'https://www.cowin.gov.in',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.cowin.gov.in/',
        'accept-language': 'en-GB,en;q=0.9'

    }
    curSession = requests.Session()
    curSession.headers.update(common_headers)
    curSession.get('https://www.cowin.gov.in/home')

    # Find list
    response = curSession.get(url)
    data = response.json()
    for center in data['centers']:
        for session in center['sessions']:
            if session['min_age_limit'] == MIN_AGE:
                print(session)
                if session['available_capacity'] > MIN_ALERT_SEATS:
                    available_centers.add(center['name'])
    print("Alerting for : " + str(available_centers))

    if not available_centers:
        continue

    # Alert
    # set up the SMTP server
    server = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    server.starttls()
    server.login(FROM, PASS)
    server.ehlo()
    msg = MIMEMultipart()

    sender = FROM
    subject = "AVAILABLE COWIN SLOTS!!!"
    msg_text = "Available Centers : " + str(available_centers)

    msg['From'] = sender
    msg['To'] = NOTIFY_TO
    msg['Subject'] = subject
    msg.attach(MIMEText(msg_text, 'plain'))
    server.send_message(msg)
    print('sending email to outlook')
    server.quit()





