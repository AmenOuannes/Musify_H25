<template>
  <button class="album-button" @click="$emit('click')">
    <div class="info">
      <span class="name">{{ album.album_name }}</span>
      <span class="genre">{{ album.genre }}</span>
      <span class="artist">🎤 {{ album.artist_name }}</span>
      <span class="date">📅 {{ album.release_date }}</span>
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
  justify-content: space-between;
  background-color: #1e1e1e;
  border: 1px solid #444;
  border-radius: 10px;
  padding: 1rem 1.5rem;
  color: white;
  width: 100%;
  text-align: left;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.2s;
}

.album-button:hover {
  background-color: #2a9d8f22;
  transform: scale(1.01);
}

.info {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
  align-items: center;
  width: 100%;
}

.name {
  font-weight: bold;
  color: #2a9d8f;
}

.genre,
.artist,
.date {
  color: #ccc;
  font-size: 0.9rem;
}
</style>
