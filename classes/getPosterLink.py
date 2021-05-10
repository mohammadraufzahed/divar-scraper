from selenium import webdriver
import time
import json
from url_normalize import url_normalize


class GetPosterLink:
    def __init__(self, timeout):
        # Initial the browser
        self.driver = webdriver.Firefox()
        self.category_link = input("Input the category link: ")
        self.driver.get(self.category_link)
        #  Initial the list of links
        self.links = list()
        # Initial the timeout time
        self.timeout = timeout

    def scrapData(self):
        # Store the pause time
        scroll_pause_time = self.timeout
        # Select the posters box
        posters_box_container = self.driver.find_element_by_css_selector(
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
                if link not in self.links:
                    # If it doesn't exist, append it to the list
                    self.links.append(link)
            # Scroll the page
            self.driver.execute_script(
                "window.scrollTo(" + "{" + f'top:{scroll_height}, left:0, behavior: "smooth"' + "}"+");")
            # Increase the scroll_height variable
            scroll_height += 3104.5
            # Make the app goes to sleep
            time.sleep(scroll_pause_time)
            # Refresh the styles
            style_last = style_now
            style_now = posters_box_container.get_attribute("style")
        print(f'Scraped {len(self.links)} Links')
        self.driver.quit()

    # Save the links in file
    def saveLinks(self):
        # Open the links.json file
        with open('links.json', 'w+', encoding='utf8') as f:
            # Clean it
            f.write('')
            # Append the new JSON to the file
            json.dump(self.links, f, ensure_ascii=False)
        print("Links saved on links.json")
