<template>
  <div class="artist-container">
    <button class="artist-button" @click="$emit('click')">
      <img
          v-if="artist.image"
          :src="artist.image"
          alt="Artist Image"
          class="artist-avatar"
      />
      <div class="info">
        <span class="name">
          {{ artist.artist_name }}
          <span v-if="artist.celebrity">⭐</span>
        </span>
        <span class="meta">
          {{ artist.genre }} · {{ artist.followers.toLocaleString() }} followers
        </span>
      </div>
    </button>

    <button
        v-if="showLikeButton && !liked"
        class="like-button"
        @click.stop="likeArtistHandler"
    >
      ❤️ Like
    </button>

    <span v-else-if="showLikeButton && liked" class="liked-label">
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
    required: true,
  },
  showLikeButton: {
    type: Boolean,
    default: false,
  },
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
  background-color: #1e1e1e;
  border: 1px solid #444;
  border-radius: 16px;
  padding: 1.5rem;
  width: 100%;
  color: white;
  text-align: left;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.2s ease;
  gap: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 255, 0, 0.05);
}

.artist-button:hover {
  background-color: #2a9d8f22;
  transform: scale(1.02);
}

.artist-avatar {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.5);
  border: 2px solid #0f0;
}

.info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 0.5rem;
  flex-grow: 1;
}

.name {
  font-weight: bold;
  font-size: 1.6rem;
  color: #22c55e;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.meta {
  font-size: 1rem;
  color: #aaa;
  font-style: italic;
}

.like-button {
  margin-top: 0.75rem;
  padding: 8px 16px;
  background-color: #0f0;
  color: black;
  border: none;
  border-radius: 25px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.like-button:hover {
  background-color: #1ed760;
}

.liked-label {
  display: inline-block;
  margin-top: 0.75rem;
  padding: 8px 16px;
  color: #0f0;
  font-size: 0.9rem;
  border: 1px solid #0f0;
  border-radius: 25px;
}
</style>
