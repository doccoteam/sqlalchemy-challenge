# import dependencies 
import datetime as dt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)

# reflect the database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Home page.
# List all routes that are available.
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Routes:<br/>"
        f"<br/>"
        f"<a href='http://127.0.0.1:5000/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"- List of prior year rain totals from all stations<br/>"
        f"<br/>"
        f"<a href='http://127.0.0.1:5000/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"- List of Station numbers and names<br/>"
        f"<br/>"
        f"<a href='http://127.0.0.1:5000/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"- List of prior year temperatures from all stations<br/>"
        f"<br/>"
        f"<a href='http://127.0.0.1:5000/api/v1.0/start'>/api/v1.0/start</a><br/>"
        f"- Enter a start date (YYYY-MM-DD), calculates the MIN/AVG/MAX temperature for all dates greater than and equal to the start date<br/>"
        f"<br/>"
        f"<a href='http://127.0.0.1:5000/api/v1.0/start/end'>/api/v1.0/start/end</a><br/>"
        f"- Enter a start and an end date (YYYY-MM-DD), calculate the MIN/AVG/MAX temperature for dates between the start and end date inclusive<br/>"

    )

# Convert the query results to a Dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of rain fall for prior year"""

    session = Session(engine)

    session.query(Measurement.date).order_by(Measurement.date.desc())
    end_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    end_date = end_date[0]
    
    # Calculate the date 1 year ago from the last data point in the database
    start_date = dt.datetime.strptime(end_date, "%Y-%m-%d")- dt.timedelta(days=365)
   
    # Perform a query to retrieve the data and precipitation scores
    query_for_prcp_data=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=start_date).all()
    
    session.close()

    # Create a list of dicts with `date` and `prcp` as the keys and values
    prcp = []
    for q in query_for_prcp_data:
        row = {}
        row["date"] = query_for_prcp_data[0]
        row["prcp"] = query_for_prcp_data[1]
        prcp.append(row)
    
    return jsonify(prcp)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")

def stations():
    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()
    
    stations = list(np.ravel(results))

    return jsonify(stations)

# Query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.

@app.route("/api/v1.0/tobs")

def temperature():

    session = Session(engine)
  
    tobs = []
    query_results = session.query(Measurement.tobs).filter(Measurement.date >= "08-23-2016").all()

    session.close()

    tobs = list(np.ravel(query_results))
    return jsonify(tobs)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")

def start_trip(start):

    session = Session(engine)

    results = session.query\
    (func.min(Measurement.tobs).label('tmin'),\
    func.avg(Measurement.tobs).label('tavg'),\
    func.max(Measurement.tobs).label('tmax'), Measurement.date)\
    .filter(Measurement.date >= start).all()

    session.close()
    
    start_tobs_data = []
    for r in results:
        start_tobs_dict = {}
        start_tobs_dict['Trip Date'] = start
        start_tobs_dict['Min Temp'] = r.tmin
        start_tobs_dict['Avg Temp'] = r.tavg
        start_tobs_dict['Max Temp'] = r.tmax
        start_tobs_data.append(start_tobs_dict)
    
    return jsonify(start_tobs_data)


# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>/<end>")
def start_end_trip(start, end):

    session = Session(engine)

    results = session.query(func.min(Measurement.tobs).label('tmin'),\
    func.avg(Measurement.tobs).label('tavg'),\
    func.max(Measurement.tobs).label('tmax'))\
    .filter(Measurement.date >= start)\
    .filter(Measurement.date <= end).all()

    session.close()
    
    start_end_tobs_data = []
    for r in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict['Start Date'] = start
        start_end_tobs_dict['End Date'] = end
        start_end_tobs_dict['Min Temp'] = r.tmin
        start_end_tobs_dict['Avg Temp'] = r.tavg
        start_end_tobs_dict['Max Temp'] = r.tmax
        start_end_tobs_data.append(start_end_tobs_dict)
    
    return jsonify(start_end_tobs_data)

if __name__ == '__main__':
    app.run(debug=True)