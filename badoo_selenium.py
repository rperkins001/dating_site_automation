import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# Configuration
config = {
    "message_intro_1": "Hi, are you in Kyiv?",
    "message_2": ("Great, let's chat on Instagram instead, @ig_handle_here"),
    "positive_words": ["yes"],
    "webdriver_path": "/Users/00-facebook/Downloads/chromedriver_mac64/chromedriver",
    "facebook_email": "your_facebook_email",
    "facebook_password": "your_facebook_password",
}


def login(driver):
    driver.get("https://badoo.com/signin/")

    # Click on the "Sign in with Facebook" button
    facebook_login_button = driver.find_element_by_xpath('//span[contains(text(), "Facebook")]')
    facebook_login_button.click()

    # Switch to the Facebook login window
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[-1])

    # Enter your Facebook email and password
    email_input = driver.find_element_by_id("email")
    email_input.send_keys(config["facebook_email"])
    password_input = driver.find_element_by_id("pass")
    password_input.send_keys(config["facebook_password"])

    # Click the "Log In" button
    login_button = driver.find_element_by_name("login")
    login_button.click()

    # Switch back to the Badoo window
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[0])

    # Wait for login to complete
    time.sleep(5)

def get_all_matches(driver):
    matches = []

    # Navigate to the matches page
    driver.get("https://badoo.com/matches")

    # Wait for the matches to load
    time.sleep(5)

    try:
        # Find the container element that holds all the match elements
        matches_container = driver.find_element_by_css_selector(
            ".matches-container")

        # Find all match elements within the container
        match_elements = matches_container.find_elements_by_css_selector(
            ".match-element"
        )

        # Extract the match data from each match element
        # and append it to the matches list
        for match_element in match_elements:
            match_data = {
                "id": match_element.get_attribute(
                    "data-match-id"),
                "name": match_element.find_element_by_css_selector(
                    ".match-name").text,
                "profile_url": match_element.find_element_by_css_selector(
                    "a.match-profile-link"
                ).get_attribute("href"),
            }
            matches.append(match_data)

    except NoSuchElementException:
        # If the container or match elements are not found,
        # print a message and return an empty list
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
        messages_container = driver.find_element_by_css_selector(
            ".messages-container")

        # Find all message elements within the container
        message_elements = messages_container.find_elements_by_css_selector(
            ".message-element"
        )

        # Extract the message data from each message element
        # and append it to the conversation list
        for message_element in message_elements:
            message_data = {
                "text": message_element.find_element_by_css_selector(
                    ".message-text"
                ).text,
                "from_bot": "message-sent" in message_element.get_attribute(
                    "class"),
            }
            conversation.append(message_data)

    except NoSuchElementException:
        # If the container or message elements are not found,
        # print a message and return an empty list
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
        message_input_field = driver.find_element_by_css_selector(
            ".message-input")

        # Type the message into the input field
        message_input_field.send_keys(message)

        # Press Enter to send the message
        message_input_field.send_keys(Keys.RETURN)

        # Wait for the message to be sent
        time.sleep(2)

    except NoSuchElementException:
        # If the message input field is not found,
        # print a message and do nothing
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
                    message_intro_1_sent = False
                    positive_response_received = False

                    for msg in conversation:
                        if msg["from_bot"] and \
                                msg["text"] == config["message_intro_1"]:
                            message_intro_1_sent = True

                        if (
                            message_intro_1_sent
                            and not msg["from_bot"]
                            and any(
                                word in msg["text"].lower()
                                for word in config["positive_words"]
                            )
                        ):
                            positive_response_received = True
                            break

                    if not message_intro_1_sent:
                        send_message(driver, match, config["message_intro_1"])
                    elif positive_response_received:
                        # Check if the bot has already sent message_2
                        already_sent_message_2 = any(
                            msg["text"] == config["message_2"]
                            for msg in conversation
                            if msg["from_bot"]
                        )

                        if not already_sent_message_2:
                            send_message(driver, match, config["message_2"])

            time.sleep(random.uniform(60, 300))
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
