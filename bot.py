import asyncio
import re
import requests
from discord.ext.commands import Bot
from bs4 import BeautifulSoup

TOKEN = 
PREFIX = ('!')

description = '''Test Bot in Python'''
bot = Bot(command_prefix=PREFIX, description=description)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
@asyncio.coroutine
async def on_message(message):
    # regex matches the text in between [[ and ]]
    cardname = re.findall(r"[[^[]*\[([^]]*)\]]", message.content)
    if len(cardname) > 0:
        bot_message = search_cards(cardname[0])
        if bot_message.startswith(tuple(str(i) for i in range(1))): #If message starts with 0 or 1
            await bot.send_message(message.channel, bot_message)
        else:
            await bot.send_message(message.channel, bot_message)
    else:
        message = 'Invalid search request'
        return message


def search_cards(card_name):
    cards_found = []
    search_result_links = []
    split_name = []
    match = False
    split_name = card_name.split()  #split name on spaces
    i = 0
    for i in range(0, len(split_name)):  #add brackets because of link format
        split_name[i] = '[%s]' % split_name[i]

    req = 'http://gatherer.wizards.com/Pages/Search/Default.aspx?name='
    i = 0
    for i in range(0, len(split_name)):  #append each split word from name into request link
        req += '+%s' % split_name[i]

    r = requests.get(req, timeout=10)  #search Gatherer for cards
    soup = BeautifulSoup(r.text, 'html.parser')
    search_result = soup.findAll('span', class_="cardTitle")

    if len(search_result) > 0:  #multiple cards found
        for card in range(0, len(search_result)):
            cards_found.append(search_result[card].find('a').contents[0])

        for links in range(0, len(search_result)):  #get array of links corresponding with results
            search_result_links.append(search_result[links].find('a')['href'])

        search_result_links = [a[2:] for a in search_result_links]

        i = 0
        for i in range(0, len(search_result)):  #check for a card with same name as search term
            if card_name.lower() == cards_found[i].lower():
                match = True
                break

        if match == True:
            message = 'http://gatherer.wizards.com/Pages' + search_result_links[i]

        else:
            message = '%s results found and no exact match' % str(len(search_result))

        del cards_found
        return message

    else:  #single result or no results
        if req != r.url:  #page redirects if search not found, r.url is redirected page
            message = r.url
        else:
            message = '%s results found' % str(len(search_result))
        del cards_found
        return message


bot.run(TOKEN)