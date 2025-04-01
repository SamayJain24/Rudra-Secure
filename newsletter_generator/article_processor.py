import nltk
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class ArticleProcessor:
    def __init__(self):
        # Download necessary NLTK resources
        try:
            nltk.data.find('corpora/stopwords')
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('stopwords')
            nltk.download('wordnet')
            nltk.download('punkt')
        
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.vectorizer = TfidfVectorizer(max_features=5000)
        
    def preprocess_text(self, text):
        if not isinstance(text, str):
            return ""
            
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = re.sub(f'[{string.punctuation}]', ' ', text)
        
        # Remove numbers
        text = re.sub(r'\d+', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Tokenize
        tokens = nltk.word_tokenize(text)
        
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens if word not in self.stop_words]
        
        return ' '.join(tokens)
    
    def process_articles(self, articles_file):
        articles_df = pd.read_csv(articles_file)
        articles_df['processed_text'] = articles_df['text'].apply(self.preprocess_text)
        
        # Create TF-IDF vectors
        tfidf_matrix = self.vectorizer.fit_transform(articles_df['processed_text'])
        articles_df['tfidf_vector'] = list(tfidf_matrix.toarray())
        
        # Extract keywords
        self.extract_keywords(articles_df)
        
        # Save processed data
        articles_processed_file = articles_file.replace('.csv', '_processed.csv')
        
        # Save without the vector column (it's not easily saved to CSV)
        save_df = articles_df.drop(columns=['tfidf_vector'])
        save_df.to_csv(articles_processed_file, index=False)
        
        return articles_df
    
    def extract_keywords(self, articles_df, num_keywords=5):
        keywords_list = []
        
        for _, row in articles_df.iterrows():
            text = row['processed_text']
            if not text:
                keywords_list.append([])
                continue
                
            # Simple frequency approach for keyword extraction
            words = text.split()
            word_freq = {}
            
            for word in words:
                if len(word) > 3:  # Only consider words longer than 3 characters
                    if word in word_freq:
                        word_freq[word] += 1
                    else:
                        word_freq[word] = 1
            
            # Get top words
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            keywords = [word for word, _ in sorted_words[:num_keywords]]
            keywords_list.append(keywords)
        
        articles_df['keywords'] = keywords_list
