import pandas as pd # for collecting data in csv,txt formats 
import matplotlib.pyplot as plt #for plotting graphs
import os #for finding/modifying directories
import tkinter as tk
from tkinter import filedialog

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()

# Ask the user to select a folder
folder_path = filedialog.askdirectory(title="Select Folder")

# Check if a folder was selected
if folder_path:
    # Constants for calculations
    c1 = 0.6810762722194764
    c2 = 0.8188224492897056

    try:
        # Read files in the folder
        for file_name in os.listdir(folder_path):
            # Check if the file is a text file
            if file_name.endswith('.txt'):
                file_path = os.path.join(folder_path, file_name)
                
                # Read the data from the file into a DataFrame
                data = pd.read_csv(file_path, sep='\s+', header=None, names=['Field', 'v1f', 'v2f', 'vdc1', 'vdc2'])
        
                # Calculate the ratios
                data['v2f_vdc2'] = data['v2f'] / data['vdc2']
                data['v1f_vdc1'] = data['v1f'] / data['vdc1']
                
                # Calculate Kerr rotation and ellipticity
                data['kerr_rotation'] = c2 * data['v2f_vdc2']
                data['kerr_ellipticity'] = c1 * data['v1f_vdc1']
        
                # Plot Kerr rotation versus field
                plt.figure(figsize=(8, 6))
                plt.plot(data['Field'], data['kerr_rotation'])
                plt.xlabel('Field')
                plt.ylabel('Kerr Rotation')
                plt.title('Kerr Rotation versus Field')
                rotation_image_path = os.path.join(folder_path, f"{file_name.split('.')[0]}_rotation.png")
                plt.savefig(rotation_image_path)  # Save the plot as an image
                plt.show()
        
                # Plot Kerr ellipticity versus field
                plt.figure(figsize=(8, 6))
                plt.plot(data['Field'], data['kerr_ellipticity'])
                plt.xlabel('Field')
                plt.ylabel('Kerr Ellipticity')
                plt.title('Kerr Ellipticity versus Field')
                ellipticity_image_path = os.path.join(folder_path, f"{file_name.split('.')[0]}_ellipticity.png")
                plt.savefig(ellipticity_image_path)  # Save the plot as an image
                plt.show()
        
                # Save the data as an Excel file
                excel_file_path = os.path.join(folder_path, f"{file_name.split('.')[0]}.xlsx")
                data[['Field', 'kerr_rotation', 'kerr_ellipticity']].to_excel(excel_file_path, index=False)
                
    except FileNotFoundError:
        print("Folder not found. Please check the folder path.")
else:
    print("No folder selected.")

