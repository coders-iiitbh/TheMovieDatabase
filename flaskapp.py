from flask import render_template, url_for, flash, request, g
from flask import Flask, redirect
from forms import SearchForm
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable, search

# instantiate the application
app = Flask(__name__)

# configurations of the flask application
app.config['SECRET_KEY'] = 'okaycool'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:adi@localhost/sample_db'
app.config['SQLALCHEMY_TRACCK_MODIFICATIONS'] = True

# instantiate the database object
db = SQLAlchemy(app);
make_searchable(db.metadata)

# query class
class MovieQuery(BaseQuery, SearchQueryMixin):
    pass

# the realtions/tables in form of classes that will be used in the database
class Movie(db.Model):

    query_class = MovieQuery
    __tablename__ = 'movie'

    rank = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(255))
    genre = db.Column(db.UnicodeText)
    description = db.Column(db.UnicodeText)
    director = db.Column(db.Unicode(255))
    actors = db.Column(db.UnicodeText)
    year = db.Column(db.Integer)
    runtime = db.Column(db.Integer)
    rating = db.Column(db.Float)
    votes = db.Column(db.Integer)
    revenue = db.Column(db.Float)
    metascore = db.Column(db.Integer)

    search_vector = db.Column(TSVectorType('title', 'description'))

    def __init__(self, title, genre, description, director, actors, year, runtime, rating, votes, revenue, metascore):
        self.title = title
        self.genre = genre
        self.description = description
        self.director = director
        self.actors = actors
        self.year = year
        self.runtime = runtime
        self.rating = rating
        self.votes = votes
        self.revenue = revenue
        self.metascore = metascore

    def __repr__(self):
        return '<Movie %r>' % self.title

# create the movie table/relation
db.configure_mappers() # very important
db.create_all()
db.session.commit()

@app.route('/home')
@app.route('/')
def home():
    top = Movie.query.filter(Movie.year >= 2016).all()
    return render_template('home.html', top=top)

@app.route('/about')
def about():
    return render_template('about.html', title='Abouts')

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        results = Movie.query.search(form.search.data).limit(5).all()
        return render_template('searchpage.html', results=results, form=form)
    return render_template('searchpage.html', form=form)

# @app.route('/search_results/<query>')
# def search_results(query):
#     results = Movie.query.search(query).limit(5).all()
#     return render_template('search_result.html', results=results)

@app.route('/search/<name>', methods=['GET', 'POST'])
def movie_landing(name=None):
    return render_template('landing_page.html', name=name)

if __name__ == '__main__' :
    app.run(debug=True, host='0.0.0.0')
