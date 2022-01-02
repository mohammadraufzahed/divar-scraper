import json
from time import sleep

import psycopg2
from colorama import Fore
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from tqdm import tqdm
from unidecode import unidecode


class ExtractData:
    # Initial the class
    def __init__(self):
        # If this instance of the class created, import the config file
        import config
        self.DB_HOST = config.DB_HOST
        self.DB_NAME = config.DB_NAME
        self.DB_USER = config.DB_USER
        self.DB_PORT = config.DB_PORT
        self.DB_PASSWORD = config.DB_PASSWORD
        # Initial the variables
        self.__links = list()
        # Firefox Options
        options = Options()
        options.headless = True
        self.__driver = webdriver.Firefox(
            options=options, executable_path="binary/geckodriver")
        self.__counter = 0
        self.__data_list = list()
        # Extract the links
        self.__extract_links()

    # Extract the links from the JSON file
    def __extract_links(self) -> None:
        # Open the JSON file
        with open('links.json', 'r', encoding='utf8') as f:
            # Load the JSON file
            json_links = json.load(f)
            # Extract the links from the JSON file
            for link in json_links:
                self.__links.append(link)

    # Extract the phone numbers and append them to the list

    def extract_data(self):
        # Iterate over the links list
        for link in tqdm(self.__links):
            # If it was the first link try to login to the website
            if self.__counter == 0:
                # First poster
                self.__first_poster_extract(link)
            else:
                self.__poster_extract(link)
        self.__driver.quit()
        self.__save_data()
        print("Data saved on the database")

    # Save the data in the json file
    def __save_data(self: object) -> None:
        conn = psycopg2.connect(
            host=self.DB_HOST,
            port=self.DB_PORT,
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            dbname=self.DB_NAME
        )
        curs = conn.cursor()
        for data in self.__data_list:
            sql = f"""
            INSERT INTO information(title, description, phone, tags)
            VALUES (
            '{data['postTitle']}',
            '{data['posterDiscription']}',
            '{data['posterPhone']}',
            '{data['postTags']}'
            )
            """
            curs.execute(sql)

        conn.commit()
        curs.close()
        conn.close()

    # Extract first poster with login
    def __first_poster_extract(self: object, link: str) -> None:
        # Load the website
        self.__driver.get(link)
        try:
            # Click on the 'Get Contact' button
            self.__driver.find_element_by_css_selector(
                'button.post-actions__get-contact').click()
            # Click on the 'Accept the rules button
            self.__driver.find_element_by_css_selector(
                'footer.kt-modal__actions  button.kt-button--primary').click()
            # Request the phone number from the user
            user_phone_number = input(
                "Please enter your phone number: ")
            # Send the phone number to the input
            self.__driver.find_element_by_css_selector(
                'div.kt-textfield input').send_keys(user_phone_number)
            # Request the phone number verification code from the user
            user_verify_code = input(
                'Please enter the verification code: ').strip()
            print("\n")
            # Send the phone number verification code to the input
            self.__driver.find_element_by_css_selector(
                'article.auth-modal div.kt-modal__contents input').send_keys(user_verify_code)
            # Wait 2 seconds
            sleep(2)
            # Grab the phone number box
            phone_number_box = self.__driver.find_element_by_css_selector(
                'div.expandable-box')
            # Extract the phone number from the Element
            phone_number = phone_number_box.find_element_by_tag_name(
                'a').text

            # Convert the phone numbers to English digits
            phone_number = unidecode(phone_number)
            # Select the title
            post_title = self.__driver.find_element_by_tag_name(
                'h1').text
            # select discription
            discription = self.__driver.find_element_by_css_selector(
                'p.kt-description-row__text').text
            # Delete the escape characters
            discription = discription.translate(
                {ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
            discription = discription.translate(
                {ord(c): " " for c in "'"})
            discription = discription.translate(
                {ord(c): " " for c in '"'})
            # Select the tag Box
            tags = list()
            tags_box = self.__driver.find_element_by_css_selector(
                'div.kt-wrapper-row')
            for tag in tags_box.find_elements_by_tag_name('a'):
                tags.append(tag.text)
            # Append data to list
            self.__data_list.append({
                'postTitle': post_title,
                'posterDiscription': discription,
                'posterPhone': phone_number,
                'postTags': ' '.join(tags)
            })
            # Increase the counter by one
            self.__counter += 1
        except NoSuchElementException:
            print(f'{Fore.RED}ELement does not exists{Fore.WHITE}')

    # Extract the posters
    def __poster_extract(self: object, link: str) -> None:
        try:
            # Load the website
            self.__driver.get(link)
            # Click on the 'Get Contact' button
            self.__driver.find_element_by_css_selector(
                'button.post-actions__get-contact').click()
            # Wait 2 seconds
            sleep(2)
            # Grab the phone number box
            phone_number_box = self.__driver.find_element_by_css_selector(
                'div.expandable-box')
            # Extract the phone number from the Element
            phone_number = phone_number_box.find_element_by_tag_name(
                'a').text
            # Convert the phone numbers to English digits
            phone_number = unidecode(phone_number)
            # Select the title
            post_title = self.__driver.find_element_by_tag_name(
                'h1').text
            # select discription
            discription = self.__driver.find_element_by_css_selector(
                'p.kt-description-row__text').text
            # Delete the escape characters
            discription = discription.translate(
                {ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
            discription = discription.translate(
                {ord(c): " " for c in "'"})
            discription = discription.translate(
                {ord(c): " " for c in '"'})
            # Select the tag Box
            tags = list()
            tags_box = self.__driver.find_element_by_css_selector(
                'div.kt-wrapper-row')
            for tag in tags_box.find_elements_by_tag_name('a'):
                tags.append(tag.text)
            # Append data to list
            self.__data_list.append({
                'postTitle': post_title,
                'posterDiscription': discription,
                'posterPhone': phone_number,
                'postTags': ' '.join(tags)
            })
        except NoSuchElementException:
            print(f'{Fore.RED}ELement does not exists{Fore.WHITE}')
