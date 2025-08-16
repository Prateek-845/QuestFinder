import pandas as pd
import re

def clean_text(text):
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text
    return ''

def preprocess_data(json_path, output_csv):

    df = pd.read_json(json_path, lines=True)
    df['reviewTime'] = pd.to_datetime(df['reviewTime'])
    df = df.dropna(subset=['reviewerID', 'asin', 'overall', 'reviewText'])

    user_counts = df['reviewerID'].value_counts()
    df = df[df['reviewerID'].isin(user_counts[user_counts >= 5].index)]

    game_counts = df['asin'].value_counts()
    df = df[df['asin'].isin(game_counts[game_counts >= 10].index)]

    df = df.drop_duplicates(subset=['reviewerID', 'asin'])

    df['reviewText'] = df['reviewText'].apply(clean_text)
    df['summary'] = df['summary'].apply(clean_text)

    df = df.drop(columns=['vote', 'style', 'image'], errors='ignore')

    df['review_year'] = df['reviewTime'].dt.year
    df['review_month'] = df['reviewTime'].dt.month
    df['review_length'] = df['reviewText'].apply(len)
    df['summary_length'] = df['summary'].apply(len)

    df.to_csv(output_csv, index=False)
    print(f"Data preprocessing complete. Saved to {output_csv}")

if __name__ == "__main__":
    preprocess_data("data/Video_Games_5.json", "data/cleaned_amazon_videogames_reviews.csv")