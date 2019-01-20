import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Table

Base = declarative_base()

# link between jumper and load
class JumperLoadLink(Base):
    __tablename__ = 'jumper_load_link'

    jumper_id = Column(Integer, ForeignKey('jumper.id'), primary_key = True)
    load_id = Column(Integer, ForeignKey('load.id'), primary_key = True)

class Jumper(Base):
    __tablename__ = 'jumper'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    # one to one relationship with license
    # a jumper can only have one license (they can have more but for what we care about)
    license = relationship('License', uselist = False, back_populates = 'jumper', passive_updates = False)

    # many to many relationship with loads
    # multiple jumpers will be on multiple loads
## also thinking that I will need load_id in situations like this - tbd
    load = relationship('Load', secondary = 'jumper_load_link', back_populates = 'jumpers', passive_updates = False)

    # JSON to help with debugging
    # turns out JSON might be used more
    # Can it link out to other tables?
    @property
    def serialize(self):
        return {
        'name': self.name,
        'ID': self.id,
        }


class License(Base):
    __tablename__ = 'license'

    id = Column(Integer, primary_key = True)
    lic = Column(String(10), nullable = False)
    expDate = Column('expDate', Date, nullable = False)
    # one to one relationship
    # one license can only apply to one jumper
    jumper_id = Column(Integer, ForeignKey('jumper.id'))
    jumper = relationship('Jumper', back_populates = 'license', passive_updates = False)

    # JSON to help with debugging
    @property
    def serialize(self):
        return {
        'ID': self.id,
        'license': self.lic,
        'expiration': self.expDate,
        'jumper': self.jumper_id
        }

class Load(Base):
    __tablename__ = 'load'

    id = Column(Integer, primary_key = True, nullable = False)
    date = Column(Date, nullable = False)
    # many to many with jumpers
    # a load will have many jumpers, jumpers will have multiple loads
    jumpers = relationship('Jumper', secondary = 'jumper_load_link', back_populates = 'load', passive_updates = False)
    # many to one with plane
    # many loads will be on one plane
    plane_id = Column(Integer, ForeignKey('plane.id'))
    plane = relationship('Plane', back_populates = 'load', passive_updates = False)
    # many to one with Pilot
    # a pilot will fly many loads
    pilot_id = Column(Integer, ForeignKey('pilot.id'))
    pilot = relationship('Pilot', back_populates = 'load', passive_updates = False)
    # many to many with rig
    # multiple rigs will be on multiple loads
    rigs = relationship('Rig', secondary = 'rig_load_link', back_populates = 'load', passive_updates = False)

    # JSON to help with debugging
    @property
    def serialize(self):
        return {
        'load': self.id,
        'plane': self.plane_id,
        'pilot': self.pilot_id,
        'date': self.date
        }

class Rig(Base):
    __tablename__ = 'rig'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    jumps = Column('jumps', Integer, nullable = False)
    aadExpiration = Column('aadExp', Date, nullable = False)
    reserveExpiration = Column('reserveExp', Date, nullable = False)

    # relationship with loads
    load = relationship('Load', secondary = 'rig_load_link', back_populates = 'rigs', passive_updates = False)
    # relationship with pack PackJob
    packjobs = relationship('PackJob', back_populates = 'rigs', passive_updates = False)


    # JSON to help with debugging
    @property
    def serialize(self):
        return {
        'ID': self.id,
        'name': self.name,
        'jumps': self.jumps,
        'aad expiration': self.aadExpiration,
        'reserve expiration': self.reserveExpiration,
        }

class RigLoadLink(Base):
    __tablename__ = 'rig_load_link'

    rig_id = Column(Integer, ForeignKey('rig.id'), primary_key = True)
    load_id = Column(Integer, ForeignKey('load.id'), primary_key = True)

class Packer(Base):
    __tablename__ = 'packer'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    # one to many with pack PackJob
    # a packer will do many packjobs in a day
    packjobs = relationship('PackJob', back_populates = 'packers', passive_updates = False)

    packNum = Column(Integer)

    # JSON to help with debugging
    @property
    def serialize(self):
        return {
        'name': self.name,
        'id': self.id,
        'packjobs': self.packNum
        }

class PackJob(Base):
    __tablename__ = 'packjob'

    id = Column(Integer, primary_key = True)
    date = Column('date', Date, nullable = False)

    # many to one relationship with rig
    # many packjobs for one rig, one packjob cannot be on multiple rigs
    rig_id = Column(Integer, ForeignKey('rig.id'))
    rigs = relationship('Rig', back_populates = 'packjobs', passive_updates = False)
    # many to one relationship with packer
    # one packer will do many packjobs, multiple packers will not be credited with one packjob
    packer_id = Column(Integer, ForeignKey('packer.id'))
    packers = relationship('Packer', back_populates = 'packjobs', passive_updates = False)

    # JSON to help with debugging
    @property
    def serialize(self):
        return {
        'id': self.id,
        'date': self.date,
        'rig': self.rig_id,
        'packer': self.packer_id
        }

class Plane(Base):
    __tablename__ = 'plane'

    id = Column(Integer, primary_key = True)
    name = Column(String(10), nullable = False)
    # relationship with loads
    load = relationship('Load', back_populates = 'plane', uselist = False, passive_updates = False)

    # JSON to help with debugging
    @property
    def serialize(self):
        return {
        'id': self.id,
        }


class Pilot(Base):
    __tablename__ = 'pilot'

    id = Column(Integer, primary_key = True)
    name = Column(String(20), nullable = False)
    # relationship with load
    load = relationship('Load', back_populates = 'pilot', uselist = False, passive_updates = False)

    # JSON to help with debugging
    @property
    def serialize(self):
        return {
        'name': self.name,
        'id': self.id,
        }

# End of the file
engine = create_engine('sqlite:///skydiving_system.db')
Base.metadata.create_all(engine)
