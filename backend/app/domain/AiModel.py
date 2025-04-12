from sentence_transformers import SentenceTransformer, util
import torch

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

    return {
        'group_genres': input_genres,
        'target_genre': target_genre,
        'similarity_score': round(similarity, 4),
        'is_similar': is_similar
    }


print(is_target_genre_similar_to_group(['pop', 'rap', 'pop', 'pop','pop', 'pop', 'pop', 'country'], ['rap']))