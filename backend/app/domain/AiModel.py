_model = None


def get_model():
    global _model
    if _model is None:
        import torch
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


def is_target_genre_similar_to_group(input_genres, target_genre, threshold=0.75):
    if not input_genres:
        return False
    if not target_genre:
        return False

    import torch
    from sentence_transformers import util

    model = get_model()
    input_embeddings = model.encode(input_genres, convert_to_tensor=True)
    group_embedding = torch.mean(input_embeddings, dim=0)
    target_embedding = model.encode(target_genre, convert_to_tensor=True)
    similarity = util.cos_sim(group_embedding, target_embedding).item()
    return similarity >= threshold


def recommend_entities(existing_entities, recommendation_targets, limit=10):
    if not existing_entities or not recommendation_targets:
        return recommendation_targets[:limit]

    existing_genres = [entity.genre for entity in existing_entities if getattr(entity, "genre", None)]
    recommendations = []
    for target in recommendation_targets:
        if len(recommendations) >= limit:
            break
        if is_target_genre_similar_to_group(existing_genres, getattr(target, "genre", None)):
            recommendations.append(target)
    return recommendations
