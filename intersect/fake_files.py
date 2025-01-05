# import os
# import pandas as pd

# # Define the
# # directory containing the files
# directory = "intersect/tests"

# # Initialize a list to hold the file data
# data = []

# # Iterate through all files in the directory
# for filename in os.listdir(directory):
#     filepath = os.path.join(directory, filename)
#     if os.path.isfile(filepath):
#         with open(filepath, "r", encoding="utf-8") as file:
#             lines = file.readlines()
#             if lines:
#                 title = lines[0].strip()  # First line as title
#                 text = "".join(lines[1:]).strip()  # Rest as text
#                 data.append({"title": title, "text": text})

# # Create a pandas DataFrame
# df = pd.DataFrame(data)

# # Save the DataFrame as a feather file
# output_path = "output_file.feather"
# df.to_feather(output_path)

# print(f"Data saved to {output_path}")