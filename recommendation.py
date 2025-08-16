import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset, Reader, SVD

class RecommenderSystem:
    def __init__(self, df, game_reviews, tfidf_matrix, meta_scaled, asin_to_index):
        self.df = df
        self.game_reviews = game_reviews
        self.tfidf_matrix = tfidf_matrix
        self.meta_scaled = meta_scaled
        self.asin_to_index = asin_to_index

        self.cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        self.meta_cos_sim = cosine_similarity(meta_scaled, meta_scaled)

        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(df[['reviewerID', 'asin', 'overall']], reader)
        trainset = data.build_full_trainset()
        self.algo = SVD(random_state=42)
        self.algo.fit(trainset)

    def save_models(self):
        pickle.dump(self.algo, open("models/svd_model.pkl", "wb"))
        pickle.dump(self.tfidf_matrix, open("models/tfidf.pkl", "wb"))
        pickle.dump(self.meta_scaled, open("models/scaler.pkl", "wb"))
        pickle.dump(self.asin_to_index, open("models/asin_to_index.pkl", "wb"))

    def hybrid_recommend(self, user_id, n=5, alpha=0.5):

        user_games = set(self.df[self.df['reviewerID'] == user_id]['asin'])
        all_games = set(self.df['asin'].unique())
        candidate_games = list(all_games - user_games)

        collab_scores = {g: self.algo.predict(user_id, g).est for g in candidate_games}
        played_idx = [self.asin_to_index[g] for g in user_games if g in self.asin_to_index]
        content_scores = {}

        for g in candidate_games:
            if g in self.asin_to_index and played_idx:
                idx = self.asin_to_index[g]
                sim = np.mean([self.cosine_sim[idx][pidx] for pidx in played_idx])
                content_scores[g] = sim
            else:
                content_scores[g] = 0

        hybrid_scores = {
            g: alpha * collab_scores.get(g, 0) + (1 - alpha) * content_scores.get(g, 0)
            for g in candidate_games
        }

        top_games = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)[:n]
        return [g for g, score in top_games]