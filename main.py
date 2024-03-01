import secrets
from json import loads
from requests import get
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

#from modules import search_api

app = Flask(__name__)

topSecretKey = secrets.token_urlsafe(16)
app.secret_key = topSecretKey

# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)

## Function
def search_api(searchTerm):
    api_prefix = "https://api.scryfall.com/cards/search?unique=prints&q="
    
    try:
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
    except UnboundLocalError:
        print("api_url")
    return card_list
    
##

# with Flask-WTF, each web form is represented by a class
# "NameForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used
class NameForm(FlaskForm):
    name = StringField('What Magic card are you thinking about?', validators=[DataRequired(), Length(3, 40)])
    submit = SubmitField('Submit and Begin the Search!')

testVar = search_api('lion')

# all Flask routes below

@app.route('/', methods=['GET', 'POST'])
def index():    
    form = NameForm()
    message = testVar[0]['name']
    # redirect the browser to another route and template
    if testVar:
        return redirect( url_for('response') )
    return render_template('searchpage.html', testVar=testVar, form=form, message=message)
    
@app.route('/response')
def response():
    if testVar:
        return render_template('response.html', testvar=testVar)

# keep this as is
if __name__ == '__main__':
    app.run(debug=True)
