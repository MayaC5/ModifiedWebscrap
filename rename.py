import os

# List all files in the current working directory
files = os.listdir()
i = 1

print("Files in the current directory:", files)

for file in files:
    if file.endswith('.jpg'):
        os.rename(file, f'sweat-hoodie-woman-{i}.jpg')
        i+= 1