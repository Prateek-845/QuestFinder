from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import os
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__)

DATA_PATH = "data/cleaned_amazon_videogames_reviews_with_titles.csv"
MODEL_PATH = "models/svd_model.pkl"
TFIDF_PATH = "models/tfidf.pkl"
ASIN_INDEX_PATH = "models/asin_to_index.pkl"

for path in [DATA_PATH, MODEL_PATH, TFIDF_PATH, ASIN_INDEX_PATH]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Required file missing: {path}")

df = pd.read_csv(DATA_PATH)
algo = pickle.load(open(MODEL_PATH, "rb"))
tfidf_matrix = pickle.load(open(TFIDF_PATH, "rb"))
asin_to_index = pickle.load(open(ASIN_INDEX_PATH, "rb"))
game_titles = dict(zip(df["asin"], df.get("title", pd.Series(["Unknown Title"]*len(df)))))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["GET"])
def recommend():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    user_games = set(df[df["reviewerID"] == user_id]["asin"])
    if not user_games:
        return jsonify({"error": "User ID not found in dataset"}), 404

    all_games = set(df["asin"].unique())
    games_to_predict = list(all_games - user_games)
    predictions = [(game, algo.predict(user_id, game).est) for game in games_to_predict]
    recommendations = [
        {
            "asin": asin,
            "title": game_titles.get(asin, "Unknown Title"),
            "predicted_rating": round(score, 2)
        }
        for asin, score in sorted(predictions, key=lambda x: x[1], reverse=True)[:4]
    ]
    return jsonify({"recommendations": recommendations})

@app.route("/recommend_by_title", methods=["GET"])
def recommend_by_title():
    game_title = request.args.get("title")
    if not game_title:
        return jsonify({"error": "Missing title"}), 400

    matches = df[df['title'].str.lower().str.contains(game_title.lower(), na=False)]
    if matches.empty:
        return jsonify({"error": "Game title not found"}), 404

    asin = matches.iloc[0]['asin']
    idx = asin_to_index.get(asin)
    if idx is None:
        return jsonify({"error": "Game not found in similarity index"}), 404

    cosine_sim = linear_kernel(tfidf_matrix[idx:idx+1], tfidf_matrix).flatten()
    recommendations = [
        {
            "asin": df.iloc[i]['asin'],
            "title": df.iloc[i]['title'],
            "similarity": round(float(score), 3)
        }
        for i, score in sorted(enumerate(cosine_sim), key=lambda x: x[1], reverse=True)[1:5]
    ]
    return jsonify({"recommendations": recommendations})

@app.route("/popular_games", methods=["GET"])
def popular_games():
    popular = (
        df.groupby("asin")
        .agg(review_count=("reviewerID", "count"),
             avg_rating=("overall", "mean"),
             title=("title", "first"))
        .reset_index()
        .sort_values(["review_count", "avg_rating"], ascending=[False, False])
        .head(8)
    )
    games = [
        {
            "title": row.title,
            "asin": row.asin,
            "average_rating": round(row.avg_rating, 2),
            "review_count": int(row.review_count)
        }
        for _, row in popular.iterrows()
    ]
    return jsonify({"games": games})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)