import pandas as pd
import joblib 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.utils import resample

print("Loading Data")

try:
    # 1. LOAD DATA
    df = pd.read_csv('phishing_site_urls.csv', on_bad_lines='skip', low_memory=False)
    df.dropna(subset=['URL', 'Label'], inplace=True)
    df['label_name'] = df['Label'].apply(lambda x: "Safe" if x == 'good' else "Phishing")

    # 2. BALANCE DATA 
    df_safe = df[df['label_name'] == "Safe"]
    df_phishing = df[df['label_name'] == "Phishing"]
    
    # 50,000 Safe + 50,000 Phishing = 1,00,000 Total
    n_samples_each = 50000 
    
    df_safe_small = resample(df_safe, replace=False, n_samples=n_samples_each, random_state=42)
    df_phishing_small = resample(df_phishing, replace=False, n_samples=n_samples_each, random_state=42)
    
    df_final = pd.concat([df_safe_small, df_phishing_small])
    print(f"Dataset Balanced: {len(df_final)} URLs ")

    # 3. SPLIT
    X_train, X_test, y_train, y_test = train_test_split(df_final['URL'], df_final['label_name'], test_size=0.2, random_state=42)
    
    # 4. TRAINING
    print("Training Model...")

    model = make_pipeline(
        TfidfVectorizer(), 
        RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1) # use all logical processor of machine 
    )
    
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    print(f" Model Accuracy: {accuracy * 100:.2f}%")
    
    # 5. SAVE
    joblib.dump(model, 'url_model.pkl')
    print("Success! Final Model Saved as 'url_model.pkl'")

except Exception as e:
    print(f"Error: {e}")