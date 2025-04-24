import ollama
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# Function to get mission goal with retry logic
def get_mission_goal(row, retries=3):
    try:
        print(f"Processing row {row.name}")
        prompt = f"Can you tell me what was the goal of the space mission '{row}'? I only want to know which of these categories: Earth orbit, Moon, Solar system, Outer space. Answer only one of these words, I am directly creating new dataset from it, so please keep the responses only to these categories. If you cannot find such category, please output None."
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]
    except Exception as e:
        print(f"Error while processing row {row.name}: {e}")
        if retries > 0:
            print(f"Retrying row {row.name}, {retries} retries left.")
            time.sleep(5)  # Delay before retrying
            return get_mission_goal(row, retries - 1)  # Retry the request
        else:
            print(f"Failed to process row {row.name} after retries.")
            return None



# Define file path

file_path = "C:\\Users\\blabl\\Vizualizace\\PA214-Project\\Space_Corrected.csv"
#file_path = "C:\\Users\\blabl\\Vizualizace\\PA214-Project\\.csv"
output_file = "C:\\Users\\blabl\\Vizualizace\\PA214-Project\\Space_Corrected_Extended.csv"



#df = pd.read_csv(file_path, index_col=0, delimiter=',', quotechar='"')

'''
mission_goals = []
for index, row in df.iterrows():
    if (index > -1):
        result = get_mission_goal(row)
        with open("data.txt", "a") as file:
            file.write(f"Processing row {row.name}\n")
            file.write(str(index) + "\n")
            file.write(result + "\n")
        mission_goals.append(result)
        print(index)
        print(result)


df['Mission Goal'] = mission_goals

df.to_csv(output_file, index=False)

    '''

df = pd.read_csv(file_path, index_col=0, delimiter=',', quotechar='"')

with open("current_progress.txt") as input:
    lines = input.readlines()
    print("now0)")
    result = []
    for i in range(0, len(lines), 3):
        l1 = lines[i]
        l2 = lines[i+1]
        l3 = lines[i+2]
        #print(l, l2, l3)
        print(l1)
        print(f"Processing row {int(i/3)}\n")
        assert l1 == f"Processing row {int(i/3)}\n"
        assert l2 == f"{int(i/3)}\n"
        if l3 == " Earth orbit\n":
            result.append("Earth orbit")
        elif l3 == " Moon\n":
            result.append("Moon")
        elif l3 == " Solar system\n":
            result.append("Solar system")
        elif l3 == " Outer space\n":
            result.append("Outer space")
        else:
            result.append("None")

    print(result)

df['Mission Goal'] = result
df.to_csv(output_file, index=False)



    

