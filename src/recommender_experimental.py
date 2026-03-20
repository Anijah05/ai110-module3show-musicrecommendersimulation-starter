"""
Experimental version of recommender with modified weights to test system sensitivity.

Weight Change Experiment:
- genre_weight: 2.0 → 1.0 (halved)
- energy_weight: 1.0 → 2.0 (doubled)
- This tests whether energy similarity becomes the dominant feature.
"""

from typing import List, Dict, Tuple
from recommender import load_songs

def score_song_experimental(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Experimental scoring function with energy emphasized over genre."""
    # MODIFIED WEIGHTS for experiment:
    genre_weight = 1.0  # Halved from 2.0
    mood_weight = 1.0
    energy_weight = 2.0  # Doubled from 1.0
    acoustic_bonus = 0.5

    score = 0.0
    reasons: List[str] = []

    preferred_genre = str(user_prefs.get("genre", "")).strip().lower()
    preferred_mood = str(user_prefs.get("mood", "")).strip().lower()
    target_energy = float(user_prefs.get("energy", 0.5))
    likes_acoustic = bool(user_prefs.get("likes_acoustic", False))

    song_genre = str(song.get("genre", "")).strip().lower()
    song_mood = str(song.get("mood", "")).strip().lower()
    song_energy = float(song.get("energy", 0.5))
    song_acousticness = float(song.get("acousticness", 0.0))

    if song_genre == preferred_genre and preferred_genre:
        score += genre_weight
        reasons.append(f"genre match (+{genre_weight:.1f})")

    if song_mood == preferred_mood and preferred_mood:
        score += mood_weight
        reasons.append(f"mood match (+{mood_weight:.1f})")

    energy_similarity = max(0.0, 1.0 - abs(song_energy - target_energy))
    weighted_energy = energy_similarity * energy_weight
    score += weighted_energy
    reasons.append(f"energy similarity (+{weighted_energy:.2f})")

    if likes_acoustic and song_acousticness >= 0.60:
        score += acoustic_bonus
        reasons.append(f"acoustic preference match (+{acoustic_bonus:.1f})")

    return score, reasons

def recommend_songs_experimental(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Ranks songs using experimental weights and returns top-k with explanations."""
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song_experimental(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))

    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return ranked[:k]


if __name__ == "__main__":
    """Run experiment comparing original vs experimental weights."""
    # Import original for comparison
    from recommender import recommend_songs
    
    songs = load_songs("data/songs.csv")
    print("=" * 70)
    print("EXPERIMENT: Energy-Weighted Recommender (Genre 1.0, Energy 2.0)")
    print("=" * 70)
    
    profiles = {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.88,
            "likes_acoustic": False,
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "likes_acoustic": True,
        },
    }

    for profile_name, user_prefs in profiles.items():
        print(f"\n{'=' * 70}")
        print(f"Profile: {profile_name}")
        print(f"{'=' * 70}")
        
        # Original recommendations
        print(f"\n--- ORIGINAL (Genre 2.0, Energy 1.0) ---")
        original_recs = recommend_songs(user_prefs, songs, k=5)
        for index, rec in enumerate(original_recs, start=1):
            song, score, explanation = rec
            print(f"{index}. {song['title']} (Score: {score:.2f})")
        
        # Experimental recommendations
        print(f"\n--- EXPERIMENTAL (Genre 1.0, Energy 2.0) ---")
        experimental_recs = recommend_songs_experimental(user_prefs, songs, k=5)
        for index, rec in enumerate(experimental_recs, start=1):
            song, score, explanation = rec
            print(f"{index}. {song['title']} (Score: {score:.2f})")
            print(f"   Reasons: {explanation}")
        
        # Analysis
        original_titles = [r[0]['title'] for r in original_recs]
        experimental_titles = [r[0]['title'] for r in experimental_recs]
        same_count = len(set(original_titles) & set(experimental_titles))
        print(f"\n→ Overlap: {same_count}/5 songs appear in both rankings")
        print(f"→ Interpretation: Energy weighting {'shifts' if same_count < 4 else 'slightly affects'} recommendations")
