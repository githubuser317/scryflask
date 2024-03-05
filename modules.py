from requests import get
from json import loads

""" def search_api(source):
    api_prefix = "https://api.scryfall.com/cards/search?unique=prints&q="
    
    api_url = api_prefix + f'{source}'

    card_list = []
    paging_list = []
    
    while True:
        paging_list = loads(get(api_url).text)

        for card in paging_list['data']:
            card_data = {
                'name': card['name'],
                'set': card['set_name'],
                'num': card['collector_number'],
                'price': card['prices']['usd'],
                'image': card['image_uris']['normal']
            }

            card_list.append(card_data)

        if not paging_list['has_more']:
            break

        api_url = paging_list['next_page']
   
    return card_list """

def search_api(search):   
    api_prefix = "https://api.scryfall.com/cards/search?unique=prints&q="

    api_url = api_prefix + f'{search}'

    paging_list = loads(get(api_url).text)

    card_list = []

    while True:
        paging_list = loads(get(api_url).text)
        for card in paging_list['data']:
            #the try/except here is because double face cards dont have the same image_uri path and throws a key error
            #will i fix this later?
            try:
                card_data = {
                    'name': card['name'],
                    'set': card['set_name'],
                    'num': card['collector_number'],
                    'price': card['prices']['usd'],
                    'image': card['image_uris']['normal']
                }
                card_list.append(card_data)
            except KeyError:
                continue

        if paging_list['has_more']:
            api_url = paging_list['next_page']
            
        else:    
            break

    return card_list