 
import os

# Specify the directory path
directory_path = '/newfolder'
content=os.listdir(directory_path)
for item in content:
    print(item)
