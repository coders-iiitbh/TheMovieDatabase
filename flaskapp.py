from flask import render_template, url_for, flash, request
from flask import Flask, redirect
from forms import SearchForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'okaycool'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:<password>@localhost/sample_db'
db = SQLAlchemy(app);


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(30))

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.name

@app.route('/home')
@app.route('/')
def home():
    # myUser = User()
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html', title='Abouts')

@app.route('/search/<movie_name>', methods=['GET', 'POST'])
@app.route('/search', methods=['GET', 'POST'])
def search_movie():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('searchpage.html', title='Search Results', form=form)

if __name__ == '__main__' :
    app.run(debug=True, host='0.0.0.0')
