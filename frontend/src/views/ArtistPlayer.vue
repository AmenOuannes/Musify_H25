<template>
  <div class="artist-player" v-if="songs.length > 0">
    <h2 class="now-playing">🎵 Now Playing</h2>
    <h1 class="song-title">{{ songs[currentIndex].song_name }}</h1>

    <div class="video-wrapper">
      <YoutubeEmbed :url="songs[currentIndex].url" @ended="nextSong" />
    </div>

    <p class="next-text">
      <span>⏭ Next Up:</span>
      <strong v-if="songs.length > 1">
        {{ songs[(currentIndex + 1) % songs.length].song_name }}
      </strong>
    </p>

    <div class="controls">
      <button @click="prevSong">⏮ Previous</button>
      <button @click="nextSong">Next ⏭</button>
    </div>
  </div>

  <div v-else class="loading">
    <p>🎧 Loading artist's songs...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getArtistsSongs } from '@/api/artistsAPI'
import YoutubeEmbed from '@/components/YoutubeEmbed.vue'

const route = useRoute()
const songs = ref([])
const currentIndex = ref(0)

const nextSong = () => {
  currentIndex.value = (currentIndex.value + 1) % songs.value.length
}

const prevSong = () => {
  currentIndex.value = (currentIndex.value - 1 + songs.value.length) % songs.value.length
}

onMounted(async () => {
  try {
    const artistName = route.params.name.replace(/_/g, ' ').toLowerCase()
    const result = await getArtistsSongs(artistName)
    songs.value = result.songs || []
  } catch (err) {
    console.error('Failed to load artist songs:', err)
  }
})
</script>

<style scoped>
.artist-player {
  padding: 3rem 2rem;
  background-color: #121212;
  color: white;
  text-align: center;
  max-width: 1000px;
  margin: auto;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.now-playing {
  font-size: 1.5rem;
  color: #1ed760;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.song-title {
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: #fff;
  background: linear-gradient(90deg, #1ed760, #2a9d8f);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.video-wrapper {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 0 25px rgba(30, 215, 96, 0.2);
  max-width: 640px;
  margin: 0 auto;
}

iframe {
  width: 100%;
  height: 65vh;
  max-height: 650px;
  border: none;
  border-radius: 10px;
}

.next-text {
  margin-top: 1.5rem;
  font-size: 1rem;
  color: #ccc;
}

.next-text strong {
  color: #1ed760;
  font-weight: 600;
}

.controls {
  margin-top: 2.5rem;
  display: flex;
  justify-content: center;
  gap: 2rem;
}

button {
  padding: 12px 24px;
  font-size: 1rem;
  border: none;
  border-radius: 30px;
  font-weight: bold;
  background: linear-gradient(135deg, #1ed760, #2a9d8f);
  color: black;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

button:hover {
  transform: scale(1.05);
  background: linear-gradient(135deg, #2a9d8f, #1ed760);
}

.loading {
  text-align: center;
  color: #bbb;
  font-size: 1.2rem;
  padding: 4rem;
}
</style>
