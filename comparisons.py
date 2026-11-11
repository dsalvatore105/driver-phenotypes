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
        Gas_to_brake = []
        Turning_score = []
        Wheel_movement_magnitude = []
        Wheel_when_stopped = []
        Both_pedal_pressure_score = []

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

            Gas_to_brake.append(Gas_To_Brake_Time(df)) # Time spent transitioning from gas to brake

            Turning_score.append(Turning_Score(df)) # Score for correct turning behavior

            Wheel_movement_magnitude.append(Wheel_Movement_Magnitude(df)) # Magnitude of steering wheel movement

            Wheel_when_stopped.append(Wheel_When_Stopped(df)) # Steering wheel position when stopped

            Both_pedal_pressure_score.append(Both_Pedal_Pressure_Score(df)) # Score for pressing both pedals

        #print(f"Absolute Lane Deviation: {abs_lane_dev}\n")
        #print(f"Average Speed Limit Adhearance: {speed_means}\n")   
        #print(f"Average Reaction Time: {reaction_times}\n")
        #print(f"Total Collision Count: {collision_counts}\n")
        #print(f"Average Headway Time: {headway_times}\n")
        #print(f"Blinker Score: {blinker_wheel}\n")
        #print(f"Average Brake Pressure: {brake_force}\n")
        #print(f"Brake Peaks counts: {brake_peaks}\n")
        print(f"Gas to Brake Time: {Gas_to_brake}\n")
        print(f"Turning Score: {Turning_score}\n")
        #print(f"Wheel Movement Magnitude: {Wheel_movement_magnitude}\n")
        #print(f"Wheel When Stopped: {Wheel_when_stopped}\n")
        print(f"Both Pedal Pressure Score: {Both_pedal_pressure_score}\n")


        return abs_lane_dev, speed_means, reaction_times, collision_counts, headway_times, blinker_wheel, brake_force, brake_peaks, Gas_to_brake, Turning_score, Wheel_movement_magnitude, Wheel_when_stopped, Both_pedal_pressure_score

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
    temp_df = df[df["Headway_Time"] <= 5] # Search for rows where Headway Time is less than or equal to 5 seconds. 3 seconds is the safe following distance, but some people would go above that
    return temp_df["Headway_Time"].mean() 

def Blinker_wheel_turn(df):
    # Score goes up when Left Blinker is on and wheel values go negative and vice versa for right
    # I didn't include score loss when not turning because turning usually occurs towards the end of the blinker

    score = 0
    left_positive =((df["Left_Blinker"] > 0) & (df["Steering_Wheel_Position"] < -0.5)) 
    right_postive = ((df["Right_Blinker"] > 0) & (df["Steering_Wheel_Position"] > 0.5))

    score =+ (left_positive.sum() + right_postive.sum()) 
    return score
          
def Average_brake_force(df):
    temp_df = df[df["Brake_Pedal_Force"] > 0] # Only including when the participant is braking
    return temp_df["Brake_Pedal_Force"].mean()

def Repeated_brake_score(df): # I believe through this method we should see the lower scores as more a gradual braking, while higher indicates multiple smaller braking attempts
    signal = df["Brake_Pedal_Force"].to_numpy()

    peaks, _ = find_peaks(
        signal,
        prominence= 10, # Difference in score needed to count as a different peak
        distance= 60    # How many frames are needed to seperate peaks
    )

    return len(peaks)

def Gas_To_Brake_Time(df):
    df_gas = df["Accelerator_Pedal_Position"] > 2.0 # Only including when the participant is pressing the gas pedal
    df_brake = df["Brake_Pedal_Force"] > 0 # Only including when the participant is pressing the brake pedal

    gas_releases = df_gas.shift(fill_value= False) & ~df_gas # When the gas pedal is released
    brake_presses = df_brake & ~df_brake.shift(fill_value= False) # When the brake pedal is pressed

    release_indices = df.loc[gas_releases, "Frame_Number"].tolist()
    brake_indices = df.loc[brake_presses, "Frame_Number"].tolist()

    transition_times = []

    for release_indice in release_indices:

        next_brake = [b for b in brake_indices if b > release_indice]

        if next_brake:
            frame_diff = next_brake[0] - release_indice
            if frame_diff > 0 and frame_diff < 300:  # Only include transitions that are less than 300 frames (5 seconds)
                transition_times.append(frame_diff)

    if not transition_times:
        return 0
    
    return sum(transition_times) / len(transition_times)

def Turning_Score(df):
    df_turn = df["Steering_Wheel_Position"].abs() > 0.4 # Find turns
    df_turn_grouped = (df_turn != df_turn.shift()).cumsum() # Grouping the rows where the participant is turning

    turns = df.loc[df_turn].groupby(df_turn_grouped[df_turn])["Frame_Number"] # Determine start and end of each turn

    turn_times = turns.max() - turns.min() # Calculating the time spent turning for each turn

    average_turn_time = turn_times.mean() # Average time spent turning

    return average_turn_time # Should return the average amount of frames spent turning on turns above 0.4 radians

def Wheel_Movement_Magnitude(df):
    return df["Steering_Wheel_Position"].diff().abs().mean()

def Wheel_When_Stopped(df):
    df_stopped = df[df["Acceleration"].abs() < 0.1] # Only including when the participant is stopped
    wheel_movement = df_stopped["Steering_Wheel_Position"].diff().abs().mean()
    return wheel_movement

def Both_Pedal_Pressure_Score(df):
    df_both = df[(df["Brake_Pedal_Force"] > 0.5) & (df["Accelerator_Pedal_Position"] > 1.0)] # Only including when the participant is pressing both pedals
    return len(df_both)