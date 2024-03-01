# functions to be used by the routes
#from flask import Flask,request,jsonify
import requests
from requests import get
from json import loads

#retrieve list of cards matching the search term
def search_api(searchTerm):
    api_prefix = "https://api.scryfall.com/cards/search?unique=prints&q="
    
    api_url = api_prefix + searchTerm
    
    card_list = []

    while True:
        paging_list = loads(get(api_url).text)

        for card in paging_list['data']:
            card_data = {
                'name': card['name'],
                'set': card['set_name'],
                'num': card['collector_number'],
                'price': card['prices']['usd']
            }

            card_list.append(card_data)

        if not paging_list['has_more']:
            break

        api_url = paging_list['next_page']
    return card_list
