
---

# AI-Powered Personalized Newsletter Generator

An AI-driven system that curates and delivers personalized newsletters based on user preferences. The project fetches articles from various RSS feeds, processes them using NLP techniques, and generates customized Markdown newsletters for each user.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project implements an automated newsletter generation system. It includes:

1. **Fetching Articles:** Uses RSS feeds to collect articles from various news sources.
2. **NLP Processing:** Cleans, normalizes, and processes article text using NLP (TF-IDF, cosine similarity, and keyword extraction).
3. **User Personalization:** Matches articles to user preferences based on interests and preferred news sources.
4. **Newsletter Generation:** Creates personalized newsletters in Markdown format that include summaries, category-wise grouping, and hyperlinked article references.

## Features

- **Automated Data Retrieval:** Fetches articles from predefined RSS feeds.
- **Natural Language Processing:** Cleans and processes text to extract keywords and compute relevance scores.
- **User-Based Personalization:** Calculates article relevance based on users' interests and preferred sources.
- **Markdown Output:** Generates newsletters with clear sections, summaries, and links to full articles.
- **Extensible Design:** Modular architecture allows easy updates to the article processing and newsletter formatting logic.

## Project Structure

```
newsletter_generator/
├── main.py                      # Entry point of the application
├── rss_fetcher.py               # Handles RSS feed parsing and article fetching
├── article_processor.py         # Implements NLP for article processing
├── user_manager.py              # Manages user data and preferences
├── newsletter_generator.py      # Generates personalized newsletters in Markdown
├── requirements.txt             # List of required libraries
├── data/                        # Stores RSS feeds and fetched article CSVs (auto-created)
└── output/                      # Stores generated Markdown newsletters (auto-created)
```

- **main.py:** Orchestrates the overall process (fetching, processing, personalization, and newsletter generation).
- **rss_fetcher.py:** Retrieves articles from various RSS feeds and saves the output in CSV format under the `data` directory.
- **article_processor.py:** Applies text preprocessing, TF-IDF vectorization, and keyword extraction on fetched articles.
- **user_manager.py:** Loads user profiles (or creates default ones) and computes relevance scores for each article based on user preferences.
- **newsletter_generator.py:** Sorts articles by relevance and generates personalized newsletters in Markdown format, saving them in the `output` directory.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your_username/newsletter_generator.git
   cd newsletter_generator
   ```

2. **Create the project environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install the required libraries:**

   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` should include:
   - feedparser
   - newspaper3k
   - nltk
   - scikit-learn
   - pandas

## Usage

To run the newsletter generator, execute the following command from the project root:

```bash
python main.py
```

This will:
- Fetch articles from RSS feeds.
- Process the articles with NLP techniques.
- Load user preferences.
- Generate personalized newsletters as Markdown files in the `output` directory.

## Testing

After running the program:
1. Check the `output` directory for the generated newsletter Markdown files.
2. Open a newsletter file to verify:
   - A header with the user's name and generation date.
   - A "Today's Highlights" section summarizing top articles.
   - Categorized sections with article titles, summaries, links, and keywords.
3. Compare the newsletter content with the user preferences to ensure accurate personalization.

## Dependencies

The project requires the following libraries:

- **feedparser:** For parsing RSS feeds.
- **newspaper3k:** For article extraction and parsing.
- **nltk:** For natural language processing (tokenization, stopwords, lemmatization).
- **scikit-learn:** For TF-IDF vectorization and cosine similarity computations.
- **pandas:** For data handling and CSV operations.

Ensure these are installed by running:

```bash
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request with improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to adjust any sections as needed to better suit your project details. Happy coding!
