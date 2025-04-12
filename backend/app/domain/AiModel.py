import torch
from sentence_transformers import SentenceTransformer, util

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')


def is_target_genre_similar_to_group(input_genres, target_genre, threshold=0.75):
    if not input_genres:
        raise ValueError("Input genre list is empty.")

    # Encode all input genres
    input_embeddings = model.encode(input_genres, convert_to_tensor=True)

    # Average the embeddings to get a single "group" embedding
    group_embedding = torch.mean(input_embeddings, dim=0)

    # Encode the target genre
    target_embedding = model.encode(target_genre, convert_to_tensor=True)

    # Compute cosine similarity between group and target
    similarity = util.cos_sim(group_embedding, target_embedding).item()

    # Binary result based on threshold
    is_similar = 1 if similarity >= threshold else 0

    return is_similar

def recommend_entities(existing_entities, recommendation_targets):
    recommendations = []

    i = 0
    while len(recommendations) <= 10:
        is_similar = is_target_genre_similar_to_group([entity.genre for entity in existing_entities], recommendation_targets[i].genre)
        if is_similar:
            recommendations.append(recommendation_targets[i])
        i += 1
    return recommendations
