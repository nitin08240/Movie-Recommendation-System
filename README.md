# Movie Recommendation System

Short description
- A simple Streamlit web app that recommends 5 similar movies for a selected title and shows their posters fetched from The Movie Database (TMDB).
- Fast, content‑based recommender using a precomputed similarity matrix.

Key features
- Select a movie from a dropdown and get top-5 similar movies.
- Poster images loaded from TMDB (with retries and placeholder image on failure).
- Precomputed similarity for instant responses.

Project structure (important files)
- app.py              — Streamlit app and inference logic
- setup.sh            — deployment helper for some hosts (e.g. Heroku)
- requirements.txt    — Python dependencies
- model/
  - movie_list.pkl    — pandas DataFrame with movies (title, movie_id, ...)
  - similarity.pkl    — precomputed similarity matrix (numpy)
- README.md           — this file
- .gitignore          — files to ignore (venv, model pickles optionally)

ML parts — what we use and why (concise)
- Feature construction: movie metadata (title, genres, overview, cast/crew, keywords) are combined into a single text/tags field per movie.
  - Why: capture multiple aspects (plot, genre, people) in one representation.
- Vectorization: TF-IDF or CountVectorizer on the combined text/tags.
  - Why: converts text into numeric vectors; TF-IDF emphasizes distinguishing tokens.
- Similarity: cosine similarity between movie vectors, computed offline and saved to `similarity.pkl`.
  - Why: cosine is scale-invariant and standard for high-dimensional text vectors.
- Recommendation: look up the selected movie index, sort neighbors by similarity, return top-N.
  - Why: simple, interpretable, works without user-rating history (content-based).

Prerequisites
- Python 3.8+
- Internet access for TMDB API (for posters)
- model/movie_list.pkl and model/similarity.pkl must exist

Setup (Windows PowerShell)
1. Open PowerShell in project folder:
   cd "d:\ML END TO END PROJECT\Movie Recommendation System"

2. Create and activate virtual environment:
   python -m venv .venv
   .venv\Scripts\Activate

3. Install dependencies:
   pip install -r requirements.txt

Run locally
- Start the app:
  streamlit run app.py

Environment / TMDB API key (recommended)
- Do NOT commit API keys. Prefer using an environment variable:
  - Set in PowerShell:
    $env:TMDB_API_KEY="your_api_key_here"
  - Update app.py to read the key:
    import os
    TMDB_API_KEY = os.getenv("TMDB_API_KEY")
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"

Troubleshooting
- requests.exceptions.ConnectionError when fetching posters:
  - Check internet/firewall/VPN.
  - Verify TMDB key and rate limits.
  - App uses retry and placeholder image on failure.
- "src refspec main does not match any" when pushing to GitHub:
  - Ensure you have a commit, set branch to main (git branch -M main) and push.
- Large model pickle files:
  - Use Git LFS or host them elsewhere (S3, GCP) and download during startup.

Security & best practices
- Move API keys to environment variables (.env) and add .env to .gitignore.
- Do not commit large binary model files to a normal Git repository; use Git LFS or external storage.
- Validate and sanitize any external inputs where applicable.

Improvements & next steps
- Hybrid recommender (combine collaborative + content-based) for personalization.
- Cache poster URLs or images to reduce API calls and latency.
- Use approximate nearest neighbors (FAISS/Annoy) for large datasets.
- Add unit tests for recommendation logic and model loading.

License & credits
- MIT License (add LICENSE file if desired).
- Uses TMDB for poster images — follow TMDB terms of service.

