<template>
  <div class="song-page" v-if="song">
    <h1>{{ song.song_name }}</h1>
    <p><strong>Genre:</strong> {{ song.genre }}</p>
    <p><strong>Artist:</strong> {{ song.artist_name }}</p>
    <p><strong>Release Date:</strong> {{ song.release_date }}</p>
    <p><strong>URL:</strong> {{ song.url }}</p>
  </div>

  <div v-else>
    <p>Loading song...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getSongByName } from '@/api/songAPI'

const route = useRoute()
const song = ref(null)

onMounted(async () => {
  try {
    const cleaned = route.params.name.replace(/_/g, ' ').toLowerCase()
    const data = await getSongByName(cleaned)
    song.value = data // ✅ direct object, not `data.song`
  } catch (err) {
    console.error('Failed to load song:', err)
  }
})
</script>


<style scoped>
.card {
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 1rem;
  width: 300px;
}
</style>
