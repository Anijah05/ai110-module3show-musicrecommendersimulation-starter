Model Card Music Recommender Simulation


VibeFinder 1.0

---

 Intended Use  

**Goal / Task:** This recommender suggests Top 5 songs from a small CSV catalog based on user taste features.

**Intended Use:** It is for classroom learning and simple experiments with recommendation logic.

**Non-Intended Use:** It should not be used for real user decisions, mental health use, or any high-stakes personalization.

The system assumes users can describe their taste with genre, mood, energy, and acoustic preference.


## 3. How the Model Works  

**Algorithm Summary:**

Each song gets a score. The model adds points for a genre match and mood match. It also adds energy similarity points, so songs close to the target energy score higher. It gives a small bonus if the user likes acoustic songs and the track is highly acoustic.

Used song features: genre, mood, energy, tempo, valence, danceability, acousticness.
Used user features: favorite genre, favorite mood, target energy, likes acoustic.

I changed the starter logic by increasing energy importance and reducing genre weight in one experiment.


## 4. Data  

The dataset has 18 songs in `data/songs.csv`.

It includes genres like pop, lofi, rock, ambient, jazz, synthwave, hip hop, classical, reggae, metal, country, edm, r&b, latin, and indie pop.

It includes moods like happy, chill, intense, relaxed, moody.

The data is still small, so many real music styles, languages, and subcultures are missing.


## 5. Strengths  

The model works well for clear profiles like "Chill Lofi" and "Deep Intense Rock." 

It gives understandable reasons for each recommendation, which makes debugging easier.

The energy similarity feature captures vibe intensity better than simple high/low rules.


## 6. Limitations and Bias 

**Filter Bubble Risk:** The system strongly rewards energy closeness, which can cause "Gym Hero" (pop, 0.93 energy) to rank high for users searching for genres other than pop if their target energy is ~0.88. This energy-based ranking can trap users in songs that "feel" similar even if the genre is different, narrowing their discovery.

**Cross-Genre Discovery Gap:** When a user's preferred genre is absent (e.g., searching for "k-pop"), the system falls back entirely to mood and energy matching. With only one feature match available, songs become indistinguishable from each other by score alone. A larger dataset with more genres would help.

**Small Catalog Homogeneity:** With 18 songs, many songs share similar energy levels (0.74-0.93 range). This creates redundancy in the top-5—high-energy recommendations stay similar across different profiles because there are few low-energy alternatives to choose from.

**Missing Context:** The system ignores lyrics, artist popularity, listening context (workout vs sleep vs focus), and cultural/linguistic diversity. It also doesn't account for user history or temporal trends. A real recommender would incorporate these signals.


## 7. Evaluation  

**Test Profiles:**
- High-Energy Pop: genre="pop", mood="happy", energy=0.88, acoustic=false
- Chill Lofi: genre="lofi", mood="chill", energy=0.35, acoustic=true  
- Deep Intense Rock: genre="rock", mood="intense", energy=0.92, acoustic=false
- Conflicting Edge Case: genre="ambient", mood="sad", energy=0.90, acoustic=true (high energy + sad mood conflict)
- Unknown Genre Edge Case: genre="k-pop", mood="focused", energy=0.50, acoustic=false (genre not in dataset)

**Results and Interpretations:**

Clear profiles (Chill Lofi, Deep Intense Rock) produced intuitive top-5 lists where the #1 song had all four features matching (genre + mood + energy + acoustic). However, the High-Energy Pop profile revealed a key weakness: **"Gym Hero" by Max Pulse ranked 2nd despite not being pop**, beating out the indie-pop "Rooftop Lights." This happened because Gym Hero has energy 0.93, matching the target 0.88 more closely than any other non-pop song, so the energy similarity bonus (+0.95) outweighed the missing genre match.

Edge cases were revealing. The conflicting profile (high energy + sad mood) couldn't find well-matched songs because no songs combined those features. "Spacewalk Thoughts" (ambient + chill) ranked first only because it matched mood and was highly acoustic—the energy mismatch (0.28 vs 0.90 target) cost -1.24 points. The unknown-genre profile fell back to mood and energy, with "Focus Flow" winning purely on mood match and energy similarity.

**Weight Sensitivity Experiment:**
I tested doubling energy weight (1.0→2.0) and halving genre weight (2.0→1.0) to see if that would reduce genre dominance. Result: the **same 5 songs ranked in both versions**. For Chill Lofi, the top song stayed identical (Library Rain 4.50/4.50), proving that when both genre and energy are strong matches, small weight changes don't shift the ranking significantly. This suggests the system works best for users whose preferred genre aligns with their energy level, and struggles for cross-genre searchers.

**Biggest Surprise:**
Songs with mid-range energy (like 0.74-0.82) appeared frequently across multiple profile recommendations, even when mood was mismatched. This is because energy similarity is calculated as a closeness score: even songs 0.3 energy points away still get +0.7 bonus, making them competitive against songs with only one feature match.


## 8. Future Work  

1. Add diversity rules so the Top 5 is not dominated by one style.
2. Add more user controls (tempo range, valence target, danceability target).
3. Expand the dataset with more genres, languages, and artists.


## 9. Personal Reflection  

My biggest learning moment was seeing how energy similarity becomes the dominant factor when genre matches are limited. When I tested doubling energy weight, the rankings barely changed because energy was already the tiebreaker—not because genre wasn't important, but because genre alone isn't enough to differentiate songs.

I was surprised that "Gym Hero" ranked #2 for High-Energy Pop despite being a different genre. This taught me that energy closeness is a powerful ranking signal, which is good for vibe-matching but bad for genre diversity. In a real recommender, I would add a diversity penalty to reduce repetition.

AI tools helped me draft the scoring logic and experiment code quickly, but manual testing was essential. I had to trace through why specific songs ranked where they did, and that detective work revealed the energy-as-tiebreaker pattern that the weights alone didn't show.

I was surprised that a simple scoring formula can still feel like a real recommender when explanations are clear. Users trust a system when they understand its reasoning, even if the math is basic. This is why the "reasons" list became the most important part of my output.

If I continue this project, I would: (1) expand the dataset to 200+ songs with more genre and mood diversity, (2) add a diversity penalty to the scoring function to reduce repetition in top-5, and (3) build a Streamlit UI to let users adjust weights and see results in real-time. I'd also collect user feedback on whether recommendations "feel right" versus just scoring well mathematically.
