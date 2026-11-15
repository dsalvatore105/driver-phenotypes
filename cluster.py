import pandas as pd
import comparisons
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler


def test(names, plt_files):
    abs_lane_dev, speed_means, reaction_times, collision_counts, headway_times, blinker_wheel, brake_force, brake_peaks = comparisons.calculate_comparisons(plt_files)
    current_df = None

    while(True):
        print("What would you like to test for?")
        print("\n1: Arthritis")
        print("2: Stroke")
        print("3: Multiple Sclerosis")
        print("Exit: To Leave This Menu\n")
        
        choice = input("Enter your choice: ").lower().strip()

        match choice:
            case '1':
                print("\nTesting for Arthritis...\n")
                current_df = pd.DataFrame({'reaction_times': reaction_times, 'lane_drift': abs_lane_dev, 'brake_pressure': brake_force}, index=names)
                break

            case '2':
                print("\nTesting for Stroke...\n")
                current_df = pd.DataFrame({'reaction_times': reaction_times, 'speed_means': speed_means, 'lane_drift': abs_lane_dev, 'headway_times': headway_times}, index=names)
                break

            case '3':
                print("\nTesting for Multiple Sclerosis...\n")
                current_df = pd.DataFrame({'reaction_times': reaction_times, 'lane_drift': abs_lane_dev, 'brake_pressure': brake_force}, index=names)
                break

            case 'exit':
                return
            
            case _:
                print("Invalid choice. Please try again.")
            
    if current_df is not None and not current_df.empty:
        # Average values of all participants
        key = current_df.index.str.replace(r'_Drive_\d+$', '', regex=True)
        current_df = current_df.groupby(key).mean().round(3)

        if len(current_df) == 1:
            print("Can't test with only one participant.") 

        scaler = StandardScaler()
        scaled_current_df = scaler.fit_transform(current_df)

        # Apply Gaussian Mixture Model with 2 components
        gmm = GaussianMixture(
            n_components=2,
            covariance_type='full',
            random_state=42,
            n_init=10
        )

        gmm.fit(scaled_current_df)
        centroids = gmm.means_
        labels = gmm.predict(scaled_current_df)
        probs = gmm.predict_proba(scaled_current_df)

        results = pd.DataFrame(probs, columns=[f'Cluster {i}' for i in range(gmm.n_components)], index=current_df.index)
        results = results.round(3)
        results.insert(0, 'cluster', labels)

        full = pd.concat([current_df, results], axis=1)
        full = full.sort_values(by='cluster')

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.width', None)

        print(full)
