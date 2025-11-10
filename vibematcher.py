import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sentence_transformers import SentenceTransformer

class VibeMatcher:

    def __init__(self):
        self.model = SentenceTransformer('all-mpnet-base-v2')
        self.products_df = self._get_mock_data()
        self.product_vectors = None
        self._vibe_emoji_map = {
            "boho": "🌸",
            "festival": "🎉",
            "beach": "🌊",
            "urban": "🏙️",
            "techwear": "🔌",
            "athletic": "👟",
            "cozy": "🧣",
            "comfort": "☕",
            "minimalist": "✨",
            "elegant": "💎",
            "classic": "🏛️",
            "cyberpunk": "🤖",
            "energetic": "⚡",
            "relaxed": "🧘",
            "vacation": "🌴",
            "vintage": "📜",
            "academic": "📚",
            "default": "🛍️"
        }

    def _get_mock_data(self):
        data = [
            {
                "name": "Sunset Boho Maxi Dress",
                "desc": "Flowy, earthy tones with floral embroidery. Perfect for festivals or a beach walk. Feels like freedom.",
                "vibes": ["boho", "festival", "beach", "free-spirit"],
                "ai_tags": "a free-spirit boho dress for a beach festival."
            },
            {
                "name": "Urbanite Tech Runner",
                "desc": "Sleek, black-on-black design with reflective accents. Lightweight, high-rebound sole for city streets.",
                "vibes": ["urban", "techwear", "athletic", "modern"],
                "ai_tags": "energetic urban chic. a modern athletic techwear sneaker for the city."
            },
            {
                "name": "Cozy Knit Cardigan",
                "desc": "An oversized, chunky knit sweater in a warm cream color. Feels like a hug. Ideal for rainy days with a good book.",
                "vibes": ["cozy", "comfort", "hygge", "casual"],
                "ai_tags": "cozy rainy day book. a perfect cozy knit cardigan. oversized, warm, and comfortable. hygge style."
            },
            {
                "name": "Minimalist Gold Hoops",
                "desc": "Thin, 18k gold-plated hoops. A timeless, elegant staple that goes with everything. Clean and sophisticated.",
                "vibes": ["minimalist", "elegant", "classic", "chic"],
                "ai_tags": "minimalist art gallery. an elegant and chic accessory. timeless, sophisticated gold hoops."
            },
            {
                "name": "Cyber-Punk Bomber Jacket",
                "desc": "A high-shine metallic silver jacket with neon pink LED piping on the seams. Waterproof, with hidden internal pockets.",
                "vibes": ["cyberpunk", "energetic", "statement", "future"],
                "ai_tags": "futuristic cyberpunk. a cyberpunk street market. a high-shine statement jacket. future-tech style."
            },
            {
                "name": "Linen Drawstring Trousers",
                "desc": "Lightweight, breathable beige linen pants. Relaxed fit. Perfect for a summer vacation or a casual brunch.",
                "vibes": ["relaxed", "vacation", "summer", "minimalist"],
                "ai_tags": "Relaxed, minimalist linen pants. Perfect for a summer vacation or casual brunch. Lightweight and breathable."
            },
            {
                "name": "Vintage Leather Satchel",
                "desc": "A distressed brown leather bag with brass buckles. Smells of old books and adventure. Built to last a lifetime.",
                "vibes": ["vintage", "academic", "adventurous", "classic"],
                "ai_tags": "cozy academic library. a classic vintage leather satchel. smells of old books and history."
            }
        ]
        return pd.DataFrame(data)

    def get_emoji_for_vibes(self, vibe_list):
        for vibe in vibe_list:
            if vibe in self._vibe_emoji_map:
                return self._vibe_emoji_map[vibe]
        return self._vibe_emoji_map["default"]

    def embed_text(self, text):
        try:
            return self.model.encode(text.lower())
        except Exception as e:
            print(f"Error embedding text locally: {e}")
            return None

    def build_product_vectors(self):
        print("Building product vectors (locally)...")
        vectors = []
        for tags in self.products_df['ai_tags']:
            vector = self.embed_text(tags)
            if vector is not None:
                vectors.append(vector)
        
        self.product_vectors = np.array(vectors)
        print("Product vectors built successfully!")

    def find_matches(self, vibe_query, top_n=3):
        if self.product_vectors is None:
            raise Exception("Product vectors are not built. Run build_product_vectors() first.")

        query_vector = self.embed_text(vibe_query)
        if query_vector is None:
            return pd.DataFrame() 

        query_vector = query_vector.reshape(1, -1)
        
        sim_scores = cosine_similarity(query_vector, self.product_vectors)
        
        sim_scores = sim_scores.flatten()
        
        top_indices = sim_scores.argsort()[-top_n:][::-1]
        
        results_df = self.products_df.iloc[top_indices].copy()
        results_df['score'] = sim_scores[top_indices]
        
        return results_df