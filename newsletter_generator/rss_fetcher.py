import feedparser
import newspaper
import pandas as pd
import time
import os
from datetime import datetime

class RSSFetcher:
    def __init__(self, rss_urls_file='data/rss_feeds.csv'):
        self.rss_urls = pd.read_csv(rss_urls_file) if os.path.exists(rss_urls_file) else self._create_default_rss_file()
        
    def _create_default_rss_file(self):
        rss_data = {
            'category': [
                'General', 'General', 'General',
                'Technology', 'Technology', 'Technology',
                'Finance', 'Finance', 'Finance',
                'Sports', 'Sports', 'Sports',
                'Entertainment', 'Entertainment', 'Entertainment',
                'Science', 'Science', 'Science'
            ],
            'source': [
                'BBC World News', 'The New York Times', 'Reuters',
                'TechCrunch', 'Wired', 'MIT Technology Review',
                'Bloomberg', 'CNBC', 'Financial Times',
                'ESPN', 'BBC Sport', 'Sky Sports',
                'Variety', 'Hollywood Reporter', 'Billboard',
                'NASA', 'Science Daily', 'Ars Technica Science'
            ],
            'url': [
                'http://feeds.bbci.co.uk/news/world/rss.xml',
                'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
                'http://feeds.reuters.com/reuters/worldNews',
                'https://techcrunch.com/feed/',
                'https://www.wired.com/feed/rss',
                'https://www.technologyreview.com/feed/',
                'https://www.bloomberg.com/feed/podcast/masters-in-business',
                'https://www.cnbc.com/id/100003114/device/rss/rss.html',
                'https://www.ft.com/rss/home',
                'https://www.espn.com/espn/rss/news',
                'http://feeds.bbci.co.uk/sport/rss.xml',
                'https://www.skysports.com/rss/12040',
                'https://variety.com/feed/',
                'https://www.hollywoodreporter.com/feed/',
                'https://www.billboard.com/feed/',
                'https://www.nasa.gov/feed/',
                'https://www.sciencedaily.com/rss/all.xml',
                'https://feeds.arstechnica.com/arstechnica/science'
            ]
        }
        
        df = pd.DataFrame(rss_data)
        os.makedirs('data', exist_ok=True)
        df.to_csv('data/rss_feeds.csv', index=False)
        return df
    
    def fetch_articles(self, max_articles_per_feed=5):
        all_articles = []
        
        for _, row in self.rss_urls.iterrows():
            category = row['category']
            source = row['source']
            url = row['url']
            
            try:
                feed = feedparser.parse(url)
                count = 0
                
                for entry in feed.entries:
                    if count >= max_articles_per_feed:
                        break
                        
                    # Get basic info from RSS
                    article_data = {
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                        'source': source,
                        'category': category
                    }
                    
                    try:
                        article = newspaper.Article(article_data['link'])
                        article.download()
                        article.parse()
                        article_data['text'] = article.text
                        article_data['summary'] = article.text[:200] + '...' if len(article.text) > 200 else article.text
                        
                        # Add to our collection
                        all_articles.append(article_data)
                        count += 1
                        
                    except Exception as e:
                        print(f"Error processing article {article_data['link']}: {e}")
                    
                    # Be nice to servers
                    time.sleep(1)
                    
            except Exception as e:
                print(f"Error fetching feed {url}: {e}")
        
        # Save to CSV
        articles_df = pd.DataFrame(all_articles)
        os.makedirs('data', exist_ok=True)
        articles_df.to_csv(f'data/articles_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv', index=False)
        
        return all_articles
