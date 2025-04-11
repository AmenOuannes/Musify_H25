<template>
  <div class="artist-search">
    <div class="search-container">
      <input
          v-model="searchQuery"
          type="text"
          placeholder="Search your favorite artists..."
          class="search-input"
      />
    </div>

    <div class="artist-list">
      <ArtistDisplay
          v-for="artist in artists"
          :key="artist.artist_name"
          :artist="artist"
          @click="goToArtist(artist.artist_name)"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import ArtistDisplay from '@/Artists/ArtistDisplay.vue'
import { getLikedArtists } from '@/api/artistsAPI.js'

const router = useRouter()
const store = useStore()

const artists = ref([])
const searchQuery = ref('')
const token = store.getters.currentToken

const fetchLikedArtists = async () => {
  try {
    const data = await getLikedArtists(searchQuery.value, token)
    artists.value = Array.isArray(data) ? data : data?.artists || []
  } catch (err) {
    console.error('Error fetching liked artists:', err)
    artists.value = []
  }
}

const goToArtist = (name) => {
  const formattedName = name.toLowerCase().replace(/\s+/g, '_')
  router.push({ name: 'ArtistDetail', params: { name: formattedName } })
}

onMounted(fetchLikedArtists)
watch(searchQuery, fetchLikedArtists)
</script>

<style scoped>
.artist-search {
  padding: 2rem;
  color: white;
  background-color: #111;
}

.search-container {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 2rem;
}

.search-input {
  padding: 10px 15px;
  border-radius: 20px;
  border: 1px solid #888;
  background-color: #222;
  color: white;
  width: 250px;
}

.artist-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
