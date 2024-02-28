import secrets
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

from data import ACTORS
from modules import get_names, get_actor, get_id

app = Flask(__name__)

topSecretKey = secrets.token_urlsafe(16)
app.secret_key = topSecretKey

# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)

# with Flask-WTF, each web form is represented by a class
# "NameForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used
class NameForm(FlaskForm):
    name = StringField('What Magic card are you thinking about?', validators=[DataRequired(), Length(3, 40)])
    submit = SubmitField('Submit and Begin the Search!')


# all Flask routes below

@app.route('/', methods=['GET'])
def search_api():
    card_search = NameForm.name
    api_prefix = "https://api.scryfall.com/cards/search?unique=prints&q="

    api_url = api_prefix + card_search

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
    #return card_list
    message = "The Truth"
       
    return redirect( url_for('response') )
        
    return render_template('searchpage.html', message=message)

@app.route('/response/')
def actor(id):
    # run function to get actor data based on the id in the path
    id, name, photo = get_actor(ACTORS, id)
    if name == "Unknown":
        # redirect the browser to the error template
        return render_template('404.html'), 404
    else:
        # pass all the data for the selected actor to the template
        return render_template('response.html', id=id, name=name, photo=photo)

# keep this as is
if __name__ == '__main__':
    app.run(debug=True)
