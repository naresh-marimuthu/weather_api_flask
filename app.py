from flask import Flask, render_template
from pathlib import Path
import pandas as pd
import json


app = Flask(__name__)


@app.route("/")
def home():
    df = pd.read_csv("data_small/stations.txt", skiprows=17, dtype=str)
    data = df.to_html()
    #print(data)
    return render_template("home.html", data=data)


@app.route("/api/v1/<station_id>/<date>")
def get_weather(station_id: str, date: str) -> dict:
    """get weather by station_id and date"""
    file_name = "data_small/TG_STAID" + station_id.zfill(6) + ".txt"
    file_path = Path(file_name)

    if file_path.exists():
        df = pd.read_csv(file_name, skiprows=20, parse_dates=['    DATE'])
        df.columns = df.columns.str.strip()
        date = pd.Timestamp(date)
        temprature = df.loc[df["DATE"] == date, "TG"].squeeze()
        
        date = str(date.date())
        temprature = str(temprature)
        print(f"temprature is {temprature}")

        output = {
        "station_id": station_id,
        "date": date,
        "temprature": temprature
        }
        return output
    
    else:
        output = {
            "output": "File Not Found"
        }
        return output


@app.route("/api/v1/<station_id>")
def get_weather_byid(station_id: str) -> dict:
    """get station temprature by id"""
    file_name = f"data_small/TG_STAID{station_id.zfill(6)}.txt"
    file_path = Path(file_name)

    if file_path.exists():
        df = pd.read_csv(file_name, skiprows=20, parse_dates=['    DATE'])
        df.columns = df.columns.str.strip()
        output = df.to_dict(orient='records')
        return output
    else:
        output = {
            "output": "File Not Found"
        }
        return output

    
if __name__ == "__main__":
    app.run(debug=True)