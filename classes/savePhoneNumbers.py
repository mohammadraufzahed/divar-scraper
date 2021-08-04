"""
Select the unique and valid phone numbers and save them in the text file
"""
import random
from datetime import datetime

import psycopg2
from persiantools.jdatetime import JalaliDate
from tqdm import tqdm


def savePhoneNumbers():
    import config
    conn = psycopg2.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        dbname=config.DB_NAME
    )
    curs = conn.cursor()

    curs.execute(
        """SELECT DISTINCT phone 
        FROM information
        WHERE phone ~ '^\d+$'
        """)
    phoneNumbresDB = curs.fetchall()
    phoneNumbres = list()
    for i in phoneNumbresDB:
        phoneNumbres.append(i[0])
    del phoneNumbresDB
    counter = 0
    category_name = input("Category Name: ")
    category_name = category_name.split(' ')
    category_name = "-".join(category_name).lower()
    today_time = JalaliDate.today()
    today_time = f"{today_time.year}-{today_time.month}-{today_time.day}"
    rand_num = random.randint(0, datetime.now().microsecond)
    file_name = f"{today_time}-{category_name}-{rand_num}.txt"
    del today_time
    del category_name
    del rand_num
    with open(f"output//{file_name}", "w+", encoding="utf8") as numbersFile:
        numbersFile.flush()
        for number in tqdm(phoneNumbres):
            numbersFile.write(
                f"+98{str(number)},این یک پیام تستی است لطفا دقیق بررسی نمایید\n")
            counter += 1
        numbersFile.close()
        print(f"\n{counter} phone number saved in the {file_name} in the output folder")
    while True:
        delete_reocrds = input(
            "Do you want to delete all of the database records? (yes/no)")
        if delete_reocrds == "yes":
            curs.execute("DELETE FROM information")
            print("All of the records deleted")
            break
        elif delete_reocrds == "no":
            pass
            break
        else:
            print("Please Enter the correct answer")
            continue
    conn.commit()
    curs.close()
