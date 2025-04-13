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
        @click.stop="onRemove(song.song_name)"
        title="Remove from album"
    >
      🗑
    </button>
  </div>
</template>

<script setup>
defineProps({
  song: {
    type: Object,
    required: true
  },
  onRemove: Function
})
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
  transition: background-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
}

.song-button:hover {
  background-color: #2a9d8f22;
  transform: scale(1.01);
}

.song-button:active {
  background-color: #00ff00;
  box-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00aa;
  transform: scale(0.98);
}

/* ✅ Nouveau style du bouton 🗑 */
.remove-btn {
  background-color: transparent;
  border: none;
  color: #ff5f5f;
  font-size: 1.3rem;
  padding: 0.6rem;
  border-radius: 50%;
  transition: all 0.3s ease;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.remove-btn:hover {
  background-color: rgba(255, 95, 95, 0.1);
  color: #ff4d4d;
  transform: scale(1.2);
  box-shadow: 0 0 8px rgba(255, 80, 80, 0.4);
}

.remove-btn:active {
  transform: scale(0.95);
  background-color: rgba(255, 50, 50, 0.2);
}

.info {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
  width: 100%;
}

.name {
  font-weight: bold;
  color: #0f0;
}

.genre,
.artist,
.date {
  color: #ccc;
  font-size: 0.9rem;
}
</style>