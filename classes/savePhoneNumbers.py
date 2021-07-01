"""
Select the unique and valid phone numbers and save them in the text file
"""
import psycopg2
import config


def savePhoneNumbers():
    conn = psycopg2.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        dbname=config.DB_NAME
    )
    curs = conn.cursor()

    curs.execute(
        "SELECT DISTINCT phone FROM information WHERE phone ~ '^\d+$'")
    phoneNumbresDB = curs.fetchall()
    phoneNumbres = list()
    for i in phoneNumbresDB:
        phoneNumbres.append(i[0])
    del phoneNumbresDB
    counter = 0
    with open("numbers.txt", "w+", encoding="utf8") as numbersFile:
        numbersFile.flush()
        for number in phoneNumbres:
            numbersFile.write(f"{str(number)}\n")
            counter += 1
        numbersFile.close()
        print(f"{counter} phone number saved in the numbers.txt")
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
