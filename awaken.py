# All private information has been redacted

# Twilio is what we use to place the call
from twilio.rest import Client
import discord

TOKEN = 'REDACTED'

client = discord.Client()

# Place the call to specified number
def makeCall(number):
    account_sid = 'REDACTED'
    auth_token = 'REDACTED'
    client = Client(account_sid, auth_token)

    call = client.calls.create(
        url='REDACTED',
        from_='REDACTED',
        to='+1' + str(number)
        )

    print(call.sid)

# Check if there is a number associated with the user ID provided
def checkNumber(id):
    found = False
    with open('numbers.txt') as f:
                lines = f.read().splitlines()
                for item in lines:
                    if id in item:
                        number = item.split()[1]
                        found = True
    return found

# Get the number associated with the specified user ID
def getNumber(id):
    number = ''
    with open('numbers.txt') as f:
                lines = f.read().splitlines()
                for item in lines:
                    if id in item:
                        number = item.split()[1]
    return number

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Awaken command; Any user can use this function to wake up a registered user
    if message.content.startswith('REDACTED'):
        text = message.content.split()
        if not len(text) < 2:
            text = message.content.split()
            print(text[1])

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

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)