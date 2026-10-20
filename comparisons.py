def calculate_comparisons(plt_files):
        abs_lane_dev = []
        speed_means = []
        reaction_times = []
        collision_counts = []

        for df in plt_files:
            abs_lane_dev.append(df["Lane_Offset"].abs().mean())

            diff = df["Velocity"] - (df["Speed_Limit"] * 0.44704)
            speed_means.append(diff.abs().mean())

            reaction_times.append(df["Reaction_Time"].mean())

            collision_counts.append(df["Collision"].sum())

        print(f"Absolute Lane Deviation: {abs_lane_dev}\n")
        print(f"Average Speed Limit Adhearance: {speed_means}\n")   
        print(f"Average Reaction Time: {reaction_times}\n")
        print(f"Total Collision Count: {collision_counts}\n")

        return abs_lane_dev, speed_means, reaction_times, collision_counts
