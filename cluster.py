import numpy as np
import pandas as pd
import comparisons
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

MEASURES = ["lane_drift", "speed_means", "reaction_times", "collisions", "headway_times", "blinker_wheel", "brake_pressure",
            "brake_peaks", "gas_to_brake", "turning_score", "wheel_movement", "wheel_stopped", "both_pedals"]

TESTS = {
    "Arthritis": ["reaction_times", "lane_drift", "brake_pressure"],
    "Stroke": ["reaction_times", "speed_means", "lane_drift", "headway_times"],
    "Multiple Sclerosis": ["reaction_times", "lane_drift", "wheel_movement", "wheel_stopped"],
    "Pedal Control": ["gas_to_brake", "brake_peaks", "both_pedals", "brake_pressure"],
    "Steering Control": ["turning_score", "wheel_movement", "blinker_wheel"],
}


def participant_table(names, plt_files):
    ids = pd.Index(names).str.extract(r"Sub_(\d+)_Drive")[0]
    df = pd.DataFrame(dict(zip(MEASURES, comparisons.calculate_comparisons(plt_files))), index=ids).groupby(level=0).mean()
    return df.fillna(df.mean()).fillna(0)


def score(df, cols):
    x = StandardScaler().fit_transform(df[cols])
    gmm = GaussianMixture(n_components=2, covariance_type="full", random_state=42, n_init=10).fit(x)
    odd = np.bincount(gmm.predict(x), minlength=2).argmin()
    return pd.Series((gmm.predict_proba(x)[:, odd] * 100).round(), index=df.index)


def test(names, plt_files):
    df = participant_table(names, plt_files)
    if len(df) < 3:
        print("Need at least 3 participants to test.")
        return

    tests = list(TESTS)
    while True:
        print("What would you like to test for?\n")
        for i, t in enumerate(tests, 1):
            print(f"{i}: {t}")
        print("Exit: To Leave This Menu\n")

        choice = input("Enter your choice: ").lower().strip()
        if choice == "exit":
            return
        if choice.isdigit() and 1 <= int(choice) <= len(tests):
            t = tests[int(choice) - 1]
            print(f"\nTesting for {t}...\n")
            out = df[TESTS[t]].round(3).assign(unusual_pct=score(df, TESTS[t])).sort_values("unusual_pct", ascending=False)
            with pd.option_context("display.max_rows", None, "display.width", None):
                print(out)
            return
        print("Invalid choice. Please try again.")
