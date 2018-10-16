from flask import Flask, redirect, render_template, flash, redirect, url_for, request,g 
from flask_wtf import FlaskForm 
from wtforms import TextAreaField, BooleanField, StringField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)


app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'FuckOFF'


class SearchForm(FlaskForm):
    search = StringField('search')


@app.route("/", methods=['GET'])
def index():
		g.search_form = SearchForm()
		return render_template('index.html')

@app.route('/search')
def search():
		q = request.args.get('search')
		return render_template('gallery.html', args=q)



@app.route('/single')
def single():
		return render_template('single.html')

if __name__ == '__main__':
     app.run()


