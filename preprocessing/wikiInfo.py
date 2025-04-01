import pandas as pd
import wikipediaapi
import re


    # Function to clean and extract the mission name from the 'Detail' column
def extract_mission_name(detail):
    # Split the detail string by '|' and take the second part
    parts = detail.split('|')
    if len(parts) > 1:
        mission_name = parts[1].strip()
    else:
        mission_name = detail.strip()
    # Remove any content within parentheses and surrounding whitespace
    mission_name = re.sub(r'\(.*?\)', '', mission_name).strip()
    return mission_name

# Function to fetch the Wikipedia summary for a given mission name
def get_wikipedia_summary(mission_name):
    # Initialize the Wikipedia API
    wiki_wiki = wikipediaapi.Wikipedia(user_agent='vizi (verca.bory@gmail.com)', language='en')

    page = wiki_wiki.page(mission_name)
    if page.exists():
        print(f"✅ Found: {mission_name} → {page.title}: {page.summary[0:200]}")
        return page.summary
    else:
        print(f"Not found: {mission_name}")

    
def robust_wiki_search(mission_detail):
    # 1. Direct search with the full mission detail
    summary = get_wikipedia_summary(mission_detail)
    if summary:
        return summary

    # 2. Component search: split by '|' and search individually
    components = mission_detail.split('|')
    for component in components:
        summary = get_wikipedia_summary(component.strip())
        if summary:
            return summary

    # 3. Further split components into subcomponents and search
    for component in components:
        subcomponents = component.split()
        for length in range(len(subcomponents), 0, -1):
            for start in range(len(subcomponents) - length + 1):
                substring = ' '.join(subcomponents[start:start+length])
                summary = get_wikipedia_summary(substring)
                if summary:
                    return summary

    print(f"❌ No relevant Wikipedia page found for '{mission_detail}'.")
    return ""

# Example usage:
#mission_detail = "Falcon 9 Block 5 | Starlink V1 L9 & BlackSky"
#print("\n\n", robust_wiki_search(mission_detail))


def fetch_wikipedia_summaries(csv_file_path):
    # Load the dataset
    df = pd.read_csv(csv_file_path)

    # Apply the extraction function to create a new column for mission names
    df['Mission_Name'] = df['Detail'].apply(extract_mission_name)

    # Apply the Wikipedia summary fetching function to create a new column
    df['Wikipedia_Summary'] = df['Mission_Name'].apply(get_wikipedia_summary)

    # Select relevant columns to save
    result_df = df[['Unnamed: 0', 'Wikipedia_Summary']]

    # Save the results to a new CSV file
    result_df.to_csv('space_missions_with_summaries.csv', index=False)

    print("Summaries have been successfully fetched and saved to 'space_missions_with_summaries.csv'.")

    
def fetch_wikipedia_summaries_robust(csv_file_path):
    # Load the dataset
    df = pd.read_csv(csv_file_path)

    # Apply the Wikipedia summary fetching function to create a new column
    df['Wikipedia_Summary'] = df['Detail'].apply(robust_wiki_search)


    # Select relevant columns to save
    result_df = df[['Unnamed: 0', 'Wikipedia_Summary']]

    # Save the results to a new CSV file
    result_df.to_csv('space_missions_with_summaries-part.csv', index=False)
    #df.to_csv('space_missions_with_summaries.csv', index=False)

    print("Summaries have been successfully fetched and saved to 'space_missions_with_summaries.csv'.")

# Example usage:
#fetch_wikipedia_summaries('space_missions/Space_Corrected_2001-end.csv')
fetch_wikipedia_summaries_robust('space_missions/Space_Corrected_1-2000.csv')
