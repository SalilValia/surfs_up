#from flask import Flask
#app = Flask(__name__)

#@app.route('/')
#def hello_world():
    #return 'Hello world'

#above is what I need to do to get flask to work
# setup and Dependencies
import datetime as dt
import numpy as np
import pandas as pd
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func , inspect
from flask import Flask, jsonify

database_path = "../surfs_up/hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")
insp = inspect(engine)
# check database table names
print(insp.get_table_names())
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
# Create the Flask app which is above 
app = Flask(__name__)

# define welcome or index route
@app.route('/')
def welcome():
  return(
  f'Welcome to the Climate Analysis API!<br/>'
  f'Available Routes:<br/>'
  f'/api/v1.0/precipitation<br/>'
  f'/api/v1.0/stations<br/>'
  f'/api/v1.0/tobs<br/>'
  f'/api/v1.0/temp/start/end<br/>'
  )

# Defining the precepitation route
@app.route("/api/v1.0/precipitation")  
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Defining the station route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations) 

# Defining the temp route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Defining the stat route
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

    if __name__ == '__main__':
         app.run(debug=True)