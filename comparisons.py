def Absolute_lane_deviation(plt_files):
        abs_lane_dev = []
        for df in plt_files:
            abs_lane_dev.append(df["Lane_Offset"].abs().mean())

        print(f"Absolute Lane Deviation: {abs_lane_dev}\n")
        return abs_lane_dev


def Average_speed_limit_adhearance(plt_files):
        speed_means = []
        for df in plt_files:
            diff = df["Velocity"] - (df["Speed_Limit"] * 0.44704)

            speed_means.append(diff.abs().mean())

        print(f"Average Speed Limit Adhearance: {speed_means}\n")
        return speed_means


def Average_reaction_time(plt_files):
        reaction_times = []
        for df in plt_files:
            reaction_times.append(df["Reaction_Time"].mean())

        print(f"Average Reaction Time: {reaction_times}\n")
        return reaction_times