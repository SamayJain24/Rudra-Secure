import os
import glob
from datetime import datetime
from rss_fetcher import RSSFetcher
from article_processor import ArticleProcessor
from user_manager import UserManager
from newsletter_generator import NewsletterGenerator

def main():
    print("Starting AI-Powered Personalized Newsletter Generator...")
    
    # Step 1: Fetch articles from RSS feeds
    print("Fetching articles from RSS feeds...")
    fetcher = RSSFetcher()
    fetcher.fetch_articles(max_articles_per_feed=5)
    
    # Find the most recent articles file
    articles_files = glob.glob('data/articles_*.csv')
    if not articles_files:
        print("No article files found!")
        return
        
    latest_file = max(articles_files, key=os.path.getctime)
    print(f"Processing the latest article file: {latest_file}")
    
    # Step 2: Process articles with NLP
    print("Processing articles with NLP...")
    processor = ArticleProcessor()
    processed_articles = processor.process_articles(latest_file)
    
    # Step 3: Load user preferences
    print("Loading user preferences...")
    user_manager = UserManager()
    
    # Step 4: Generate personalized newsletters
    print("Generating personalized newsletters...")
    generator = NewsletterGenerator(user_manager)
    generator.generate_newsletters(processed_articles)
    
    print("Newsletter generation complete!")
    print(f"Newsletters saved to the 'output' directory")

if __name__ == "__main__":
    main()