#learn 1

# import json
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# class VectorService:

#     def __init__(self):

#         with open("app/kb/kb.json") as f:
#             self.kb = json.load(f)

#         self.questions = [item["question"] for item in self.kb]

#         self.vectorizer = CountVectorizer()

#         self.kb_vectors = self.vectorizer.fit_transform(self.questions)

#     def search(self, user_message):

#         user_vector = self.vectorizer.transform([user_message])

#         similarity = cosine_similarity(user_vector, self.kb_vectors)

#         best_match_index = similarity.argmax()

#         return self.kb[best_match_index]

# learn 2
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity


# class VectorService:

#     def __init__(self):

#         # Load embedding model
#         self.model = SentenceTransformer('all-MiniLM-L6-v2')

#         # Knowledge base
#         self.kb = [
#             {
#                 "id": "kb_vm_crash",
#                 "question": "vm crashed",
#                 "answer": "Restart the VM from lab dashboard.",
#                 "severity": "HIGH",
#                 "tier": "TIER_2"
#             },
#             {
#                 "id": "kb_login_loop",
#                 "question": "login redirect issue",
#                 "answer": "Clear browser cookies and retry login.",
#                 "severity": "LOW",
#                 "tier": "TIER_1"
#             },
#             {
#                 "id": "kb_container_fail",
#                 "question": "container init failed",
#                 "answer": "Verify container image and restart container.",
#                 "severity": "MEDIUM",
#                 "tier": "TIER_2"
#             }
#         ]

#         # Precompute KB embeddings
#         self.kb_questions = [item["question"] for item in self.kb]
#         self.kb_embeddings = self.model.encode(self.kb_questions)

#     def search(self, query):

#         # Convert query into vector
#         query_embedding = self.model.encode([query])

#         # Compute similarity
#         scores = cosine_similarity(query_embedding, self.kb_embeddings)

#         # Find best match
#         best_index = scores.argmax()

#         return self.kb[best_index]


# learn 3
# 


# learn 4

# import faiss
# import numpy as np
# import json
# from sentence_transformers import SentenceTransformer


# class VectorService:

#     def __init__(self):

#         # Load embedding model
#         self.model = SentenceTransformer("all-MiniLM-L6-v2")

#         # Load KB from file
#         with open("app/kb/kb.json", "r") as f:
#             self.kb = json.load(f)

#         # Extract questions
#         self.kb_questions = [item["question"] for item in self.kb]

#         # Convert questions to embeddings
#         embeddings = self.model.encode(self.kb_questions)

#         # Convert to numpy array
#         self.kb_embeddings = np.array(embeddings).astype("float32")

#         # Create FAISS index
#         dimension = self.kb_embeddings.shape[1]
#         self.index = faiss.IndexFlatL2(dimension)

#         # Add vectors to index
#         self.index.add(self.kb_embeddings)

#     def search(self, query):

#         # Convert query to embedding
#         query_embedding = self.model.encode([query]).astype("float32")

#         # Search FAISS index
#         distances, indices = self.index.search(query_embedding, k=1)

#         best_index = indices[0][0]

#         return self.kb[best_index]


# learn 5
# import faiss
# import numpy as np
# import json
# from sentence_transformers import SentenceTransformer


# class VectorService:

#     def __init__(self):

#         # Load embedding model
#         self.model = SentenceTransformer("all-MiniLM-L6-v2")

#         # Load KB
#         with open("app/kb/kb.json", "r") as f:
#             self.kb = json.load(f)

#         # Extract KB questions
#         self.kb_questions = [item["question"] for item in self.kb]

#         # Create embeddings
#         embeddings = self.model.encode(self.kb_questions)

#         # Convert to numpy float32
#         self.kb_embeddings = np.array(embeddings).astype("float32")

#         # Create FAISS index
#         dimension = self.kb_embeddings.shape[1]
#         self.index = faiss.IndexFlatL2(dimension)

#         # Add vectors to index
#         self.index.add(self.kb_embeddings)


#     def search(self, query):

#         # Convert query to embedding
#         query_embedding = self.model.encode([query]).astype("float32")

#         # Search FAISS
#         distances, indices = self.index.search(query_embedding, k=1)

#         best_index = indices[0][0]
#         best_distance = distances[0][0]

#         result = self.kb[best_index]

#         # Convert distance to confidence
#         confidence = float(1 / (1 + best_distance))

#         return {
#             "id": result["id"],
#             "question": result["question"],
#             "answer": result["answer"],
#             "severity": result["severity"],
#             "tier": result["tier"],
#             "confidence": confidence
#         }


#learn 6

import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer


class VectorService:

    def __init__(self):

        # Load embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Load knowledge base
        with open("app/kb/kb.json", "r") as f:
            self.kb = json.load(f)

        # Extract KB questions
        self.kb_questions = [item["question"] for item in self.kb]

        # Generate embeddings
        embeddings = self.model.encode(self.kb_questions)

        # Convert embeddings to numpy float32
        self.kb_embeddings = np.array(embeddings).astype("float32")

        # Create FAISS index
        dimension = self.kb_embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)

        # Add vectors to index
        self.index.add(self.kb_embeddings)

    def search(self, query):

        # Convert query to embedding
        query_embedding = self.model.encode([query]).astype("float32")

        # Retrieve top 3 KB matches
        distances, indices = self.index.search(query_embedding, k=3)

        results = []

        for i in range(len(indices[0])):

            kb_index = indices[0][i]
            distance = distances[0][i]

            kb_item = self.kb[kb_index]

            confidence = float(1 / (1 + distance))

            results.append({
                "id": kb_item["id"],
                "question": kb_item["question"],
                "answer": kb_item["answer"],
                "severity": kb_item["severity"],
                "tier": kb_item["tier"],
                "confidence": confidence
            })

        # Sort by highest confidence
        results.sort(key=lambda x: x["confidence"], reverse=True)

        return results