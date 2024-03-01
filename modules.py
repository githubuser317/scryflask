from json import loads
from requests import get
# functions to be used by the routes

# returns a list of results
def search_api(source):
    api_prefix = "https://api.scryfall.com/cards/search?unique=prints&q="
    
    try:
        api_url = api_prefix + f'{source}'

        card_list = []

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
    except:
            print("source")
    return card_list