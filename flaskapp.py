from flask import render_template, url_for, flash, request
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

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255))
    content = db.Column(db.UnicodeText)
    search_vector = db.Column(TSVectorType('name', 'content'))

    def __init__(self, name, content):
        self.name = name
        self.content = content

    def __repr__(self):
        return '<Movie %r>' % self.name

# create the movie table/relation
db.configure_mappers() # very important
db.create_all()
db.session.commit()

@app.route('/home')
@app.route('/')
def home():
    posts = Movie.query.limit(10).all()
    return render_template('home.html', posts=posts)

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
    results = Movie.query.search(query).limit(5).all()
    return render_template('search_result.html', results=results)

@app.route('/search/<name>', methods=['GET', 'POST'])
def movie_landing(name=None):
    return render_template('landing_page.html', name=name)

if __name__ == '__main__' :
    app.run(debug=True, host='0.0.0.0')
