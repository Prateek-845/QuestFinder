import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler

def generate_features(clean_csv):
    df = pd.read_csv(clean_csv, parse_dates=['reviewTime'])
    df['reviewText'] = df['reviewText'].fillna('')

    game_reviews = df.groupby('asin')['reviewText'].apply(lambda x: " ".join(x)).reset_index()

    tfidf_vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(game_reviews['reviewText'])

    meta_cols = ['asin', 'review_year', 'review_month', 'review_length', 'summary_length']
    metadata_features = (
        df[meta_cols]
        .drop_duplicates(subset='asin')
        .set_index('asin')
        .fillna(df[meta_cols].mean())
    )

    scaler = StandardScaler()
    meta_scaled = scaler.fit_transform(metadata_features)

    return df, game_reviews, tfidf_vectorizer, tfidf_matrix, metadata_features, meta_scaled, None

if __name__ == "__main__":
    generate_features("data/cleaned_amazon_videogames_reviews_with_titles.csv")
