import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# Configuration
config = {
    "message_intro_1": "Hi, are you in Kyiv?",
    "message_2": "Great, let's chat on Instagram instead, it's better, @ig_handle_here",
    "positive_words": ["yes"],
    "username": "your_username",
    "password": "your_password",
    "webdriver_path": "path/to/your/webdriver"
}

def login(driver):
    driver.get("https://badoo.com/signin/")

    username_field = driver.find_element_by_name("email")
    password_field = driver.find_element_by_name("password")

    username_field.send_keys(config["username"])
    password_field.send_keys(config["password"])
    password_field.send_keys(Keys.RETURN)

    time.sleep(5)  # Wait for login to complete

def get_all_matches(driver):
    matches = []

    # Navigate to the matches page
    driver.get("https://badoo.com/matches")

    # Wait for the matches to load
    time.sleep(5)

    try:
        # Find the container element that holds all the match elements
        matches_container = driver.find_element_by_css_selector(".matches-container")

        # Find all match elements within the container
        match_elements = matches_container.find_elements_by_css_selector(".match-element")

        # Extract the match data from each match element and append it to the matches list
        for match_element in match_elements:
            match_data = {
                "id": match_element.get_attribute("data-match-id"),
                "name": match_element.find_element_by_css_selector(".match-name").text,
                "profile_url": match_element.find_element_by_css_selector("a.match-profile-link").get_attribute("href")
            }
            matches.append(match_data)

    except NoSuchElementException:
        # If the container or match elements are not found, print a message and return an empty list
        print("Unable to find match elements on the page")
        return []

    return matches

def get_conversation(driver, match):
    # Navigate to the match's profile page using the URL from the match data
    driver.get(match["profile_url"])

    # Wait for the conversation to load
    time.sleep(5)

    conversation = []

    try:
        # Find the container element that holds all the message elements
        messages_container = driver.find_element_by_css_selector(".messages-container")

        # Find all message elements within the container
        message_elements = messages_container.find_elements_by_css_selector(".message-element")

        # Extract the message data from each message element and append it to the conversation list
        for message_element in message_elements:
            message_data = {
                "text": message_element.find_element_by_css_selector(".message-text").text,
                "from_bot": "message-sent" in message_element.get_attribute("class")
            }
            conversation.append(message_data)

    except NoSuchElementException:
        # If the container or message elements are not found, print a message and return an empty list
        print("Unable to find message elements on the page")
        return []

    return conversation

def send_message(driver, match, message):
    # Navigate to the match's profile page using the URL from the match data
    driver.get(match["profile_url"])

    # Wait for the message input field to load
    time.sleep(5)

    try:
        # Find the message input field element
        message_input_field = driver.find_element_by_css_selector(".message-input")

        # Type the message into the input field
        message_input_field.send_keys(message)

        # Press Enter to send the message
        message_input_field.send_keys(Keys.RETURN)

        # Wait for the message to be sent
        time.sleep(2)

    except NoSuchElementException:
        # If the message input field is not found, print a message and do nothing
        print("Unable to find message input field on the page")

def main():
    driver = webdriver.Chrome(config["webdriver_path"])

    try:
        login(driver)

        while True:
            matches = get_all_matches(driver)

            for match in matches:
                conversation = get_conversation(driver, match)

                if not conversation:
                    send_message(driver, match, config["message_intro_1"])
                else:
                    last_message = conversation[-1]

                    if any(word in last_message.lower() for word in config["positive_words"]) and config["message_2"] not in conversation:
                        send_message(driver, match, config["message_2"])

            time.sleep(random.uniform(60, 300))
    finally:
        driver.quit()

if __name__ == "__main__":
    main()