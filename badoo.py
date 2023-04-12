import time
import random
from badoo_api import Badoo

# Configuration
config = {
    "message_intro_1": "Hi, are you in London?",
    "message_2": "Great, let's chat on Instagram instead, it's better, @ig_handle_here",
    "positive_words": ["yes"]
}

# Login to Badoo
badoo = Badoo("your_username", "your_password")

def send_message(match, message):
    # Implement the method to send a message to the match using the API
    pass

def main():
    while True:
        # Get all matches
        matches = badoo.get_all_matches()

        for match in matches:
            conversation = badoo.get_conversation(match)

            if not conversation:
                # Send message_intro_1 if the bot hasn't talked to the match before
                send_message(match, config["message_intro_1"])
            else:
                last_message = conversation[-1]

                # If the match replied positively and the bot hasn't sent message_2 yet
                if any(word in last_message["text"].lower() for word in config["positive_words"]) and not any(msg["text"] == config["message_2"] for msg in conversation if msg["from_bot"]):
                    send_message(match, config["message_2"])

        # Sleep for a random time between 1 and 5 minutes before checking again
        time.sleep(random.uniform(60, 300))

if __name__ == "__main__":
    main()