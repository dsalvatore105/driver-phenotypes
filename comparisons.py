import numpy as np
from scipy.signal import find_peaks

def calculate_comparisons(plt_files):
        abs_lane_dev = []
        speed_means = []
        reaction_times = []
        collision_counts = []
        headway_times = []
        blinker_wheel = []
        brake_force = []
        brake_peaks = []

        print(f"Calculating Comparisons for {len(plt_files)} files...\n")

        for df in plt_files:
            abs_lane_dev.append(Absolute_Lane_Deviation(df)) # Absolute Lane Deviation

            speed_means.append(Speed_Limit_Adhearance(df)) # Average Speed Limit Adhearance

            reaction_times.append(Reaction_Time(df)) # Average Reaction Time

            collision_counts.append(Collision_Count(df)) # Total Collision Count

            headway_times.append(Car_distance_time(df)) # Average Headway Time

            blinker_wheel.append(Blinker_wheel_turn(df)) # Score of correct wheel movement when blinker is on

            brake_force.append(Average_brake_force(df)) # Avg brake force, only when braking throughout drive

            brake_peaks.append(Repeated_brake_score(df)) # Counting the number of local peaks detected in braking

        #print(f"Absolute Lane Deviation: {abs_lane_dev}\n")
        #print(f"Average Speed Limit Adhearance: {speed_means}\n")   
        #print(f"Average Reaction Time: {reaction_times}\n")
        #print(f"Total Collision Count: {collision_counts}\n")
        #print(f"Average Headway Time: {headway_times}\n")
        #print(f"Blinker Score: {blinker_wheel}\n")
        #print(f"Average Brake Pressure: {brake_force}\n")
        #print(f"Brake Peaks counts: {brake_peaks}\n")


        return abs_lane_dev, speed_means, reaction_times, collision_counts, headway_times, blinker_wheel, brake_force, brake_peaks

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

def Blinker_wheel_turn(df):
     # Score goes up when Left Blinker is on and wheel values go negative and vice versa for right.
     # I didn't include score loss when not turning because turning usually occurs towards the end of the blinker.

     score = 0
     left_positive =((df["Left_Blinker"] > 0) & (df["Steering_Wheel_Position"] < -0.5) ) 
     right_postive = ((df["Right_Blinker"] > 0) & (df["Steering_Wheel_Position"] > 0.5))

     score =+ (left_positive.sum() + right_postive.sum()) 
     return score
          
def Average_brake_force(df):
     temp_df = df[df["Brake_Pedal_Force"] > 0] # Only including when the participant is braking.
     return temp_df["Brake_Pedal_Force"].mean()

def Repeated_brake_score(df): # I believe through this method we should see the lower scores as more a gradual braking, while higher indicates multiple samller braking attempts.
     signal = df["Brake_Pedal_Force"].to_numpy()

     peaks, _ = find_peaks(
          signal,
          prominence= 10, # Difference in score needed to count as a different peak
          distance= 60    # How many frames are needed to seperate peaks
     )

     return len(peaks)
