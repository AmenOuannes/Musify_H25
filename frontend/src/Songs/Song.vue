<template>
  <div class="song-page" v-if="song">
    <h1>{{ song.song_name }}</h1>
    <p><strong>Genre:</strong> {{ song.genre }}</p>
    <p><strong>Artist:</strong> {{ song.artist_name }}</p>
    <p><strong>Release Date:</strong> {{ song.release_date }}</p>
    <p><strong>URL:</strong> {{ song.url }}</p>

    <YoutubeEmbed :url="song.url" />
  </div>

  <div v-else>
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
  max-width: 800px;
  margin: 3rem auto;
  background-color: #1e1e1e;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 0 15px rgba(0, 255, 0, 0.07);
  color: white;
  line-height: 1.6;
}

.song-page h1 {
  font-size: 2.2rem;
  color: #1abc9c;
  margin-bottom: 1rem;
  font-weight: 700;
}

.song-page p {
  margin: 0.5rem 0;
  font-size: 1.05rem;
}

.song-page p strong {
  color: #0f0;
  font-weight: 600;
}

.song-page a {
  color: #1abc9c;
  text-decoration: underline;
}

.song-page iframe {
  width: 100%;
  max-width: 100%;
  height: 400px;
  border-radius: 10px;
  margin-top: 2rem;
  box-shadow: 0 0 12px rgba(0, 255, 0, 0.1);
}

@media screen and (max-width: 600px) {
  .song-page {
    padding: 1.5rem;
  }

  .song-page iframe {
    height: 250px;
  }
}

</style>
