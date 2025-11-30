# Customer Experience Analytics for Fintech Apps

## Overview

This project focuses on analyzing customer experiences for Ethiopian fintech applications by scraping Google Play Store reviews for three major banks: Commercial Bank of Ethiopia (CBE), Dashen Bank, and Awash International Bank. The workflow includes data scraping, preprocessing, sentiment analysis, thematic analysis, database storage, and visualization of insights to understand user feedback and improve app performance.

The project is structured into three main branches/tasks:

- **task-1**: Scraping & raw data collection
- **task-2**: Preprocessing & analysis (sentiment and thematic)
- **task-3**: Database load and final visualization

## Features

- **Data Scraping**: Automated scraping of Google Play reviews using the `google-play-scraper` library.
- **Data Preprocessing**: Cleaning, deduplication, and normalization of raw review data.
- **Sentiment Analysis**: Utilizes advanced NLP models (Transformers and VADER) to classify review sentiments.
- **Thematic Analysis**: Extracts top keywords per bank using TF-IDF and assigns themes based on rule-based keyword matching.
- **Database Integration**: Stores processed data in a PostgreSQL database for efficient querying and analysis.
- **Visualization**: Generates insightful charts and graphs to visualize rating distributions, sentiment counts, and top themes.
- **Modular Codebase**: Organized scripts and notebooks for easy maintenance and extension.

## Project Structure

```
.
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .gitignore                # Git ignore rules
├── data/
│   ├── raw/                  # Raw scraped data (e.g., CBE_raw.csv, Dashen_raw.csv)
│   ├── cleaned/              # Preprocessed and cleaned data (all_reviews_clean.csv)
│   └── processed/            # Analyzed data with sentiment/themes and figures
│       ├── all_reviews_with_sentiment.csv
│       ├── all_reviews_with_themes.csv
│       ├── top_keywords_per_bank.csv
│       └── figures/          # Generated visualizations (e.g., rating_distribution.png)
├── docs/                     # Additional documentation
├── notebooks/                # Jupyter notebooks for exploration and visualization
│   ├── Task_1.ipynb          # Initial data exploration
│   ├── Task_2.ipynb          # Analysis notebook
│   └── Visualization.ipynb   # Visualization scripts
├── sql/
│   └── create_schema.sql     # PostgreSQL database schema
└── src/                      # Source code scripts
    ├── scrape_reviews.py     # Scrapes Google Play reviews
    ├── preprocess.py         # Cleans and preprocesses data
    ├── sentiment_pipeline.py # Performs sentiment analysis
    ├── thematic_tfidf.py     # Computes TF-IDF and assigns themes
    └── postgres_insert.py    # Inserts data into PostgreSQL
```

## Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database (for data storage)
- Git (for cloning the repository)

### Setup Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Tofikoabdu1/Omega-Consultancy.git
   cd omega-consultancy
   ```

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**:

   - Install PostgreSQL and create a database named `bank_reviews`.
   - Run the schema script:
     ```bash
     psql -d bank_reviews -f sql/create_schema.sql
     ```
   - Configure environment variables for database connection (optional, create a `.env` file):
     ```
     DB_NAME=bank_reviews
     DB_USER=postgres
     DB_PASS=yourpassword
     DB_HOST=localhost
     DB_PORT=5432
     ```

5. **Download required NLP models**:
   ```bash
   python -c "import spacy; spacy.cli.download('en_core_web_sm')"
   ```

## Usage

### Data Pipeline Execution

1. **Scrape Reviews** (Task 1):

   ```bash
   python src/scrape_reviews.py
   ```

   This generates raw CSV files in `data/raw/`.

2. **Preprocess Data** (Task 2):

   ```bash
   python src/preprocess.py
   ```

   This cleans the data and saves `all_reviews_clean.csv` in `data/cleaned/`.

3. **Run Sentiment Analysis**:

   ```bash
   python src/sentiment_pipeline.py
   ```

   This adds sentiment labels and scores to the data.

4. **Perform Thematic Analysis**:

   ```bash
   python src/thematic_tfidf.py
   ```

   This computes TF-IDF keywords and assigns themes, saving results in `data/processed/`.

5. **Load Data into Database** (Task 3):

   ```bash
   python src/postgres_insert.py
   ```

   This inserts the processed data into PostgreSQL.

6. **Generate Visualizations**:
   Run the `notebooks/Visualization.ipynb` notebook to create charts for rating distributions, sentiment counts, and top themes.

### Running Notebooks

Use Jupyter Lab to explore and run the notebooks:

```bash
jupyter lab
```

Open the notebooks in `notebooks/` for interactive analysis.

## Data Description

- **Raw Data**: Reviews scraped from Google Play Store, including text, ratings, dates, and review IDs.
- **Cleaned Data**: Deduplicated, normalized data with consistent formats.
- **Processed Data**: Includes sentiment analysis (positive/negative/neutral) and thematic categorization (e.g., Account Access, Transactions, Performance).
- **Themes**: Rule-based assignment using keywords like "login", "transfer", "slow", etc.

## Visualization Examples

The project generates several visualizations:

- Rating distribution by bank
- Sentiment counts by bank
- Top themes across all reviews

Example output figures are saved in `data/processed/figures/`.

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit changes: `git commit -am 'Add your feature'`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Submit a pull request.

## Acknowledgments

- Built for the 10 Academy Omega Consultancy project.
- Utilizes open-source libraries like Transformers, SpaCy, and Scikit-learn for NLP tasks.
