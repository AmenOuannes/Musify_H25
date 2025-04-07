<template>
  <button class="artist-button" @click="$emit('click')">
    <div class="info">
      <span class="name">
        {{ artist.artist_name }}
        <span v-if="artist.celebrity">⭐</span>
      </span>
      <span class="genre">{{ artist.genre }}</span>
      <span class="followers">{{ artist.followers.toLocaleString() }} followers</span>
    </div>
  </button>
</template>

<script setup>
defineProps({
  artist: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.artist-button {
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

.artist-button:hover {
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
.followers {
  color: #ccc;
  font-size: 0.9rem;
}
</style>
