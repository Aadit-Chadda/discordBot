from bs4 import BeautifulSoup
from replit import db
import discord
import requests
import random

client = discord.Client()


def get_quote():
    link = requests.get('https://zenquotes.io/').text
    soup = BeautifulSoup(link, 'lxml')
    widget = soup.find('div', class_='container')
    quote = widget.find('h1').text
    author = widget.find('p').text
    words = quote + '\n' + author
    return words


def update_encouragement(encouraging_message):
    if "encourage" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragement(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


sad_words = ['depressed',
             'unhappy',
             'fucked',
             'miserable',
             'sad',
             'depressing',
             'angry',
             'Heartbroken',
             'Sorrowful',
             'Heartache',
             'Mourn',
             'Mournful',
             'Dismal',
             'Somber',
             'Grief',
             'Depressed',
             'Melancholy',
             'Hopelessness',
             'Woeful',
             'Despairing',
             'Regretful',
             'Unhappy']

starter_enouragements = ['Cheer Up!',
                         'Hang in there',
                         "You are Great",
                         "don't worry, it will all be okay",
                         'You are going to get through it']


# Client Connector
@client.event
async def on_ready():
    print('We Have Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    msg = message.content
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello! How are you?')
    
    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)
    
    options = starter_enouragements
    if "encouragements" in db.keys():
        options = options + db["encouragements"]
    
    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(options))
    
    if msg.startswith("$new"):
        encouraging_message = msg.split("$new ", 1)[1]
        update_encouragement(encouraging_message)
        await message.channel.send("New encouraging message added.")
    
    if msg.startswith("$del"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("$del ", 1)[1])
            delete_encouragement(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

BotToken = ''
client.run(BotToken)
