# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

---

## 2. Intended Use  

**Goal / Task:** This recommender suggests Top 5 songs from a small CSV catalog based on user taste features.

**Intended Use:** It is for classroom learning and simple experiments with recommendation logic.

**Non-Intended Use:** It should not be used for real user decisions, mental health use, or any high-stakes personalization.

The system assumes users can describe their taste with genre, mood, energy, and acoustic preference.

---

## 3. How the Model Works  

**Algorithm Summary:**

Each song gets a score. The model adds points for a genre match and mood match. It also adds energy similarity points, so songs close to the target energy score higher. It gives a small bonus if the user likes acoustic songs and the track is highly acoustic.

Used song features: genre, mood, energy, tempo, valence, danceability, acousticness.
Used user features: favorite genre, favorite mood, target energy, likes acoustic.

I changed the starter logic by increasing energy importance and reducing genre weight in one experiment.

---

## 4. Data  

The dataset has 18 songs in `data/songs.csv`.

It includes genres like pop, lofi, rock, ambient, jazz, synthwave, hip hop, classical, reggae, metal, country, edm, r&b, latin, and indie pop.

It includes moods like happy, chill, intense, relaxed, moody, focused, confident, calm, uplifting, aggressive, nostalgic, euphoric, romantic, and playful.

The data is still small, so many real music styles, languages, and subcultures are missing.

---

## 5. Strengths  

The model works well for clear profiles like "Chill Lofi" and "Deep Intense Rock." 

It gives understandable reasons for each recommendation, which makes debugging easier.

The energy similarity feature captures vibe intensity better than simple high/low rules.

---

## 6. Limitations and Bias 

One weakness is over-reliance on energy similarity. Songs with close energy can rank high even when mood does not match.

The catalog is small, so some user tastes are underrepresented.

This can create a filter bubble, where the same high-energy tracks appear across many profiles.

The model also ignores lyrics, language, culture, and listening context.

---

## 7. Evaluation  

I tested five profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, a conflicting edge case, and an unknown-genre edge case.

For each profile, I inspected the Top 5 songs and checked if the ranking reasons made sense.

Most clear profiles gave expected results, but high-energy songs still appeared often when mood was not a match.

The biggest surprise was how often one energetic song could appear for users who only partly matched that vibe.

---

## 8. Future Work  

1. Add diversity rules so the Top 5 is not dominated by one style.
2. Add more user controls (tempo range, valence target, danceability target).
3. Expand the dataset with more genres, languages, and artists.

---

## 9. Personal Reflection  

My biggest learning moment was seeing how small weight changes can shift recommendations a lot.

AI tools helped me draft logic and speed up coding, but I still had to verify imports, check outputs, and test edge cases manually.

I was surprised that a simple scoring formula can still feel like a real recommender when explanations are clear.

If I continue this project, I would build a small Streamlit UI and add profile comparison charts to make behavior easier to analyze.
