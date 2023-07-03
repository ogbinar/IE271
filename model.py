from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String,DateTime,Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime 

engine = create_engine('sqlite:///test.db', echo=True)
Base = declarative_base()

class Clients(Base):
    __tablename__ = "clients"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(100), nullable=True)


class Status(Base):
    __tablename__ = "status"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(100), nullable=True)

    
    
class Technicians(Base):
    __tablename__ = "technicians"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(100), nullable=True)

    
class Tasks(Base):
    __tablename__ = "tasks"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(100), nullable=True)
    service_type = Column('service_type', String(2), nullable=True)

class Specialties(Base):
    __tablename__ = "specialties"

    task_id = Column('task_id', Integer, ForeignKey('tasks.id'), primary_key=True)
    technician_id = Column('technician_id', Integer, ForeignKey('technicians.id'), primary_key=True)

    tasks = relationship(Tasks)
    technicians = relationship(Technicians)

    
class Orders(Base):
    __tablename__ = "orders"

    id = Column('id', Integer, primary_key=True)


    added_datetime = Column('added_datetime',DateTime,server_default=func.now())
    etc_datetime = Column('etc_datetime',DateTime, nullable=True)
    started_datetime = Column('started_datetime',DateTime, nullable=True)
    closed_datetime = Column('closed_datetime',DateTime, nullable=True)

    client_id = Column('client_id', Integer, ForeignKey('clients.id'), primary_key=True)
    task_id = Column('task_id', Integer, ForeignKey('tasks.id'), primary_key=True)
    status_id = Column('status_id', Integer, ForeignKey('status.id'), primary_key=True,default=2)
    tech_id = Column('tech_id', Integer, ForeignKey('technicians.id'), primary_key=True)

    clients = relationship(Clients)
    tasks = relationship(Tasks)
    status = relationship(Status)    
    technicians = relationship(Technicians)    

Base.metadata.create_all(engine) # create tables if not existing yet