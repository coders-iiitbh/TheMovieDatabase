from flask import Flask, redirect, render_template, flash, redirect, url_for, request,g 
from flask_wtf import Form 
from wtforms import TextAreaField, BooleanField, StringField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'FuckOFF'


class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])


@app.route("/", methods=['GET'])
def index():
		g.search_form = SearchForm()
		return render_template('index.html')

@app.route('/search')
def search():
		q = request.args.get('search')
    		return "HELLO %s" %q
    	

if __name__ == '__main__':
     app.run()


