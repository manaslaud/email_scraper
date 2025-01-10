import pandas as pd
import re

input_file = "p4_unclean.xlsx"
output_file = "clean_result2.xlsx"

df = pd.read_excel(input_file, engine="openpyxl")

urls = df.iloc[:, 0]

# Regex to capture the base slug before any second slash
calendly_regex = r'calendly\.com/([A-Za-z0-9\-]+)'

def filter_and_clean_urls(url):
    if isinstance(url, str):
        # Remove the 'https://' or 'http://' prefix
        url = re.sub(r'^https?://', '', url)
        # Match URL and extract base part before the second slash
        match = re.match(calendly_regex, url)
        if match:
            return f"calendly.com/{match.group(1)}"  # Keep only the base part
    return None

cleaned_urls = urls.apply(filter_and_clean_urls)

cleaned_urls = cleaned_urls.dropna().drop_duplicates()  # Remove duplicates and invalid entries
cleaned_urls.to_frame("Valid Links").to_excel(output_file, index=False, engine="openpyxl")

print(f"Cleaned URLs saved to {output_file}")
