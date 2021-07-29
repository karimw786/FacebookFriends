#!/usr/bin/env python

""" FacebookFriends.py: Writes a Facebook user's friends to file. """

import time
import os
import getpass

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FacebookFriends:
    CSS_SELECTOR_FRIEND = "div._2pit a"
    CHROME_DRIVER = "chromedriver.exe"
    OUTPUT_FILENAME = "FacebookFriends.txt"

    script_path = os.path.dirname(__file__)
    chrome_driver_path = os.path.join(script_path, CHROME_DRIVER)
    output_filepath = os.path.join(script_path, OUTPUT_FILENAME)

    def __init__(self, facebook_username, facebook_password, facebook_friends_url):
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path)
        self.friends = None
        self.facebook_username = facebook_username
        self.facebook_password = facebook_password
        self.facebook_friends_url = facebook_friends_url

    def facebook_login(self):
        """ Open Facebook login page in new browser window, then log in """
        self.driver.get(self.facebook_friends_url)
        input_email = self.driver.find_element_by_id("m_login_email")
        input_password = self.driver.find_element_by_id("m_login_password")
        btn_login = self.driver.find_element_by_name("login")
        input_email.send_keys(self.facebook_username)
        time.sleep(1)
        input_password.send_keys(self.facebook_password)
        time.sleep(1)
        btn_login.click()
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.CSS_SELECTOR_FRIEND))
        )

    def display_all_friends(self):
        """ Scroll through Facebook Friends page until bottom of page is reached """
        # Initial count of elements
        element_count = len(self.driver.find_elements_by_css_selector(self.CSS_SELECTOR_FRIEND))
        print("Processing " + str(element_count) + " CSS selectors...")

        # Scroll page to the end
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            # If the number of elements is the same, the end of page has been reached
            if len(self.driver.find_elements_by_css_selector(self.CSS_SELECTOR_FRIEND)) == element_count:
                break

            element_count = len(self.driver.find_elements_by_css_selector(self.CSS_SELECTOR_FRIEND))
            print("Processing " + str(element_count) + " CSS selectors...")

        # Store friends in class variable
        self.friends = self.driver.find_elements_by_css_selector(self.CSS_SELECTOR_FRIEND)

    def write_friends_to_file(self):
        """ Write sorted list of Facebook friends to a text file """
        if self.friends is not None:
            friends_list = []

            for friend in self.friends:
                if friend.text.strip() != "":
                    friends_list.append(friend.text)

            print("\nFound " + str(len(friends_list)) + " Facebook friends.")
            print("Writing Facebook friends to output file: " + self.output_filepath)

            friends_list.sort()

            with open(self.output_filepath, "w", encoding="utf-8") as file_handle:
                for friend in friends_list:
                    print(friend, file=file_handle)

            file_handle.close()
            print("*** Output file written successfully. Safe to exit program. ***")
        
        else:
            print("Unable to write friends to file. 'self.friends' is empty. Exit program and try again.")

    def __del__(self):
        self.driver.close()


if __name__ == "__main__":
    facebook_username = input("Your Facebook username: ")
    facebook_password = getpass.getpass("Your Facebook password: ")
    facebook_friends_url = input("Desired Facebook Friends mobile site URL (e.g., https://m.facebook.com/karim.wallani/friends): ")
    fb = FacebookFriends(facebook_username, facebook_password, facebook_friends_url)
    fb.facebook_login()
    fb.display_all_friends()
    fb.write_friends_to_file()
