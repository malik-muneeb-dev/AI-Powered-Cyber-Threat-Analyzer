import pandas as pd

# CSV load karke uske pehle 5 columns aur separator check karein
try:
    # Pehle comma se try karein
    df = pd.read_csv('dataset_malwares.csv', nrows=5)
    print("Columns found with comma (,):")
    print(df.columns.tolist())
    
    # Agar column aik hi nazar aaye, to Pipe (|) try karein
    if len(df.columns) <= 1:
        df = pd.read_csv('dataset_malwares.csv', sep='|', nrows=5)
        print("\nColumns found with Pipe (|):")
        print(df.columns.tolist())
except Exception as e:
    print(f"Error: {e}")