# Discord Magic The Gathering Bot
Basic MTG Search Bot written in Python 3.6 to help myself get familiar with the language

Replace the comment with your bot's token to use
```
TOKEN = #custom token goes here
```

## Use
The bot will search for a term inbetween two brackets on each side.

A message will be returned with a message with a link if a single result has been found.

In the case of multiple results no link will be returned.

### Example
```
[[Lightning Bolt]]

Bot will return: 
http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=442130
```
