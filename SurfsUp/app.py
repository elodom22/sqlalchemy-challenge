# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all avaiable routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# precip routing
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    #query the last 12 months of data
    one_yr_ago = "2016-08-23"
    precip_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_yr_ago).all()
    
    session.close()

# Create a dictionary from precip_results
    precip_data = []
    for date, prcp in precip_results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip_data.append(precip_dict)

    return jsonify(precip_data)

# station routing
@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query list of stations
    stat_results = session.query(Station.station, Station.name).all()
    session.close()
# Create a dictionary from stat_results
    stat_data = []
    for station, name in stat_results:
        stat_dict = {}
        stat_dict["station"] = station
        stat_dict["name"] = name
        stat_data.append(stat_dict)

    return jsonify(stat_data)

# tobs routing
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # query previous year of data
    cutoff_date = "2016-08-23"
    tobs_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= cutoff_date).all()
    session.close()
    # Create a dictionary from tobs_results
    tobs_data = []
    for date, tobs in tobs_results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)

# Start - Min - Max - Avg temp routing
@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # query start temps
    start_temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                    filter(Measurement.date >= start).all()
    session.close()

    # Create a dictionary from start date
    start_date_tobs = []
    for min, max, avg in start_temps:
        start_dict = {}
        start_dict["min_temp"] = min
        start_dict["max_temp"] = max
        start_dict["avg_temp"] = avg
        start_date_tobs.append(start_dict)
    return jsonify(start_date_tobs)

# Start/End routing
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    session = Session(engine)
    start_end_t = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close
    # Create a dictionary 
    start_end_tobs = []
    for min, max, avg in start_end_t:
         start_end_dict = {}
         start_end_dict["min_temp"] = min
         start_end_dict["max_temp"] = max
         start_end_dict["avg_temp"] = avg
         start_end_tobs.append(start_end_dict)
         
    return jsonify(start_end_tobs)

if __name__ == "__main__":
    app.run(debug=True)