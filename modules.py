from requests import get
from json import loads

def search_api(search):   
    api_prefix = "https://api.scryfall.com/cards/search?unique=prints&q="

    api_url = api_prefix + f'{search}'

    card_list = []

    while True:
        paging_list = loads(get(api_url).text)
        for card in paging_list['data']:
            #the try/except here is because double face cards dont have the same image_uri path and throws a key error
            #will i fix this later? If set contains Magic Online or Alchemy or doesnt have paper game type or digital = true then...
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

def total_results(search):   
    api_prefix = "https://api.scryfall.com/cards/search?unique=prints&q="

    api_url = api_prefix + f'{search}'

    total = loads(get(api_url).text)

    return total['total_cards']


def best_card(search):   
    api_prefix = "https://api.scryfall.com/cards/search?unique=prints&q="

    api_url = api_prefix + f'{search}'

    high_price = 0  # Initialize maximum price to 0
    high_price_card = None  # Initialize variable to store card with the highest price

    while True:
        paging_list = loads(get(api_url).text)
        for card in paging_list['data']:
            try:
                price = float(card['prices']['usd'])  # Extract price and convert to float
                if price > high_price:
                    high_price = price
                    high_price_card = card  # Update max_price_card if a higher price is found
            except (KeyError, TypeError):  # Handle KeyError if 'usd' or ValueError if price is not convertible to float
                continue

        if paging_list['has_more']:
            api_url = paging_list['next_page']
        else:    
            break

    return high_price_card