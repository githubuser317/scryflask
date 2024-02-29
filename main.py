import secrets
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

from modules import search_api

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

@app.route('/', methods=['GET', 'POST'])
def index():    
    searchTerm = str(NameForm().name)
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    message = "Be Careful What You Seek"
    if form.validate_on_submit():
        SearchArray = search_api(searchTerm)
        # redirect the browser to another route and template
        return redirect( url_for('response') )
    return render_template('searchpage.html', form=form, message=message)
    
@app.route('/response/')
def response():
    return render_template('response.html')

# keep this as is
if __name__ == '__main__':
    app.run(debug=True)
