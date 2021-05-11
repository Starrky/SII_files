import datetime
import os
import time
from os import listdir
from os.path import isfile, join
from time import time
import pymsteams
import smtplib
from email.message import EmailMessage
import pandas as pd
import Configs.Data as CD

# Emailing system
Notificator_card = CD.Notificator_card
EMAIL_USER = CD.EMAIL_USER
EMAIL_PASSWORD = CD.EMAIL_PASSWORD
myTeamsMessage = pymsteams.connectorcard(Notificator_card)
RECIEVER = "myitportal@pepco.eu"  # prod mail: myitportal@pepco.eu // test mail: test.support@pepco.eu

start_time = time()
dt = datetime.datetime.today()
today = dt.date()
yesterday = today - datetime.timedelta(days=1)
today = today.strftime('%Y-%m-%d')
yesterday = yesterday.strftime('%Y-%m-%d')

shops = ['240001']
no_file = []
with_file = []
no_connection = []

for shop in shops:
    shop_no = shop
    filename_1 = f'{shop_no}_{today}'
    filename_2 = f'{shop_no}_{yesterday}'
    shop = f'ES{shop}BOS01'
    shop_loc = f'//{shop}/c$/xstore/spain'
    try:
        onlyfiles = [f for f in listdir(
            shop_loc) if isfile(join(shop_loc, f))]

        for file in onlyfiles:
            if filename_1 in str(file) or filename_2 in str(file):
                if shop_no not in with_file:
                    if shop_no in no_file:
                        no_file.remove(shop_no)
                    with_file.append(shop_no)

            else:
                if shop_no not in no_file:
                    no_file.append(shop_no)
    except FileNotFoundError:
        print(f"Couldn't connect to store: {shop_no}")
        no_connection.append(shop_no)

print(f'with file: {with_file}\nno_file: {no_file}')

if len(no_file) != 0:
    print("List is not empty, creating tickets")
    for store in no_file:
        subject = f"Missing SII files for store {store}, {yesterday}"
        # Compose and send email
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_USER
        msg['To'] = RECIEVER

        html = f"Missing SII files for store {store} for date: {yesterday}"
        msg.add_alternative(html, subtype='html')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print("Email sent")

# Create tables for teams

# Table with file
df = pd.DataFrame(columns=['Store'])
df['Store'] = with_file
teams_table_p = df.to_html(index=False, justify='center')
teams_table = teams_table_p.replace('<tr>', '<tr align="center">')

# Table without file
df_2 = pd.DataFrame(columns=['Store'])
df_2['Store'] = no_file
teams_table_p_2 = df_2.to_html(index=False, justify='center')
teams_table_2 = teams_table_p_2.replace('<tr>', '<tr align="center">')

# Table with no connection
df_3 = pd.DataFrame(columns=['Store'])
df_3['Store'] = no_connection
teams_table_p_3 = df_3.to_html(index=False, justify='center')
teams_table_3 = teams_table_p_3.replace('<tr>', '<tr align="center">')

# Teams bot notification if ::
if len(with_file) != 0:
    # Files were found
    myTeamsMessage.title(f"SII Files were found for store/s on date: {yesterday}")
    myTeamsMessage.text(
        f"{teams_table}")
    myTeamsMessage.send()

if len(no_file) != 0:
    # Files were NOT found
    myTeamsMessage.title(f"SII Files were NOT found for store/s on date: {yesterday}")
    myTeamsMessage.text(
        f"{teams_table_2}")
    myTeamsMessage.send()

if len(no_connection) != 0:
    # Couldn't connect to machine/s at all
    myTeamsMessage.title(f"COULDN'T CONNECT TO MACHINE/S:")
    myTeamsMessage.text(
        f"{teams_table_3}")
    myTeamsMessage.send()


print("Process finished --- %s seconds ---" % (time() - start_time))
