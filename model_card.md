# Music Recommender Simulation: Model Card

## 1. Model Name & Overview

**Model Name:** VibeFinder 1.0

**Goal / Task:** This recommender suggests top 5 songs from a small CSV catalog based on user taste features like genre, mood, energy level, and acoustic preference. It's designed to demonstrate how content-based recommendation systems work by matching learned user preferences against song attributes.

---

## 2. How the Model Works  

**Algorithm Summary:**

The recommendation system scores each song in the catalog using a weighted formula:

- **+2.0 points** for genre match: Does the song match the user's favorite genre?
- **+1.0 point** for mood match: Does the song match the user's favorite mood?
- **+energy similarity** based on closeness: We calculate `1 - |song_energy - target_energy|` and multiply by weight (1.0), rewarding songs that are close to the user's target energy level. A user targeting energy 0.88 gets +0.95 for a song at 0.93 energy, but only +0.60 for a song at 0.28 energy.
- **+0.5 bonus** if the user likes acoustic songs AND the song has high acousticness (≥ 0.60)

**Example Scoring:** For a user who loves "pop" + "happy" + energy 0.88 + likes acoustic:
- "Sunrise City" (pop, happy, 0.82 energy, 0.18 acoustic): 2.0 + 1.0 + 0.94 + 0 = **3.94 points** → Ranks #1
- "Gym Hero" (pop, intense, 0.93 energy, 0.05 acoustic): 2.0 + 0 + 0.95 + 0 = **2.95 points** → Ranks #2 (same genre + closest energy, but wrong mood)

The system then **sorts all songs by score (highest first) and returns the top K recommendations** (default K=5).

**Key design choice:** Energy is a "tiebreaker" when multiple songs have the same genre AND mood. This makes songs with similar energy rank high even if other features don't match as well.

---

## 3. Data Used

**Dataset Size & Source:** 18 songs in `data/songs.csv` (small, curated catalog for learning purposes).

**Song Features Used in Scoring:**
- `genre` (categorical): pop, lofi, rock, ambient, jazz, synthwave, hip hop, classical, reggae, metal, country, edm, r&b, latin, indie pop
- `mood` (categorical): happy, chill, intense, relaxed, moody, calm, confident, aggressive, nostalgic, uplifting, focused, romantic, playful, euphoric
- `energy` (0.0-1.0, float): intensity/vibrancy of the track
- `tempo_bpm` (float): beats per minute (not currently used in scoring, but available)
- `valence` (0.0-1.0, float): musical positivity/brightness (not currently used in scoring)
- `danceability` (0.0-1.0, float): how suitable for dancing (not currently used in scoring)
- `acousticness` (0.0-1.0, float): proportion of acoustic instrumentation

**User Features (Preferences):**
- `favorite_genre`: The genre the user prefers
- `favorite_mood`: The mood the user prefers
- `target_energy`: A number 0.0-1.0 representing desired song intensity
- `likes_acoustic`: Boolean (true/false) for acoustic preference

**Data Limitations:** The dataset only has 18 songs, covering 15 unique genres and 14 unique moods. This means many real music styles, languages, regional traditions, and subcultures are not represented. The small size creates clustering (many songs in the 0.74-0.93 energy range), which limits recommendation diversity.

---

## 4. Model Strengths

The model works well for clear profiles like "Chill Lofi" and "Deep Intense Rock" where the user's preferred genre, mood, and energy level align.

It gives understandable reasons for each recommendation (genre match, mood match, energy similarity, acoustic bonus), which makes debugging easier and helps users trust the system.

The energy similarity feature captures vibe intensity better than simple "high" or "low" rules. By rewarding closeness to a target energy, we can recommend songs that feel energetically similar even across different genres.

The explanations ("reasons" list) are the most important feature—users trust a system when they understand why a song was recommended, even if the math is simple.

---

## 5. Model Limitations & Observed Biases

**Filter Bubble Risk:** The system strongly rewards energy closeness, which can cause "Gym Hero" (pop, 0.93 energy) to rank high for users searching for genres other than pop if their target energy is ~0.88. This energy-based ranking can trap users in songs that "feel" similar even if the genre is different, narrowing their discovery.

**Cross-Genre Discovery Gap:** When a user's preferred genre is absent (e.g., searching for "k-pop"), the system falls back entirely to mood and energy matching. With only one feature match available, songs become indistinguishable from each other by score alone. A larger dataset with more genres would help.

**Small Catalog Homogeneity:** With 18 songs, many songs share similar energy levels (0.74-0.93 range). This creates redundancy in the top-5—high-energy recommendations stay similar across different profiles because there are few low-energy alternatives to choose from.

**Missing Context:** The system ignores lyrics, artist popularity, listening context (workout vs sleep vs focus), and cultural/linguistic diversity. It also doesn't account for user history or temporal trends. A real recommender would incorporate these signals.


## 6. How the System Was Tested & Evaluated

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


---

## 7. Intended Use & Non-Intended Use

**Intended Use:**
- Educational tool for learning how content-based recommendation systems work
- Simple demonstration of scoring, ranking, and explanation generation
- Experiment with weight changes and their effects on recommendations
- Test case study for how energy similarity can create filter bubbles

**Non-Intended Use:**
- Do not use for real user personalization or commercial recommendations
- Do not use for mental health, well-being, or mood management (it's not trained on actual user data or therapeutic knowledge)
- Do not rely on it for high-stakes decisions about music or audio content
- Do not assume it represents real music taste patterns without much larger datasets

**Key Assumption:** The system assumes users can describe their taste with four simple features (genre, mood, energy, acoustic preference) and that these features are sufficient to find songs they'll like.

---

## 8. Potential Improvements for Future Versions

1. **Add diversity rules** so the Top 5 isn't dominated by one style. For example, penalize songs too similar to already-ranked songs.

2. **Expand the dataset** to 200+ songs with better representation of genres, languages, cultural styles, and mood ranges.

3. **Add Streaming UI** (using Streamlit) to let users adjust weights in real-time and see how recommendations change.

4. **Incorporate user history** to avoid recommending the same songs repeatedly and learn from clicks/plays.

5. **Add dynamic features** like listening context (workout vs. sleep vs. focus) and temporal trends (what's popular now?).

---

## 9. Personal Reflection: What I Learned

My biggest learning moment was seeing how energy similarity becomes the dominant factor when genre matches are limited. When I tested doubling energy weight, the rankings barely changed because energy was already the tiebreaker—not because genre wasn't important, but because genre alone isn't enough to differentiate songs.

I was surprised that "Gym Hero" ranked #2 for High-Energy Pop despite being a different genre. This taught me that energy closeness is a powerful ranking signal, which is good for vibe-matching but bad for genre diversity. In a real recommender, I would add a diversity penalty to reduce repetition.

AI tools helped me draft the scoring logic and experiment code quickly, but manual testing was essential. I had to trace through why specific songs ranked where they did, and that detective work revealed the energy-as-tiebreaker pattern that the weights alone didn't show.

I was surprised that a simple scoring formula can still feel like a real recommender when explanations are clear. Users trust a system when they understand its reasoning, even if the math is basic. This is why the "reasons" list became the most important part of my output.

If I continue this project, I would: (1) expand the dataset to 200+ songs with more genre and mood diversity, (2) add a diversity penalty to the scoring function to reduce repetition in top-5, and (3) build a Streamlit UI to let users adjust weights and see results in real-time. I'd also collect user feedback on whether recommendations "feel right" versus just scoring well mathematically.
