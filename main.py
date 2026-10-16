import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn
from pathlib import Path

def get_Study_Name():
    study_name = input("Enter the study name: ").upper().replace(" ", "")
    return study_name

def get_Participant_ID():
    participant_id = input("Enter the participant ID: ")
    return participant_id

def get_Drive():
    drive_path = input("Enter the drive number: ")
    return drive_path

def load_data(names, plt_files, file):
    try:
        print(f"Loading {file} |", end=" ")
        df = pd.read_csv(file, header=None, sep=r'\s+')
        names.append(file.stem)

        mask = df.loc[:,11] != df.loc[:,11].shift(1) # Only including rows between first gear change and last gear change
        mask.iloc[0] = False 
        gear_change_indices = df.index[mask]

        if len(gear_change_indices) >= 2:
            first_gear_change_index = gear_change_indices[0]
            last_gear_change_index = gear_change_indices[-1]

            rows = df.loc[first_gear_change_index:last_gear_change_index].copy()
            plt_files.append(rows)
            print(f"Number of frames: {len(rows)} |", end=" ")

            calc_runtime(len(rows))
        
    except Exception as e:
        print(f"Error loading {file}: {e}\n")

def calc_runtime(frame_number):
    minute = (frame_number // 60) // 60
    second = ((frame_number % 60) % 60) % 60

    print(f"Run time is {minute} minutes and {second} seconds.")

# Right now, we have 2 arrays storing the loaded files, names which is just storing the file names, and plt files is storing all of the actual dataframes.
# It is currently filtering the dataframes to only have the rows inbewteen the first gear change and the last gear change.
# I included the timer function while loading the files to verify if the files being loaded look correct at a quick glance. 
# If we know it's working fine, we can comment out the timer function to lessen the processing load.

def main():
    names = []
    plt_files = []
    
    while(True):
        print("\n1: Load a single drive")
        print("2: Load all drives of a participant")
        print("3: Load all drives in a study")
        print("4: Load all drives")
        print("Exit: To Close the Program\n")

        choice = input("Enter your choice: ")

        match choice:
            case '1':
                study_name = get_Study_Name()
                participant_id = get_Participant_ID()
                drive_path = get_Drive()

                data_path = Path(f"data/{study_name}/{participant_id}/{study_name}_Sub_{participant_id}_Drive_{drive_path}.plt")

                if data_path.exists():
                    if data_path.stem in names:
                        print(f"Drive {data_path.stem} has already been loaded")
                        continue

                    load_data(names, plt_files, data_path)


            case '2':
                study_name = get_Study_Name()
                participant_id = get_Participant_ID()

                data_dir = Path(f"data/{study_name}/{participant_id}")

                for file in data_dir.rglob("*.plt"):
                    if file.stem in names:
                        print(f"Drive {file.stem} has already been loaded")
                        continue
                    
                    load_data(names, plt_files, file)


            case'3':

                study_name = get_Study_Name()
                data_dir = Path(f"data/{study_name}")

                for file in data_dir.rglob("*.plt"):
                    if file.stem in names:
                        print(f"Drive {file.stem} has already been loaded")
                        continue
                    
                    load_data(names, plt_files, file)



            case '4':
                data_dir = Path("data/")

                for file in data_dir.rglob("*.plt"):
                    if file.stem in names:
                        print(f"Drive {file.stem} has already been loaded")
                        continue

                    load_data(names, plt_files, file)


            case 'exit':
                print(f" {len(plt_files)} Files loaded:")
                for n in names:
                    print(n, end=" \n")
                break

if __name__ == "__main__":
    main()