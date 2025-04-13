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
  display: block;
  width: 100%;
  background-color: #1e1e1e;
  color: white;
  padding: 1.2rem 1.5rem;
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

.info {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  align-items: center;
  font-size: 0.95rem;
}

.name {
  font-weight: 600;
  color: #0f0;
  background-color: rgba(26, 188, 156, 0.1);
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
}

.genre {
  color: #ccc;
  font-weight: 500;
}

.artist {
  color: #f1f1f1;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.date {
  font-size: 0.9rem;
  color: #999;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

</style>
