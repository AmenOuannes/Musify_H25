<template>
  <div class="artist-search">
    <div class="search-container">
      <input
          v-model="searchQuery"
          type="text"
          placeholder="Search your favorite artists..."
          class="search-input"
          :disabled="showingSuggestions"
      />
      <button class="suggested-btn" @click="toggleSuggestions">
        {{ showingSuggestions ? 'Hide Suggested Artists' : 'Show Suggested Artists' }}
      </button>
    </div>

    <div class="artist-columns">
      <div class="artist-list">
        <h2>🎧 Your Liked Artists</h2>
        <ArtistDisplay
            v-for="artist in likedArtists"
            :key="artist.artist_name"
            :artist="artist"
            @click="goToArtist(artist.artist_name)"
        />
      </div>

      <div v-if="showingSuggestions" class="artist-list">
        <h2>🤖 Suggested Artists</h2>
        <ArtistDisplay
            v-for="artist in suggestedArtists"
            :key="artist.artist_name"
            :artist="artist"
            @click="goToArtist(artist.artist_name)"
        />
      </div>
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

const likedArtists = ref([])
const suggestedArtists = ref([])
const searchQuery = ref('')
const token = store.getters.currentToken
const showingSuggestions = ref(false)

const fetchLikedArtists = async () => {
  try {
    const data = await getLikedArtists(searchQuery.value, token)
    likedArtists.value = Array.isArray(data) ? data : data?.artists || []
  } catch (err) {
    console.error('Error fetching liked artists:', err)
    likedArtists.value = []
  }
}

const fetchSuggestedArtists = async () => {
  try {
    const data = await getRecommendedArtists(token)
    suggestedArtists.value = Array.isArray(data) ? data : data?.artists || []
  } catch (err) {
    console.error('Error fetching suggested artists:', err)
    suggestedArtists.value = []
  }
}

const toggleSuggestions = async () => {
  showingSuggestions.value = !showingSuggestions.value
  if (showingSuggestions.value && suggestedArtists.value.length === 0) {
    await fetchSuggestedArtists()
  } else {
    await fetchLikedArtists()
  }
}

const goToArtist = (name) => {
  const formattedName = name.toLowerCase().replace(/\s+/g, '_')
  router.push({ name: 'ArtistDetail', params: { name: formattedName } })
}

onMounted(fetchLikedArtists)

watch(searchQuery, async () => {
  if (!showingSuggestions.value) {
    await fetchLikedArtists()
  }
})
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

.artist-columns {
  display: flex;
  gap: 4rem;
  justify-content: space-between;
}

.artist-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>

