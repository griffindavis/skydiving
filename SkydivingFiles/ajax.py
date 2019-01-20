from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)


# define the pages

@app.route('/')
@app.route('/testing')
def runPage():
    return render_template('index.html')


# run at the start
if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host = '0.0.0.0', port = 4000)
