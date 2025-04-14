<template>
  <div class="song-container">
    <button class="song-button" @click="$emit('click')">
      <div class="info">
        <span class="name">{{ song.song_name }}</span>
        <span class="meta">
          {{ song.genre }} · 🎤 {{ song.artist_name }} · 📅 {{ song.release_date }}
        </span>
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
.song-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
}

.song-button {
  flex-grow: 1;
  display: flex;
  align-items: center;
  background-color: #1e1e1e;
  border: 1px solid #444;
  border-radius: 16px;
  padding: 1.5rem 2rem;
  color: white;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.2s, box-shadow 0.2s;
  text-align: left;
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

.info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  width: 100%;
}

.name {
  font-weight: 700;
  font-size: 1.5rem;
  color: #22c55e;
}

.meta {
  font-size: 1.1rem;
  color: #bbb;
}

/* Remove button */
.remove-btn {
  background-color: transparent;
  border: none;
  color: #ff5f5f;
  font-size: 1.6rem;
  padding: 0.8rem;
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
</style>
