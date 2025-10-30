import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

# ---- Step 1: Create a small sample dataset ----
data = {
    'text': [
        "Update your bank account immediately",
        "Your Netflix account has been suspended, click here to fix it",
        "Meeting at 3 PM today",
        "Get free rewards by signing in now",
        "Please find the attached project report",
        "Congratulations! You have won a free iPhone"
    ],
    'label': ['phishing', 'phishing', 'legit', 'phishing', 'legit', 'phishing']
}

df = pd.DataFrame(data)

# ---- Step 2: Split data ----
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.3, random_state=42)

# ---- Step 3: Convert text to numerical form ----
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# ---- Step 4: Train ML model ----
model = LogisticRegression()
model.fit(X_train_vec, y_train)

# ---- Step 5: Test accuracy ----
predictions = model.predict(X_test_vec)
print("Model Accuracy:", accuracy_score(y_test, predictions))

# ---- Step 6: Save model and vectorizer ----
joblib.dump(model, "reports/phishing_model.pkl")
joblib.dump(vectorizer, "reports/vectorizer.pkl")

print("✅ Model and vectorizer saved in reports folder!")
