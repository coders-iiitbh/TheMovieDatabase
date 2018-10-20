from flask import render_template, url_for, flash, request
from flask import Flask, redirect
from forms import SearchForm
from flask_sqlalchemy import SQLAlchemy
from flask_whooshalchemy import whoosh_index

# instantiate the application
app = Flask(__name__)

# configurations of the flask application
app.config['SECRET_KEY'] = 'okaycool'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:adi@localhost/sample_db'
#app.config['SQLALCHEMY_TRACCK_MODIFICATIONS'] = True
app.config['WHOOSH_BASE'] = 'whoosh'

# instantiate the database object
db = SQLAlchemy(app);

# the realtions/tables in form of classes that will be used in the database
class Movie(db.Model):
    __searchable__ = ['name']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(30))

    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Movie %r>' % self.name

whoosh_index(app, Movie)

@app.route('/home')
@app.route('/')
def home():
    #myMovie = Movie()
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html', title='Abouts')

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        return redirect((url_for('search_results', query=form.search.data)))
    return render_template('searchpage.html', form=form)

@app.route('/search_results/<query>')
def search_results(query):
  # results = Movie.query.whoosh_search(query).all()
  # return str(request.form)
  res =  db.session.query(Movie).all()
  print( str(res));

if __name__ == '__main__' :
    app.run(debug=True, host='0.0.0.0')
