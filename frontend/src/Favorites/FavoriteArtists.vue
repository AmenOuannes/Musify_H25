<template>
  <div class="artist-search">
    <div class="search-container">
      <input
          v-model="searchQuery"
          type="text"
          placeholder="Search your favorite artists..."
          class="search-input"
      />
      <button class="suggested-btn" @click="fetchSuggestedArtists">
        Show Suggested Artists
      </button>
    </div>

    <div class="artist-list">
      <h2 v-if="!showingSuggestions">🎧 Your Liked Artists</h2>
      <h2 v-if="showingSuggestions">🤖 Suggested Artists</h2>

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
import { getLikedArtists, getRecommendedArtists } from '@/api/artistsAPI.js'

const router = useRouter()
const store = useStore()

const artists = ref([])
const searchQuery = ref('')
const token = store.getters.currentToken
const showingSuggestions = ref(false)

const fetchLikedArtists = async () => {
  try {
    const data = await getLikedArtists(searchQuery.value, token)
    artists.value = Array.isArray(data) ? data : data?.artists || []
    showingSuggestions.value = false
  } catch (err) {
    console.error('Error fetching liked artists:', err)
    artists.value = []
  }
}

const fetchSuggestedArtists = async () => {
  try {
    const data = await getRecommendedArtists(token)
    artists.value = Array.isArray(data) ? data : data?.artists || []
    showingSuggestions.value = true
  } catch (err) {
    console.error('Error fetching suggested artists:', err)
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
  gap: 1rem;
  align-items: center;
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

.suggested-btn {
  padding: 10px 15px;
  background-color: #2a9d8f;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-weight: bold;
}

.artist-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
