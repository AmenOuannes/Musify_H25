<template>
  <div class="playlist-player" v-if="songs.length > 0">
    <h2>Now Playing: {{ songs[currentIndex].song_name }}</h2>
    <YoutubeEmbed :url="songs[currentIndex].url" @ended="nextSong" />

    <p class="next-text">
      Next up:
      <span v-if="songs.length > 1">
        {{ songs[(currentIndex + 1) % songs.length].song_name }}
      </span>
    </p>

    <div class="controls">
      <button @click="prevSong">⏮ Previous</button>
      <button @click="nextSong">Next ⏭</button>
    </div>
  </div>

  <div v-else>
    <p>Loading playlist...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getPlaylistSongs } from '@/api/playlistAPI'
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
    const playlistName = route.params.name.replace(/_/g, ' ').toLowerCase()
    const owner = route.query.owner?.toLowerCase() || ''
    const result = await getPlaylistSongs(playlistName, owner)
    songs.value = result.songs || []
  } catch (err) {
    console.error('Failed to load playlist songs:', err)
  }
})
</script>

<style scoped>
.playlist-player {
  padding: 2rem;
  color: white;
  background-color: #111;
  text-align: center;
}

.controls {
  margin-top: 2rem;
  display: flex;
  justify-content: center;
  gap: 2rem;
}

.next-text {
  margin-top: 1rem;
  font-style: italic;
  color: #ccc;
}

button {
  background-color: #2a9d8f;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 10px;
  font-weight: bold;
  cursor: pointer;
}
</style>
