from data_preprocessing import preprocess_data
from feature_engineering import generate_features
from recommendation import RecommenderSystem
import pandas as pd
import os

if __name__ == "__main__":
    preprocess_data("data/Video_Games_5.json", "data/cleaned_amazon_videogames_reviews.csv")

    meta_path = "data/meta_Video_Games.json"
    reviews_path = "data/cleaned_amazon_videogames_reviews.csv"
    merged_path = "data/cleaned_amazon_videogames_reviews_with_titles.csv"

    if os.path.exists(meta_path):
        meta_df = pd.read_json(meta_path, lines=True)[['asin', 'title']]
        reviews_df = pd.read_csv(reviews_path)
        merged_df = pd.merge(reviews_df, meta_df, on='asin', how='left')
        merged_df.to_csv(merged_path, index=False)
        print(f"Merged CSV with titles saved to {merged_path}")
    else:
        raise FileNotFoundError(f"Metadata file {meta_path} not found. Cannot add titles.")

    df, game_reviews, tfidf_vectorizer, tfidf_matrix, metadata_features, meta_scaled, _ = generate_features(merged_path)
    asin_to_index = pd.Series(game_reviews.index, index=game_reviews['asin'])

    recommender = RecommenderSystem(df, game_reviews, tfidf_matrix, meta_scaled, asin_to_index)
    recommender.save_models()

    # Example
    sample_user = df['reviewerID'].iloc[0]
    print("Hybrid Recommendations:", recommender.hybrid_recommend(sample_user))