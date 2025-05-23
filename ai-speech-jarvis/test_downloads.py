import os

downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
print("Opening:", downloads_path)
os.startfile(downloads_path)
