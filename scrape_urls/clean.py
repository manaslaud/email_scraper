import pandas as pd
import re

regex = r'calendly\.com/[A-Za-z0-9]+'

input_file = "calendly.com-backlinks_pages.xlsx"  
df = pd.read_excel(input_file)

urls = df.iloc[:, 0]

valid_urls = []
for url in urls:
    if isinstance(url, str):  
        url = re.sub(r'^https://', '', url)
        # Check if the URL matches the regex
        if re.fullmatch(regex, url):
            valid_urls.append(url)

clean_df = pd.DataFrame(valid_urls, columns=["Valid Calendly URLs"])

output_file = "clean_result.xlsx"
clean_df.to_excel(output_file, index=False)

print(f"Valid URLs saved to {output_file}")
