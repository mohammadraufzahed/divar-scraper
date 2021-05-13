from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from unidecode import unidecode
import json
import string


class ExtractData:
    # Initial the class
    def __init__(self):
        # Initial the variables
        self.__links = list()
        self.__driver = webdriver.Firefox()
        self.__counter = 0
        self.__data_list = list()
        # Extract the links
        self.__extract_links()

    # Extract the links from the JSON file
    def __extract_links(self) -> None:
        # Open the JSON file
        with open('links.json', 'r', encoding='utf8') as f:
            # Load the JSON file
            jsonLinks = json.load(f)
            # Extract the links from the JSON file
            for link in jsonLinks:
                self.__links.append(link)

    # Extract the phone numbers and append them to the list

    def extract_data(self):
        # Iterate over the links list
        for link in self.__links:
            # If it was the first link try to login to the website
            if self.__counter == 0:
                # Load the website
                self.__driver.get(link)
                # Click on the 'Get Contact' button
                self.__driver.find_element_by_css_selector(
                    'button.post-actions__get-contact').click()
                # Click on the 'Accept the rules button
                self.__driver.find_element_by_css_selector(
                    'footer.kt-modal__actions  button.kt-button--primary').click()
                # Request the phone number from the user
                user_phone_number = input("Please enter your phone number: ")
                # Send the phone number to the input
                self.__driver.find_element_by_css_selector(
                    'div.kt-textfield input').send_keys(user_phone_number)
                # Request the phone number verification code from the user
                user_verify_code = input(
                    'Please enter the verification code: ').strip()
                # Send the phone number verification code to the input
                self.__driver.find_element_by_css_selector(
                    'article.auth-modal div.kt-modal__contents input').send_keys(user_verify_code)
                # Wait 2 seconds
                time.sleep(2)
                # Grab the phone number box
                phone_number_box = self.__driver.find_element_by_css_selector(
                    'div.expandable-box')
                # Extract the phone number from the Element
                phone_number = phone_number_box.find_element_by_tag_name(
                    'a').text

                # Convert the phone numbers to English digits
                phone_number = unidecode(phone_number)
                # Select the title
                post_title = self.__driver.find_element_by_tag_name('h1').text
                # select discription
                discription = self.__driver.find_element_by_css_selector(
                    'p.kt-description-row__text').text
                # Select the tag Box
                tags = list()
                tagsBox = self.__driver.find_element_by_css_selector(
                    'div.kt-wrapper-row')
                for tag in tagsBox.find_elements_by_tag_name('a'):
                    tags.append(tag.text)
                # Append data to list
                self.__data_list.append({
                    'postTitle': post_title,
                    'posterDiscription': discription,
                    'posterPhone': phone_number,
                    'postTags': tags
                })
                # Increase the counter by one
                self.__counter += 1
            else:
                # Load the website
                self.__driver.get(link)
                # Click on the 'Get Contact' button
                self.__driver.find_element_by_css_selector(
                    'button.post-actions__get-contact').click()
                # Wait 2 seconds
                time.sleep(2)
                # Grab the phone number box
                phone_number_box = self.__driver.find_element_by_css_selector(
                    'div.expandable-box')
                # Extract the phone number from the Element
                phone_number = phone_number_box.find_element_by_tag_name(
                    'a').text
                # Convert the phone numbers to English digits
                phone_number = unidecode(phone_number)
                # Select the title
                post_title = self.__driver.find_element_by_tag_name('h1').text
                # select discription
                discription = self.__driver.find_element_by_css_selector(
                    'p.kt-description-row__text').text
                # Select the tag Box
                tags = list()
                tagsBox = self.__driver.find_element_by_css_selector(
                    'div.kt-wrapper-row')
                for tag in tagsBox.find_elements_by_tag_name('a'):
                    tags.append(tag.text)
                # Append data to list
                self.__data_list.append({
                    'postTitle': post_title,
                    'posterDiscription': discription,
                    'posterPhone': phone_number,
                    'postTags': tags
                })
        self.__driver.quit()
        print(self.__data_list)
