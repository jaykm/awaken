from twilio.rest import Client
import discord

# Discord token
TOKEN = ''

client = discord.Client()

# Function to place the call
def makeCall(number):
    # Twilio account information
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)

    # Place the call
    call = client.calls.create(
        url='',
        from_='',
        to='+1' + str(number)
        )

# Check if the user has a number associated with their ID
def checkNumber(id):
    found = False
    with open('numbers.txt') as f:
                lines = f.read().splitlines()
                for item in lines:
                    if id in item:
                        number = item.split()[1]
                        found = True
    return found

# Get phone number ID
def getNumber(id):
    number = ''
    with open('numbers.txt') as f:
                lines = f.read().splitlines()
                for item in lines:
                    if id in item:
                        number = item.split()[1]
    return number

# Make sure that the message is not from the bot
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Awaken command; Any user can use this function to wake up a registered user
    # Check if the message starts with a mention to the bot
    if message.content.startswith(''):
        text = message.content.split()
        if not len(text) < 2:
            text = message.content.split()

            # Person who executed command
            id = message.author.id
            
            mentioned = text[1]

            # Strip formatting from user ID
            if mentioned.startswith('<'):
                mentioned = (text[1][2:-1])

            if mentioned.startswith('@'):
                mentioned = id

            # If the user has a nickname in the server they are mentioned in,
            # they will have an ! before their ID. We need to remove that
            if mentioned.startswith('!'):
                mentioned = mentioned[1::]
            
            # Get discord User object from ID
            user = await client.get_user_info(mentioned)
            msg = 'Waking up ' + user.name
            number = ''
            if not checkNumber(mentioned):
                msg = 'No number found for ' + user.name
            else:
                makeCall(getNumber(mentioned))
                
            # Send message
            await client.send_message(message.channel, msg)
        else:
            msg = 'Not enough arguments'
            await client.send_message(message.channel, msg)

    # Register command; Saves the user's phone number and ID
    if message.content.startswith('!register'):
        msg = ''
        text = message.content.split()

        # Check if phone number is valid
        if text[1].isdigit() and len(text[1]) == 10:
            id = message.author.id

            # Check if user already has phone number associated
            if checkNumber(id):
                msg = 'Record exists for user'
            else:
                out = [id, text[1]]

                # Write text to file
                file = open('numbers.txt', 'a')
                file.write(str(id) + ', ' + text[1] + '\n')
                file.close()

                msg = 'Registered ' + text[1] + ' for ' + id
        else:
            msg = 'Invalid number. Phone numbers must be 10 digits'
    await client.send_message(message.channel, msg)

    # Test command. This is not used
    # if message.content.startswith('!test'):
    #     await client.send_message(message.channel, 'test invoked')
        

# This runs when the bot is ready
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)