import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression 
from sklearn.pipeline import make_pipeline
from sklearn.utils import resample

print("Loading Data...")

try:
    #  DATA LOADING & CLEANING 
    # read the dataset and skip any broken lines
    df = pd.read_csv('data.csv', names=['password', 'strength'], on_bad_lines='skip', low_memory=False)
    
    # convert strength to numbers and handle errors
    df['strength'] = pd.to_numeric(df['strength'], errors='coerce')
    
    # remove any empty rows to clean the data
    df.dropna(subset=['strength', 'password'], inplace=True)
    
    # make sure data types are correct
    df['strength'] = df['strength'].astype(int)
    df['password'] = df['password'].astype(str)

    print(f"Total Clean Data: {len(df)}")

    #  LOGIC APPLICATION
    # mark strength 2 as Strong and everything else as Weak
    df['label'] = df['strength'].apply(lambda x: "Strong" if x == 2 else "Weak")

    print("Labels Distribution (Before Balancing):")
    print(df['label'].value_counts())

    #  DATA BALANCING 
    # separate weak and strong passwords to balance them for resample
    df_weak = df[df['label'] == "Weak"]
    df_strong = df[df['label'] == "Strong"]
    
    min_samples = min(len(df_weak), len(df_strong))
    
    df_weak_balanced = resample(df_weak, replace=False, n_samples=min_samples, random_state=42)
    df_strong_balanced = resample(df_strong, replace=False, n_samples=min_samples, random_state=42)
    
    df_final = pd.concat([df_weak_balanced, df_strong_balanced])
    
    print(f"Balanced Data Ready! Training on: {len(df_final)} passwords")

    X_train, X_test, y_train, y_test = train_test_split(df_final['password'], df_final['label'], test_size=0.2, random_state=42)
    
    print("Training Model using Logistic Regression")

    #  PREPROCESSING & TRAINING 
    # Tfidf: converts text to numbers, LogisticRegression: the actual AI brain
    model = make_pipeline(TfidfVectorizer(analyzer='char'), LogisticRegression(max_iter=1000))
    
    # start training the model
    model.fit(X_train, y_train)
    
    # check how accurate the model is on test data
    accuracy = model.score(X_test, y_test)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    
    # save the trained model as a file
    joblib.dump(model, 'model_feature1.pkl')
    print("Success! Model Saved as 'model_feature1.pkl'")
    
    #  FINAL MANUAL CHECK 
    # test the model with some random passwords
    print("Final Check")
    test_passwords = ["123", "password", "super@12/", "Xy9#mP!2s", "CorrectHorseBattery"]
    
    for pwd in test_passwords:
        pred = model.predict([pwd])[0]
        print(f"Password: {pwd:<20} -> Prediction: {pred}")

except FileNotFoundError:
    print("Error: 'data.csv' file not found!")
except Exception as e:
    print(f"Error Detail: {e}")