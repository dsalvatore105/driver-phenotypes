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


# Right now, we have 2 arrays storing the loaded files, names which is just storing the file names, and plt files is storing all of the actual dataframes.
# It is currently filtering the dataframes to only have the rows inbewteen the first gear change and the last gear change.
# I included the timer print statement while loading the files to verify if the files being loaded look correct at a quick glance. 
# If we know it's working fine, we can comment out the timer statements to lessen the processing load.

def main():
    names = []
    plt_files = []
    
    while(True):
        print("1: Load a single drive")
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

                    print(f"Loading: {data_path}", end=" ")

                    try:
                        df = pd.read_csv(data_path, header=None, sep=r'\s+')
                        names.append(data_path.stem)

                        mask = df.loc[:,11] != df.loc[:,11].shift(1) # Only including rows between first gear change and last gear change
                        rows = df[mask]

                        plt_files.append(rows)

                        frame_time = rows.iloc[-1, 53] - rows.iloc[1,53]
                        minute = (frame_time // 60) // 60
                        second = ((frame_time % 60) % 60) % 60

                        print(f"Run time is {minute} minutes and {second} seconds.") 

                    except Exception as e:
                        print(f"Error loading {data_path}: {e}\n")

                else:
                    print(f"The file path was invalid: {data_path}\n")


            case '2':
                study_name = get_Study_Name()
                participant_id = get_Participant_ID()

                data_dir = Path(f"data/{study_name}/{participant_id}")

                for file in data_dir.rglob("*.plt"):
                    if file.stem in names:
                        print(f"Drive {file.stem} has already been loaded")
                        continue
                    try:
                        print(f"Loading {file}", end=" ")
                        df = pd.read_csv(file, header=None, sep=r'\s+')
                        names.append(file.stem)

                        mask = df.loc[:,11] != df.loc[:,11].shift(1) # Only including rows between first gear change and last gear change
                        rows = df[mask]

                        plt_files.append(rows)

                        frame_time = rows.iloc[-1, 53] - rows.iloc[1,53]
                        minute = (frame_time // 60) // 60
                        second = ((frame_time % 60) % 60) % 60

                        print(f"Run time is {minute} minutes and {second} seconds.")

                    except Exception as e:
                        print(f"Error loading {file}: {e}\n")
                        continue


            case'3':

                study_name = get_Study_Name()
                data_dir = Path(f"data/{study_name}")

                for file in data_dir.rglob("*.plt"):
                    if file.stem in names:
                        print(f"Drive {file.stem} has already been loaded")
                        continue

                    try:
                        print(f"Loading {file}", end=" ")
                        df = pd.read_csv(file, header=None, sep=r'\s+')
                        names.append(file.stem)

                        mask = df.loc[:,11] != df.loc[:,11].shift(1) # Only including rows between first gear change and last gear change
                        rows = df[mask]

                        plt_files.append(rows)

                        frame_time = rows.iloc[-1, 53] - rows.iloc[1,53]
                        minute = (frame_time // 60) // 60
                        second = ((frame_time % 60) % 60) % 60

                        print(f"Run time is {minute} minutes and {second} seconds.")

                    except Exception as e:
                        print(f"Error loading {file}: {e}\n")
                        continue



            case '4':
                data_dir = Path("data/")

                for file in data_dir.rglob("*.plt"):
                    if file.stem in names:
                        print(f"Drive {file.stem} has already been loaded")
                        continue

                    try:
                        print(f"Loading {file}", end=" ")
                        df = pd.read_csv(file, header=None, sep=r'\s+')
                        names.append(file.stem)

                        mask = df.loc[:,11] != df.loc[:,11].shift(1) # Only including rows between first gear change and last gear change
                        rows = df[mask]

                        plt_files.append(rows)

                        frame_time = rows.iloc[-1, 53] - rows.iloc[1,53]
                        minute = (frame_time // 60) // 60
                        second = ((frame_time % 60) % 60) % 60

                        print(f"Run time is {minute} minutes and {second} seconds.")
                        
                    except Exception as e:
                        print(f"Error loading {file}: {e}\n")
                        continue

            case 'exit':
                print(f" {len(plt_files)} Files loaded:")
                for n in names:
                    print(n, end=" \n")
                break

if __name__ == "__main__":
    main()