#!/usr/bin/python3
'''Flask web application.
'''
from flask import Flask, render_template


app = Flask(__name__)
'''The Flask application instance.'''
app.url_map.strict_slashes = False


@app.route('/')
def index():
    '''The home route.'''
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    '''The hbnb toute.'''
    return 'HBNB'


@app.route('/c/<text>')
def c(text):
    '''The c route.'''
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python/<text>')
@app.route('/python', defaults={'text': 'is cool'})
def python(text):
    '''The python route.'''
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>')
def number(n):
    '''The number route.'''
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>')
def number_template(n):
    '''The number_template route.'''
    var = {
        'n': n
    }
    return render_template('5-number.html', **var)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
