import requests
from webexteamsbot import TeamsBot
from webexteamsbot.models import Response
import json
import os

# Note: Formatting in Webex Teams uses **text** for bold and *text* for italic

# Dict switch function for planet names and numbers
def planet_switch(input):
    switcher = {
        "1": "**Mercury**",
        "2": "**Venus**",
        "3": "**Earth**",
        "4": "**Mars**",
        "5": "**Jupiter**",
        "6": "**Saturn**",
        "7": "**Uranus**",
        "8": "**Neptune**",
        "mercury": "**1**",
        "venus": "**2**",
        "earth": "**3**",
        "mars": "**4**",
        "jupiter": "**5**",
        "saturn": "**6**",
        "uranus": "**7**",
        "neptune": "**8**"
    }
    return switcher.get(input, "Input is not a valid planet *name* or *number*!")

# Dict switch function for planet pictures based on name or number
def picture_switch(input):
    switcher = {
        "1": "https://space-facts.com/wp-content/uploads/mercury-transparent.png",
        "2": "https://space-facts.com/wp-content/uploads/venus-transparent.png",
        "3": "https://space-facts.com/wp-content/uploads/earth-transparent.png",
        "4": "https://space-facts.com/wp-content/uploads/mars-transparent.png",
        "5": "https://space-facts.com/wp-content/uploads/jupiter-transparent.png",
        "6": "https://space-facts.com/wp-content/uploads/saturn-transparent.png",
        "7": "https://space-facts.com/wp-content/uploads/uranus-transparent.png",
        "8": "https://space-facts.com/wp-content/uploads/neptune-transparent.png",
        "mercury": "https://space-facts.com/wp-content/uploads/mercury-transparent.png",
        "venus": "https://space-facts.com/wp-content/uploads/venus-transparent.png",
        "earth": "https://space-facts.com/wp-content/uploads/earth-transparent.png",
        "mars": "https://space-facts.com/wp-content/uploads/mars-transparent.png",
        "jupiter": "https://space-facts.com/wp-content/uploads/jupiter-transparent.png",
        "saturn": "https://space-facts.com/wp-content/uploads/saturn-transparent.png",
        "uranus": "https://space-facts.com/wp-content/uploads/uranus-transparent.png",
        "neptune": "https://space-facts.com/wp-content/uploads/neptune-transparent.png"
    }
    return switcher.get(input, "https://www.sccpre.cat/mypng/full/356-3567647_attention-incorrect-blemish-invalid-warning-icon-panic-button.png")

# Bot function for /planets trigger
def planets(input):
    # Extract string following trigger; Set to lowercase to allow for uppercase/lowercase data
    entry = bot.extract_message("/planets", input.text).strip().lower()
    response = Response()
    # Set general response if no data or "all" is entered
    if entry == "" or entry == "all":
        response.markdown = "Here are the 8 planets in order:  \n"
        response.markdown += "  1. Mercury  \n"
        response.markdown += "  2. Venus  \n"
        response.markdown += "  3. Earth  \n"
        response.markdown += "  4. Mars  \n"
        response.markdown += "  5. Jupiter  \n"
        response.markdown += "  6. Saturn  \n"
        response.markdown += "  7. Uranus  \n"
        response.markdown += "  8. Neptune  \n"
        return response
    else:
        # Set help response if "help" or "?" is entered
        if entry == "help" or input == "?":
            response.markdown = "Enter **/planets** followed by a planet name or a number to find the corresponding value.  \n"
            response.markdown += "Type **/planets** or **/planets all** to list all planets."
            return response
        else:
            # Call swtichers to retrieve planet name/number and picture
            response.markdown = planet_switch(entry)
            response.files = picture_switch(entry)
            return response

# Simple bot function to repsond to "ping" with "pong"
def ping(input):
    response = Response()
    response.text = "pong"
    return response

# Function to update default bot response with custom method as opposed to default "/help" response
def greeting(input):
    sender = bot.teams.people.get(input.personId)
    response = Response()
    response.markdown = "Hello **{}**! Welcome to this chat bot!  \n".format(sender.displayName)
    response.markdown += "You can get a list of commands by typing **/help**."
    return response

if __name__ == "__main__":

    # Set Webex Teams bot data fromn json file
    script_dir = os.path.dirname(__file__)
    bot_file = "{}\\bot.json".format(script_dir)
    with open(bot_file) as data_file:
        bot_json = json.load(data_file)
        bot_url = bot_json["bot_url"]
        bot_token = bot_json["bot_token"]
        bot_email = bot_json["bot_email"]
        bot_name = bot_json["bot_name"]

    # Create bot instance; Setting debug on
    bot = TeamsBot(
        bot_name,
        teams_bot_token = bot_token,
        teams_bot_url = bot_url,
        teams_bot_email = bot_email,
        debug = True
    )

    # Create bot commands
    bot.add_command("/planets", "List the planets.", planets)
    bot.add_command("/ping", "Send a ping, get a pong.", ping)
    bot.set_greeting(greeting)

    # Start bot using ngrok
    bot.run(host="0.0.0.0", port=5000)
