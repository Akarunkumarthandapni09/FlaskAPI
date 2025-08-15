# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

# Load cleaned data
df = pd.read_csv("request_types_approvals_clean.csv")

# Encode target labels
df['approval_cat'] = df['approval_flow'].astype('category')
df['label'] = df['approval_cat'].cat.codes
label_map = dict(enumerate(df['approval_cat'].cat.categories))

# Split data
X = df[['request_type','description']]
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Preprocessor
preprocessor = ColumnTransformer([
    ("type", OneHotEncoder(handle_unknown="ignore"), ['request_type']),
    ("desc", TfidfVectorizer(max_features=5000, ngram_range=(1,2)), 'description')
])

# Pipeline
clf = Pipeline([
    ("pre", preprocessor),
    ("model", LogisticRegression(max_iter=1000, class_weight='balanced'))
])

# Train
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

# Report
print(classification_report(y_test, y_pred))

# Save model & label map
joblib.dump(clf, "approval_model.pkl")
joblib.dump(label_map, "label_map.pkl")
print("✅ Model saved as approval_model.pkl")
print("✅ Label map saved as label_map.pkl")
