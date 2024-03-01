from json import loads
from requests import get
# functions to be used by the routes

# retrieve all the names from the dataset and put them into a list
def get_names(source):
    names = []
    for row in source:
        # lowercase all the names for better searching
        name = row["name"].lower()
        names.append(name)
    return sorted(names)

# find the row that matches the id in the URL, retrieve name and photo
def get_actor(source, id):
    for row in source:
        if id == str( row["id"] ):
            name = row["name"]
            photo = row["photo"]
            # change number to string
            id = str(id)
            # return these if id is valid
            return id, name, photo
    # return these if id is not valid - not a great solution, but simple
    return "Unknown", "Unknown", ""

# find the row that matches the name in the form and retrieve matching id
def get_id(source, name):
    for row in source:
        # lower() makes the string all lowercase
        if name.lower() == row["name"].lower():
            id = row["id"]
            # change number to string
            id = str(id)
            # return id if name is valid
            return id
    # return these if id is not valid - not a great solution, but simple
    return "Unknown"

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
                    'price': card['prices']['usd']
                }

                card_list.append(card_data)

            if not paging_list['has_more']:
                break

            api_url = paging_list['next_page']
    except:
            print("source")
    return card_list