import tkinter as tk
from tkinter import filedialog
import pandas as pd


class FileSelector:

    def select_file(self, title="Select a file"):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title=title)
    
        if not file_path:
            raise FileNotFoundError("No file selected.")
        
        if not file_path.endswith('.csv'):
            raise ValueError("Invalid file format. Please select a CSV file.")
        
        return file_path
    
    def select_folder(self, title="Select a folder"):
        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory(title=title)
    
        if not folder_path:
            raise FileNotFoundError("No folder selected.")
        
        return folder_path
        

    def load_file(self, file_path):
        try:
            df = pd.read_csv(file_path, encoding="latin1", sep=";")
            for column in df.columns:
                if 'fecha' in column.lower():
                    df[column] = pd.to_datetime(df[column], errors='coerce', infer_datetime_format=True)
        
        except Exception as e:
            raise ValueError(f"Error loading file: {e}")
        return df
    

    def load_validations(self, file_path):
        try:
            df_validations = pd.read_csv(file_path, encoding="latin1", sep=";")
            validations_dict = [(row[0], row[1]) for _, row in df_validations.iterrows()]
        except Exception as e:
            raise ValueError(f"Error loading validations: {e}")
        return validations_dict
    