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

      <div class="artist-list suggested-column" :class="{ hidden: !showingSuggestions }">
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
  }
}

const goToArtist = (name) => {
  const formattedName = name.toLowerCase().replace(/\s+/g, '_')
  router.push({ name: 'ArtistDetail', params: { name: formattedName } })
}

onMounted(() => {
  fetchLikedArtists()
  fetchSuggestedArtists()
})

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
  background-color: #121212;
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.search-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1.2rem;
  align-items: center;
  margin-bottom: 2.5rem;
  padding: 0 1rem;
}

.search-input {
  flex: 1;
  min-width: 280px;
  padding: 1.2rem 1.5rem;
  border-radius: 2rem;
  border: none;
  background-color: #282828;
  color: white;
  font-size: 1rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  box-shadow: 0 0 0 3px #1ed760;
}

.suggested-btn {
  padding: 1.2rem 2rem;
  border-radius: 2rem;
  background-color: #1ed760;
  color: white;
  border: none;
  font-weight: bold;
  cursor: pointer;
  font-size: 1.05rem;
  transition: all 0.2s ease;
}

.suggested-btn:hover {
  background-color: #1db954;
  transform: scale(1.03);
}

.artist-columns {
  display: flex;
  flex-direction: row;
  gap: 2.5rem;
  justify-content: space-between;
  padding: 0 1rem;
  align-items: flex-start;
}

.artist-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  min-width: 300px;
}

.artist-list h2 {
  font-size: 1.4rem;
  font-weight: 700;
  color: #1ed760;
  margin-bottom: 0.75rem;
  border-left: 4px solid #1ed760;
  padding-left: 0.75rem;
}

/* Suggested column toggle */
.suggested-column.hidden {
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  height: 0;
  overflow: hidden;
  transition: opacity 0.3s ease;
}

.suggested-column {
  opacity: 1;
  visibility: visible;
  transition: opacity 0.3s ease;
}

@media (max-width: 900px) {
  .artist-columns {
    flex-direction: column;
  }
}
</style>
