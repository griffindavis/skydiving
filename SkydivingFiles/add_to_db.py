from datetime import date
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from skydiving_database_setup import Base, Jumper, Load, License, Plane, Pilot

engine = create_engine('sqlite:///skydiving_system.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def addJumper(nameVal, licenseVal, expDate):
    if nameVal == "":
         return 0
    else:
        year,month,day = convertDate(expDate)
        expDate=date(year, month, day)
        license = License(lic=licenseVal, expDate=expDate)
        jumper = Jumper(name=nameVal, license=license)
        session.add(jumper)

        print 'added jumper ' + nameVal

def addPilot(pilotName):
    if pilotName == "":
        return 0
    else:
        pilot = Pilot(name=pilotName)
        session.add(pilot)

        print 'Added pilot ' + pilotName

def addPlane(planeName):
    if planeName == "":
        return 0
    else:
        plane = Plane(name = planeName)
        session.add(plane)

        print 'Added plane ' + planeName

def convertDate(expDate):
    # split will put it into an array
    ary = expDate.split('-')
    # need integer values from the string
    year = int(ary[0])
    month = int(ary[1])
    day = int(ary[2])

    return year,month,day

def addLoads():
    pilotList = session.query(Pilot).all()
    planeList = session.query(Plane).all()
    jumperList = session.query(Jumper).all()
    jumpers = session.query(Jumper).all()

    today = date.today().isoformat()
    year,month,day = convertDate(today)
    print year
    print month
    print day
    dateAdd = date(year,month,day)

    for pilot in pilotList:
        pilot_id = pilot.id

        for plane in planeList:
            plane_id = plane.id

            load = Load(plane_id = plane_id,
            pilot_id = pilot_id,
            jumpers = jumpers,
            date = dateAdd)

            session.add(load)

            print 'Load ' + str(load.id) + 'added'

addPilot('Maverick')
addPilot('Ice Man')

addPlane('82Romeo')
addPlane('824')

addJumper('Greg Anthony', '27363', '2019-2-2')
addJumper('Griffin Davis', '283747', '2019-2-2')
addJumper('Brad Lawson', '12345', '2019-2-2')
addJumper('James Ridley', '18373', '2019-2-2')
addJumper('Erik Gregory', '23844', '2019-2-2')
addJumper('Allison Riley', '34097', '2019-2-2')

session.commit()

addLoads()

session.commit()

print "\nCreated the scratch database."
