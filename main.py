from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

from modules import search_api
import secrets

app = Flask(__name__)

topSecretKey = secrets.token_urlsafe(16)
app.secret_key = topSecretKey

# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)

class NameForm(FlaskForm):
    name = StringField('Which Magic card do you seek?', validators=[DataRequired(), Length(2, 40)])
    submit = SubmitField('Submit and Bring Forth The Arcane!')


# all Flask routes below

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    searchterm = form.name.data
    searchcall = search_api(searchterm)
    message = ""
    if form.validate_on_submit():
        return redirect( url_for('result',searchterm=searchterm) )
    else:
        message = "The Blind Eternities Await"
    return render_template('searchpage.html', searchcall=searchcall, searchterm=searchterm, form=form, message=message)

@app.route('/<searchterm>')
def result(searchterm):
    searchcall = search_api(searchterm)
    return render_template('response.html',searchterm=searchterm, searchcall=searchcall)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='10.0.0.134')
