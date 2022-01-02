import json
from time import sleep

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from url_normalize import url_normalize


class GetPosterLink:
    def __init__(self, timeout):
        # Firefox Options
        options = Options()
        options.headless = True
        # Initial the browser
        self.__driver = webdriver.Firefox(
            options=options, executable_path="binary/geckodriver")
        self.__category_link = input("Input the category link: ")
        self.__driver.get(self.__category_link)
        #  Initial the list of links
        self.__links = list()
        # Initial the timeout time
        self.__timeout = timeout

    def scrap_data(self):
        posters_max_length = int(
            input("Input the max length of posters you want to scrap: "))
        # Store the pause time
        scroll_pause_time = self.__timeout
        # Select the posters box
        posters_box_container = self.__driver.find_element_by_css_selector(
            'div.browse-post-list')
        # Initial the now and last style of posters box to detect the page changes
        style_last = ''
        style_now = posters_box_container.get_attribute("style")
        # Initial the scroll height
        scroll_height = 3104.5
        # Initial the whileWork
        while_work = True
        # Start to scrap the data
        while while_work:
            # Check if styles are equal break the loop
            if style_last == style_now:
                while_work = False
            # Grab the data
            posters = posters_box_container.find_elements_by_css_selector(
                "div.post-card-item a")
            # Iterate over the scraped data
            for poster in posters:
                # Grab the poster link and normalize it
                link = url_normalize(poster.get_attribute('href'))
                # Check the link that exists in the links list
                if link not in self.__links:
                    # If it doesn't exist, append it to the list
                    self.__links.append(link)
            if (len(self.__links) > posters_max_length):
                while_work = False
            # Scroll the page
            self.__scrollPage(scroll_height)
            # Increase the scroll_height variable
            scroll_height += 3104.5
            # Make the app goes to sleep
            sleep(scroll_pause_time)
            # Refresh the styles
            style_last = style_now
            style_now = posters_box_container.get_attribute("style")
        print(f'Scraped {len(self.__links)} Links')
        self.__save_links()
        self.__driver.quit()

    # Save the links in file
    def __save_links(self):
        # Open the links.json file
        with open('links.json', 'w+', encoding='utf8') as f:
            # Clean it
            f.write('')
            # Append the new JSON to the file
            json.dump(self.__links, f, ensure_ascii=False)
        print("Links saved on links.json")

    # Scroll the page
    def __scrollPage(self, scroll_height: float):
        self.__driver.execute_script(
            "window.scrollTo(" + "{" + f'top:{scroll_height}, left:0, behavior: "smooth"' + "}" + ");")