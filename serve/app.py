import os
import joblib
from flask import Flask, request, jsonify

MODEL_DIR = os.environ.get("MODEL_DIR", "/models")
CLASSES = ["setosa", "versicolor", "virginica"]

app = Flask(__name__)
models = {
    name: joblib.load(os.path.join(MODEL_DIR, f"iris_{name}.joblib"))
    for name in ("rf", "xgb")
}


@app.route("/health")
def health():
    return jsonify(status="ok", models=list(models))


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)
    features = [data["features"]]  # [sepal_l, sepal_w, petal_l, petal_w]
    wanted = data.get("model")  # "rf", "xgb", ou absent = les deux

    if wanted is not None and wanted not in models:
        return jsonify(error=f"model must be one of {list(models)}"), 400

    result = {}
    for name, model in models.items():
        if wanted in (None, name):
            pred = int(model.predict(features)[0])
            result[name] = {"class_id": pred, "class_name": CLASSES[pred]}
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


