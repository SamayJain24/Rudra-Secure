import pandas as pd
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class UserManager:
    def __init__(self, users_file='data/users.json'):
        self.users_file = users_file
        self.users = self._load_users()
        
    def _load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                return json.load(f)
        else:
            # Create default users based on project specifications
            default_users = {
                "alex_parker": {
                    "name": "Alex Parker",
                    "age": 28,
                    "country": "USA",
                    "interests": ["AI", "cybersecurity", "blockchain", "startups", "programming"],
                    "sources": ["TechCrunch", "Wired Tech", "Ars Technica", "MIT Tech Review"]
                },
                "priya_sharma": {
                    "name": "Priya Sharma",
                    "age": 35,
                    "country": "India",
                    "interests": ["Global markets", "startups", "fintech", "cryptocurrency", "economics"],
                    "sources": ["Bloomberg", "Financial Times", "Forbes", "CoinDesk"]
                },
                "marco_rossi": {
                    "name": "Marco Rossi",
                    "age": 30,
                    "country": "Italy",
                    "interests": ["Football", "F1", "NBA", "Olympic sports", "esports"],
                    "sources": ["ESPN", "BBC Sport", "Sky Sports F1", "The Athletic"]
                },
                "lisa_thompson": {
                    "name": "Lisa Thompson",
                    "age": 24,
                    "country": "UK",
                    "interests": ["Movies", "celebrity news", "TV shows", "music", "books"],
                    "sources": ["Variety", "Rolling Stone", "Billboard", "Hollywood Reporter"]
                },
                "david_martinez": {
                    "name": "David Martinez",
                    "age": 40,
                    "country": "Spain",
                    "interests": ["Space exploration", "AI", "biotech", "physics", "renewable energy"],
                    "sources": ["NASA", "Science Daily", "Nature", "Ars Technica Science"]
                }
            }
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
            
            # Save to file
            with open(self.users_file, 'w') as f:
                json.dump(default_users, f, indent=4)
                
            return default_users
            
    def calculate_article_relevance(self, user_id, article, vectorizer):
        # Calculate how relevant an article is to a user's interests
        if user_id not in self.users:
            return 0
            
        user = self.users[user_id]
        
        # Source match score (direct match with user's preferred sources)
        source_score = 0
        if article['source'] in user['sources']:
            source_score = 0.5  # Weight for source match
            
        # Interest match score using TF-IDF and cosine similarity
        user_interests = " ".join(user['interests'])
        
        # Create document matrix from user interests and article text
        documents = [user_interests, article['processed_text']]
        
        # Vectorize (only if there's content to compare)
        if documents[0] and documents[1]:
            tfidf_matrix = vectorizer.fit_transform(documents)
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        else:
            similarity = 0
            
        # Combine scores (weight interest match more heavily)
        total_score = source_score + (similarity * 0.5)
        
        return total_score
        
    def get_user(self, user_id):
        # Get a specific user by ID
        return self.users.get(user_id)
        
    def get_all_users(self):
        # Get all users
        return self.users
