<template>
  <button class="album-button" @click="$emit('click')">
    <img
        v-if="album.image"
        :src="album.image"
        alt="Album Cover"
        class="album-avatar"
    />
    <div class="info">
      <span class="name">{{ album.album_name }}</span>
      <span class="meta-line">
        <span class="genre">{{ album.genre }}</span>
        <span class="artist">🎤 {{ album.artist_name }}</span>
        <span class="date">📅 {{ album.release_date }}</span>
      </span>
    </div>
  </button>
</template>

<script setup>
defineProps({
  album: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.album-button {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
  background-color: #1e1e1e;
  color: white;
  padding: 1rem 1.2rem;
  border: 1px solid #2a2a2a;
  border-radius: 12px;
  cursor: pointer;
  text-align: left;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 2px 6px rgba(0, 255, 255, 0.05);
}

.album-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(26, 188, 156, 0.25);
  border-color: #0f0;
}

.album-avatar {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.5);
}

.info {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  flex-grow: 1;
}

.name {
  font-weight: 700;
  font-size: 1.05rem;
  color: #22c55e;
  background-color: rgba(26, 188, 156, 0.1);
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
  width: fit-content;
}

.meta-line {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  font-size: 0.85rem;
  color: #ccc;
  align-items: center;
}

.genre {
  font-weight: 500;
  color: #ccc;
}

.artist {
  font-weight: 500;
  color: #eee;
}

.date {
  font-size: 0.85rem;
  color: #aaa;
}
</style>
