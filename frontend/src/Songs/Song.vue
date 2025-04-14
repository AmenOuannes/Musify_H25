<template>
  <div class="song-page" v-if="song">
    <div class="song-hero">
      <div class="song-hero-info">
        <h1>{{ song.song_name }}</h1>
        <div class="meta-block">
          <p><strong>Genre:</strong> {{ song.genre }}</p>
          <p><strong>Artist:</strong> {{ song.artist_name }}</p>
          <p><strong>Release Date:</strong> {{ formatDate(song.release_date) }}</p>
          <button
              v-if="song.url"
              class="url-button"
              @click="openSongUrl"
          >
            🎬 Open on YouTube
          </button>
        </div>
      </div>
    </div>

    <div class="player-section" v-if="song.url">
      <YoutubeEmbed :url="song.url" />
    </div>
  </div>

  <div v-else class="loading">
    <p>Loading song...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getSongByName } from '@/api/songAPI'
import YoutubeEmbed from '@/components/YoutubeEmbed.vue'

const route = useRoute()
const song = ref(null)

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

const openSongUrl = () => {
  if (song.value?.url) {
    window.open(song.value.url, '_blank')
  }
}

onMounted(async () => {
  try {
    const cleaned = route.params.name.replace(/_/g, ' ').toLowerCase()
    const data = await getSongByName(cleaned)
    song.value = data
  } catch (err) {
    console.error('Failed to load song:', err)
  }
})
</script>

<style scoped>
.song-page {
  padding: 2rem;
  background-color: #111;
  color: #f0f0f0;
  max-width: 1000px;
  margin: auto;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.song-hero {
  background-color: #1a1a1a;
  border-radius: 20px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
  text-align: center;
}

.song-hero-info h1 {
  font-size: 2rem;
  font-weight: 800;
  color: #22c55e;
  margin-bottom: 1rem;
}

.meta-block {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  font-size: 1.05rem;
}

.meta-block p {
  margin: 0;
}

.meta-block p strong {
  color: #0f0;
}

.url-button {
  margin-top: 1.5rem;
  background-color: #1ed760;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 2rem;
  font-weight: bold;
  cursor: pointer;
  color: #111;
  transition: all 0.3s ease;
}

.url-button:hover {
  background-color: #1db954;
  transform: scale(1.05);
}

.player-section {
  margin: 2rem auto 0;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 0 15px rgba(0, 255, 0, 0.1);
  width: 640px;
  height: 360px;
  display: flex;
  justify-content: center;
}

.player-section iframe {
  width: 100%;
  height: 100%;
  border: none;
  border-radius: 16px;
}

.loading {
  text-align: center;
  color: #aaa;
  padding: 2rem;
}

@media (max-width: 700px) {
  .player-section {
    width: 100%;
    height: auto;
    aspect-ratio: 16 / 9;
  }

  .player-section iframe {
    width: 100%;
    height: 100%;
  }

  .song-hero-info h1 {
    font-size: 1.6rem;
  }

  .meta-block {
    font-size: 0.95rem;
  }

  .url-button {
    width: 100%;
  }
}
</style>
