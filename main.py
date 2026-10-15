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

                    print(f"Loading: {data_path}\n")

                    try:
                        df = pd.read_csv(data_path, header=None, sep=r'\s+')
                        names.append(data_path.stem)
                        plt_files.append(df)
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
                        print(f"Loading {file}")
                        df = pd.read_csv(file, header=None, sep=r'\s+')
                        names.append(file.stem)
                        plt_files.append(df)
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
                        print(f"Loading {file}")
                        df = pd.read_csv(file, header=None, sep=r'\s+')
                        names.append(file.stem)
                        plt_files.append(df)
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
                        print(f"Loading {file}")
                        df = pd.read_csv(file, header=None, sep=r'\s+')
                        names.append(file.stem)
                        plt_files.append(df)

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