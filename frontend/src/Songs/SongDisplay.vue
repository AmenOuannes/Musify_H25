<template>
  <button class="song-button" @click="$emit('click')">
    <div class="info">
      <span class="name">{{ song.song_name }}</span>
      <span class="genre">{{ song.genre }}</span>
      <span class="artist">🎤 {{ song.artist_name }}</span>
      <span class="date">📅 {{ song.release_date }}</span>
    </div>
  </button>
</template>

<script setup>
defineProps({
  song: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.song-button {
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

.song-button:hover {
  background-color: #2a9d8f22;
  transform: scale(1.01);
}

.info {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
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
