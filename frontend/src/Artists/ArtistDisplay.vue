<template>
  <div class="artist-container">
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
    <button
        v-if="showLikeButton && !liked"
        class="like-button"
        @click.stop="likeArtistHandler"
    >
      ❤️ Like
    </button>
    <span
        v-else-if="showLikeButton && liked"
        class="liked-label"
    >
      ✅ Liked
    </span>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { likeArtist } from '@/api/artistsAPI.js'
import store from '@/Store/Store.js'

const props = defineProps({
  artist: {
    type: Object,
    required: true
  },
  showLikeButton: {
    type: Boolean,
    default: false
  }
})

const liked = ref(false)

const likeArtistHandler = async () => {
  try {
    const token = store.getters.getToken
    await likeArtist(props.artist.artist_name, token)
    liked.value = true
  } catch (error) {
    console.error('Error liking artist:', error)
    alert('Error adding to favorites')
  }
}
</script>

<style scoped>
.artist-container {
  position: relative;
}

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

.like-button {
  margin-top: 0.5rem;
  padding: 6px 12px;
  background-color: #0f0;
  color: black;
  border: none;
  border-radius: 20px;
  font-size: 0.8rem;
  cursor: pointer;
}

.liked-label {
  display: inline-block;
  margin-top: 0.5rem;
  padding: 6px 12px;
  color: #0f0;
  font-size: 0.8rem;
}
</style>
