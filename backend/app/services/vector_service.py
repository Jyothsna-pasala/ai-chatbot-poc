import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class VectorService:

    def __init__(self):

        with open("app/kb/kb.json") as f:
            self.kb = json.load(f)

        self.questions = [item["question"] for item in self.kb]

        self.vectorizer = CountVectorizer()

        self.kb_vectors = self.vectorizer.fit_transform(self.questions)

    def search(self, user_message):

        user_vector = self.vectorizer.transform([user_message])

        similarity = cosine_similarity(user_vector, self.kb_vectors)

        best_match_index = similarity.argmax()

        return self.kb[best_match_index]