# QuestFinder

QuestFinder is a web application for exploring and recommending classic and retro video games using Amazon review data.  
The system predicts top-rated games, generates personalized recommendations for each user, and suggests similar games based on title search.

---

## Features

- **Top Rated Games:**  
  Displays a grid of highly rated and popular games with their average rating and review count.

- **Personalized Recommendations:**  
  Enter your Amazon user ID to get tailored predicted ratings for games you haven't reviewed yet.

- **Find Similar Games:**  
  Search by partial or full game title, and discover similar or related games, with similarity scoring.

---

## Screenshots
**Top Rated Games**
<img width="1891" height="612" alt="Screenshot 2025-08-16 145012" src="https://github.com/user-attachments/assets/fa07d15d-5dc2-4eaa-b969-d7a04aeed55d" />
**Recommendations by User ID and Game Title**
<img width="1893" height="833" alt="Screenshot 2025-08-16 144931" src="https://github.com/user-attachments/assets/74515848-6d02-42cf-9fc7-461f630c589f" />


---

## Project Structure
```
├── api.py
├── main.py
├── data_preprocessing.py
├── feature_engineering.py
├── metrics.py
├── recommendation.py
├── requirements.txt
├── runtime.txt
├── data/ # Game review data and metadata (csv, json)
├── models/ # Trained models and vectorizers
├── static/ # CSS/JS frontend assets
├── templates/ # HTML templates
├── venv/ # Local Python virtual environment

```

---

## How to Run

**Install dependencies:**

**Process data and train models:**

**Start the web server:**

**Open the app:**  
Go to [http://localhost:5000](http://localhost:5000) in your browser.

---

## Data and Methodology

- Uses real Amazon video game reviews, filtered and preprocessed for quality.
- Hybrid recommendation engine:
    - Collaborative filtering (user-game ratings)
    - Content-based analysis (review text similarity via NLP and TF-IDF)
- Fast querying via Flask API endpoints.

---
