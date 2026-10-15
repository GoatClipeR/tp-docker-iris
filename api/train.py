import os
import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

MODEL_DIR = os.environ.get("MODEL_DIR", "/models")
os.makedirs(MODEL_DIR, exist_ok=True)

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

models = {
    "rf": RandomForestClassifier(n_estimators=100, random_state=42),
    "xgb": XGBClassifier(n_estimators=100, max_depth=3, random_state=42),
}

for name, model in models.items():
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"[{name}] Accuracy: {acc:.3f}")
    joblib.dump(model, os.path.join(MODEL_DIR, f"iris_{name}.joblib"))
    print(f"[{name}] Modèle sauvegardé dans {MODEL_DIR}/iris_{name}.joblib")


