import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
print(Base.classes.keys())

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)
app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to the Justice League API!<br/>"
        f"Available Routes:<br/>"
        f'<a href = "/api/v1.0/precipitation">Precipitation</a><br/>'
        f'<a href = "/api/v1.0/stations">Stations</a><br/>'
        f'<a href = "/api/v1.0/tobs">Tobs</a><br/>' 
        f'<a href = "/api/v1.0/temp/<start>/<end>">Statistics</a><br/>' 
        f'<a href = "/api/v1.0/temp/2017-06-01/2017-06-30">Statistics example - 2017-06-01/2017-06-30 </a><br/>'     
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(356)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temp = list(np.ravel(results))
    return jsonify(temp)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps1 = list(np.ravel(results))
        return jsonify(temps1)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps2 = list(np.ravel(results))
    return jsonify(temps2)


# export FLASK_APP=app.py
# set FLASK_APP=app.py
# flask run
app.run(debug=True, host='localhost', port=5001)

