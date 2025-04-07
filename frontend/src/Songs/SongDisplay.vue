<template>
  <div class="song-button-container">
    <button class="song-button" @click="$emit('click')">
      <div class="info">
        <span class="name">{{ song.song_name }}</span>
        <span class="genre">{{ song.genre }}</span>
        <span class="artist">🎤 {{ song.artist_name }}</span>
        <span class="date">📅 {{ song.release_date }}</span>
      </div>
    </button>

    <button
        v-if="onRemove"
        class="remove-btn"
        @click.stop="confirmRemove"
        title="Remove from album"
    >
      🗑
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  song: {
    type: Object,
    required: true
  },
  onRemove: Function // facultatif : si fourni, on affiche le bouton
})

const confirmRemove = () => {
  if (confirm(`Are you sure you want to remove "${props.song.song_name}" from the album?`)) {
    props.onRemove?.(props.song.song_name)
  }
}
</script>

<style scoped>
.song-button-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
}

.song-button {
  flex-grow: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #1e1e1e;
  border: 1px solid #444;
  border-radius: 10px;
  padding: 1rem 1.5rem;
  color: white;
  text-align: left;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.2s;
}

.song-button:hover {
  background-color: #2a9d8f22;
  transform: scale(1.01);
}

.remove-btn {
  background: none;
  border: none;
  color: #f87171;
  font-size: 1.2rem;
  cursor: pointer;
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
