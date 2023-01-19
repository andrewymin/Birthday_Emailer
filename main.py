import smtplib as sm
import random
from dotenv import load_dotenv
import pandas
import datetime as dt
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

myGmail = os.getenv("GMAIL")
G_PASSWORD = os.getenv('GPASSWORD')

PORT = 587

today = dt.datetime.now()

# 1. Update the birthdays.csv
bd_df = pandas.read_csv("birthdays.csv")
bd_dict = bd_df.to_dict(orient="records")
# print(bd_dict)

# 2. Check if today matches a birthday in the birthdays.csv
for entry in bd_dict:
    if today.day == entry["day"] and today.month == entry["month"]:

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the
# person's actual name from birthdays.csv

        random_letter_num = random.randint(1, 3)
        with open(f"letter_templates/letter_{random_letter_num}.txt") as letter_file:
            birthday_letter = letter_file.read().replace("[NAME]", entry["name"])
#
        # print(birthday_letter)
# # 4. Send the letter generated in step 3 to that person's email address.
        with sm.SMTP("smtp.gmail.com", PORT) as gmail_transport:
            gmail_transport.starttls()
            gmail_transport.login(user=myGmail, password=G_PASSWORD)
            gmail_transport.sendmail(
                from_addr=myGmail,
                to_addrs=entry["email"],
                msg=f"Subject: Happy Birthday!\n\n{birthday_letter}".encode("utf8"),
            )

