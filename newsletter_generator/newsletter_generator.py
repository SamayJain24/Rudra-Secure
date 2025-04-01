import os
import pandas as pd
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer

class NewsletterGenerator:
    def __init__(self, user_manager):
        self.user_manager = user_manager
        self.vectorizer = TfidfVectorizer(max_features=5000)
        
    def generate_newsletters(self, processed_articles, output_dir='output'):
        # Generate personalized newsletters for all users
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Get all users
        users = self.user_manager.get_all_users()
        
        # Process for each user
        for user_id, user in users.items():
            self._generate_user_newsletter(user_id, user, processed_articles, output_dir)
        
    def _generate_user_newsletter(self, user_id, user, processed_articles, output_dir):
        # Generate a newsletter for a specific user
        # Calculate relevance score for each article
        article_scores = []
        
        for _, article in processed_articles.iterrows():
            score = self.user_manager.calculate_article_relevance(user_id, article, self.vectorizer)
            article_scores.append({
                'article': article,
                'score': score
            })
            
        # Sort by relevance score
        article_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Select top articles (e.g., top 10)
        top_articles = article_scores[:10]
        
        # Generate newsletter in Markdown format
        newsletter_content = self._format_newsletter(user, top_articles)
        
        # Save to file
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"{output_dir}/{user_id}_newsletter_{date_str}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(newsletter_content)
            
        return filename
        
    def _format_newsletter(self, user, top_articles):
        # Format the newsletter in Markdown
        # Newsletter header
        now = datetime.now().strftime("%B %d, %Y")
        content = f"# Personalized Newsletter for {user['name']}\n\n"
        content += f"**Generated on:** {now}\n\n"
        
        # Summary of top stories
        content += "## Today's Highlights\n\n"
        for i, item in enumerate(top_articles[:3]):
            article = item['article']
            content += f"{i+1}. **{article['title']}** - {article['summary'][:100]}...\n"
        
        content += "\n---\n\n"
        
        # Organize articles by category
        categories = {}
        for item in top_articles:
            article = item['article']
            category = article['category']
            
            if category not in categories:
                categories[category] = []
                
            categories[category].append(article)
        
        # Add articles by category
        for category, articles in categories.items():
            content += f"## {category} News\n\n"
            
            for article in articles:
                content += f"### {article['title']}\n\n"
                content += f"{article['summary']}\n\n"
                content += f"[Read more]({article['link']})\n\n"
                
                # Add keywords if available
                if isinstance(article['keywords'], list) and article['keywords']:
                    # Handle string representation of a list if needed
                    keywords = article['keywords']
                    if isinstance(keywords, str):
                        try:
                            keywords = eval(keywords)
                        except:
                            keywords = [keywords]
                            
                    if keywords:
                        content += f"**Keywords:** {', '.join(keywords)}\n\n"
                
                content += "---\n\n"
        
        # Footer
        content += f"This newsletter was personalized for {user['name']} based on their interests: "
        content += f"{', '.join(user['interests'])}\n"
        
        return content
