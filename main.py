from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

#from data import ACTORS
from modules import get_names, get_actor, get_id, search_api

app = Flask(__name__)
app.secret_key = 'tO$&!|0wkamvVia0?n$NqIRVWOG'

# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)

# with Flask-WTF, each web form is represented by a class
# "NameForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used
class NameForm(FlaskForm):
    name = StringField('Which magic card do you seek?', validators=[DataRequired(), Length(2, 40)])
    submit = SubmitField('Submit')


# all Flask routes below

@app.route('/', methods=['GET', 'POST'])
def index():
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    searchterm = form.name.data
    searchcall = search_api(searchterm)
    message = "Good Luck"
    if form.validate_on_submit():
        return redirect( url_for('result',searchterm=searchterm) )
    else:
        message = "That actor is not in our database."
    """ if form.validate_on_submit():
        name = form.name.data
        if name.lower() in names:
            # empty the form field
            form.name.data = ""
            id = get_id(ACTORS, name)
            # redirect the browser to another route and template
            return redirect( url_for('actor', id=id) )
        else:
            message = "That actor is not in our database."  """
    return render_template('searchpage.html', searchcall=searchcall, searchterm=searchterm, form=form, message=message)

@app.route('/<searchterm>')
def result(searchterm):
    """ form = NameForm()
    searchterm = form.name.data """
    searchcall = search_api(searchterm)
     # run function to get actor data based on the id in the path
    
    return render_template('response.html',searchterm=searchterm, searchcall=searchcall)

# 2 routes to handle errors - they have templates too

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# keep this as is
if __name__ == '__main__':
    app.run(debug=True)
