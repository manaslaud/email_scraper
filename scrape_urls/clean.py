import pandas as pd
import re

input_file = "calendly.com-backlinks_pages.xlsx" 
output_file = "clean_result.xlsx"

df = pd.read_excel(input_file, engine="openpyxl")

urls = df.iloc[:, 0]  

profile_regex = r'calendly\.com/[A-Za-z0-9]+'
time_slot_regex = r'calendly\.com/([A-Za-z0-9]+)/\d+min'

def filter_and_clean_urls(url):
    if isinstance(url, str): 
        # Remove the 'https://' prefix
        url = re.sub(r'^https?://', '', url)
        time_slot_match = re.match(time_slot_regex, url)
        if time_slot_match:
            return f"calendly.com/{time_slot_match.group(1)}/"  # Extract the base URL
        profile_match = re.match(profile_regex, url)
        if profile_match:
            return f"{profile_match.group(0)}/"
    return None  

cleaned_urls = urls.apply(filter_and_clean_urls)

cleaned_urls = cleaned_urls.dropna().drop_duplicates()  # Remove duplicates and invalid entries
cleaned_urls.to_frame("Valid Links").to_excel(output_file, index=False, engine="openpyxl")

print(f"Cleaned URLs saved to {output_file}")
