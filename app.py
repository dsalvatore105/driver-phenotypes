import re
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd


from flask import Flask, jsonify, send_file


from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

import comparisons




import main

HERE = Path(__file__).parent


STUDY = HERE / "data" / "FPP"




POINTS = 300

app = Flask(__name__)


def drive_files(pid, drive):
    return sorted(STUDY.joinpath(pid).glob(f"FPP_Sub_{pid}_Drive_{drive}*.plt"))


def squeeze(series):
    step = max(1, len(series) // POINTS)
    return series.groupby(np.arange(len(series)) // step).max().round(3).tolist()


@lru_cache(maxsize=32)
def load_drive(pid, drive):








    names, frames = [], []
    for f in drive_files(pid, drive):
        main.load_data(names, frames, f)
    if not frames:
        return None
    df = frames[0]
    both = comparisons.Both_Pedal_Pressure_Score(df)






    return {
        "brake": squeeze(df["Brake_Pedal_Force"]),
        "gas": squeeze(df["Accelerator_Pedal_Position"]),
        "reaction": squeeze(df["Reaction_Time"]),
        "bothPct": round(both / len(df) * 100, 1),
    }


TESTS = {
    "Arthritis": ["reaction_times", "lane_drift", "brake_pressure"],
    "Stroke": ["reaction_times", "speed_means", "lane_drift", "headway_times"],
}


@lru_cache(maxsize=1)
def cluster_scores():




    names, frames = [], []
    for f in sorted(STUDY.rglob("*.plt")):





        main.load_data(names, frames, f)
    lane, speed, react, _, headway, _, brake, *_ = comparisons.calculate_comparisons(frames)





    df = pd.DataFrame(
        {"reaction_times": react, "lane_drift": lane, "brake_pressure": brake, "speed_means": speed, "headway_times": headway},
        index=pd.Index(names).str.extract(r"Sub_(\d+)_Drive")[0],
    )
    df = df.groupby(level=0).mean()
    df = df.fillna(df.mean())
    out = {pid: {} for pid in df.index}




    for test, cols in TESTS.items():
        x = StandardScaler().fit_transform(df[cols])





        gmm = GaussianMixture(n_components=2, covariance_type="full", random_state=42, n_init=10).fit(x)
        odd = np.bincount(gmm.predict(x), minlength=2).argmin()





        for pid, p in zip(df.index, gmm.predict_proba(x)[:, odd]):
            out[pid][test] = round(p * 100)




    return out


@app.get("/api/clusters")
def clusters():
    return jsonify(cluster_scores())


@app.get("/")
def index():




    return send_file(HERE / "frontend.html")


@app.get("/api/participants")
def participants():
    out = {}
    for d in sorted(p for p in STUDY.iterdir() if p.is_dir()):





        drives = {int(m.group(1)) for f in d.glob("*.plt") if (m := re.search(r"Drive_(\d)", f.name))}
        out[d.name] = sorted(drives)
    return jsonify(out)


@app.get("/api/drive/<pid>/<int:drive>")
def drive(pid, drive):


    
    data = load_drive(pid, drive) if pid.isdigit() else None
    return jsonify(data) if data else ("not found", 404)


if __name__ == "__main__":
    app.run(port=5001)
