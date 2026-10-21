def calculate_comparisons(plt_files):
        abs_lane_dev = []
        speed_means = []
        reaction_times = []
        collision_counts = []
        headway_times = []

        print(f"Calculating Comparisons for {len(plt_files)} files...\n")

        for df in plt_files:
            abs_lane_dev.append(Absolute_Lane_Deviation(df)) # Absolute Lane Deviation

            speed_means.append(Speed_Limit_Adhearance(df)) # Average Speed Limit Adhearance

            reaction_times.append(Reaction_Time(df)) # Average Reaction Time

            collision_counts.append(Collision_Count(df)) # Total Collision Count

            headway_times.append(Car_distance_time(df)) # Average Headway Time

        #print(f"Absolute Lane Deviation: {abs_lane_dev}\n")
        #print(f"Average Speed Limit Adhearance: {speed_means}\n")   
        #print(f"Average Reaction Time: {reaction_times}\n")
        #print(f"Total Collision Count: {collision_counts}\n")
        #print(f"Average Headway Time: {headway_times}\n")


        return abs_lane_dev, speed_means, reaction_times, collision_counts, headway_times

def Absolute_Lane_Deviation(df):
    return df["Lane_Offset"].abs().mean() # Absolute Lane Deviation

def Speed_Limit_Adhearance(df):
    diff = df["Velocity"] - (df["Speed_Limit"] * 0.44704) # Speed Limit Adhearance
    return diff.abs().mean()

def Reaction_Time(df):
    return df["Reaction_Time"].mean() # Average Reaction Time

def Collision_Count(df):
    return df["Collision"].sum() # Total Collision Count

def Car_distance_time(df):
    temp_df = df[df["Headway_Time"] <= 5] # Search for rows where Headway Time is less than or equal to 5 seconds. 3 seconds is the safe following distance, but some people would go above that.
    return temp_df["Headway_Time"].mean() 

def Blinker_Wheel_turn(df):
     temp_df = df[df["Left_Blinker"] > 0 | df["Right_Blinker"] > 0] # Search for rows where either the left or right blinker is on