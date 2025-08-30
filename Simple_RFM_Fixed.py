# DRAG AND DROP YOUR CSV FILE ONTO THIS SCRIPT
import sys
import os

print("Drag and drop your Online_retail.csv file onto this window, then press Enter...")
file_path = input().strip().replace('"', '')

if os.path.exists(file_path):
    print(f"✅ File found: {file_path}")
    print(f"\nUse this path in your RFM analysis code:")
    print(f'file_path = r"{file_path}"')
else:
    print("❌ File not found. Please try again.")