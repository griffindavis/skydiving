from flask import Flask, render_template, request, url_for, redirect, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from skydiving_database_setup import *
from datetime import date
import os

app = Flask(__name__)

def engineMaker():
    engine = create_engine('sqlite:///skydiving_system.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

@app.route('/')
@app.route('/manifest')
def manifest():
    session = engineMaker()

    date = getTodaysDate()
    # do SQL stuff
    jumperList = session.query(Jumper).all()
    loadList = session.query(Load)#.filter_by(date=date)

    return render_template('manifest.html',
        jumperList = jumperList,
        loadList = loadList)

@app.route('/upcomingLoads/')
def upcomingLoads():
    session = engineMaker()
    #date = getTodaysDate()
    #if date != "":
    #    loadlist = session.query(Load).options(joinedload('jumpers', innerjoin = True)).filter_by(date=date)
    loadlist = session.query(Load).options(joinedload('jumpers', innerjoin = True)).all()

    return jsonify(load=[dict(i.serialize, jumpers=[j.serialize for j in i.jumpers]) for i in loadlist]) #render_template('upcomingLoads.html')

@app.route('/loadDisplay/')
def loadList():
    session = engineMaker()

    loadList = session.query(Load).options(joinedload('jumpers', innerjoin = True)).all()
    return render_template('loadDisplay.html')

@app.route('/packing')
def packing():
    session = engineMaker()

    return render_template('packing.html')

@app.route('/jumpers')
def jumpersJSON():
    session = engineMaker()
    jumpers = session.query(Jumper).all()
    return jsonify(Jumper=[i.serialize for i in jumpers])

@app.route('/loads')
def loadsJSON():
    session = engineMaker()
    loads = session.query(Load).all()
    return jsonify(Load=[i.serialize for i in loads])

@app.route('/loadinfo')
def loadInfoJSON():
    session = engineMaker()
    loads = session.query(Load).all()

@app.route('/backbone')
def backboneTesting():
    return render_template('backbone.html')

def getTodaysDate():
    today = str(date.today())
    return today

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 4000)
