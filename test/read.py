import pandas as pd

def read_excel(file_path, sheet_name=0):
    try:
        # Read the first column of the Excel file
        df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=[0])  # 0 is the index of the first column
        print(df)  # Optional: Print the DataFrame to verify

        # Access the data in the first column (which is the first column of the sheet)
        for slug in df.iloc[:, 0]:  # `iloc[:, 0]` gets all rows in the first column
            print(slug)  # Print each slug, or process it as needed
            # Call your function to process the slug
            # process_slug(slug)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred (read_excel error): {e}")
        return None

if __name__ == "__main__":
    file_path = "Calendly_data.xlsx"  # Path to your Excel file
    read_excel(file_path)
