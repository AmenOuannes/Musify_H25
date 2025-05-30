<template>
  <div class="add-song-to-playlist">
    <h2>Add a Song to {{ playlistName }}</h2>

    <form @submit.prevent="submit">
      <div class="form-group">
        <label for="search">Search for a song:</label>
        <input
            type="text"
            v-model="searchQuery"
            placeholder="Search for a song..."
            @input="handleInput"
            @blur="hideDropdown"
            required
        />
        <ul v-if="showDropdown" class="dropdown-list">
          <li
              v-for="song in displayedSongs"
              :key="song.song_name"
              @mousedown.prevent="selectSong(song.song_name)"
          >
            {{ song.song_name }} — {{ song.artist_name }}
          </li>
        </ul>
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? 'Adding...' : 'Add Song' }}
      </button>

      <p v-if="success" class="success-message">✅ Song added successfully!</p>
      <p v-if="error" class="error-message">❌ {{ error }}</p>
    </form>

    <div v-if="recommendations.length > 0" class="recommendations-section">
      <h3>🎵 Recommended Songs</h3>
      <ul class="recommendation-list">
        <li
            v-for="song in recommendations"
            :key="song.song_name"
            @click="selectSong(song.song_name)"
        >
          {{ song.song_name }} — {{ song.artist_name }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { postSongToPlaylist, getSongsRecommendation } from '@/api/playlistAPI.js'
import { getSongs } from '@/api/songAPI.js'
import { useStore } from 'vuex'

const props = defineProps({
  playlistName: String
})
const emit = defineEmits(['close', 'song-added'])

const store = useStore()
const token = store.getters.currentToken

const searchQuery = ref('')
const showDropdown = ref(false)
const allSongs = ref([])
const selectedSong = ref('')
const loading = ref(false)
const success = ref(false)
const error = ref(null)
const recommendations = ref([])

const displayedSongs = computed(() => {
  return allSongs.value.filter(song =>
      song.song_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      song.artist_name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const fetchSongs = async () => {
  try {
    const result = await getSongs(100)
    allSongs.value = result.songs || []
  } catch (err) {
    console.error('Error fetching songs for dropdown:', err)
  }
}

const fetchRecommendations = async () => {
  try {
    const result = await getSongsRecommendation(props.playlistName, token)
    recommendations.value = result.songs || []
  } catch (err) {
    console.error('Error fetching recommendations:', err)
  }
}

const handleInput = () => {
  showDropdown.value = searchQuery.value.length > 0
}

const hideDropdown = () => {
  setTimeout(() => {
    showDropdown.value = false
  }, 200)
}

const selectSong = (name) => {
  searchQuery.value = name
  selectedSong.value = name
  showDropdown.value = false
}

const submit = async () => {
  loading.value = true
  success.value = false
  error.value = null

  try {
    await postSongToPlaylist(props.playlistName, selectedSong.value || searchQuery.value, token)
    success.value = true
    emit('song-added')
    setTimeout(() => emit('close'), 1000)
  } catch (err) {
    error.value = 'Failed to add song'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await fetchSongs()
  await fetchRecommendations()
})
</script>

<style scoped>
.add-song-to-playlist {
  color: white;
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #0f0;
}

.form-group {
  margin-bottom: 1rem;
  position: relative;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #ccc;
}

input {
  width: 100%;
  padding: 10px;
  background-color: #222;
  border: 1px solid #555;
  border-radius: 5px;
  color: white;
}

.dropdown-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background-color: #333;
  border: 1px solid #444;
  border-radius: 0 0 10px 10px;
  list-style: none;
  margin: 0;
  padding: 0;
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
}

.dropdown-list li {
  padding: 10px 15px;
  cursor: pointer;
}

.dropdown-list li:hover {
  background-color: #2a9d8f55;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #0f0;
  color: white;
  border: none;
  border-radius: 5px;
  font-weight: bold;
  cursor: pointer;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.success-message {
  margin-top: 1rem;
  color: #3ccf7a;
  text-align: center;
}

.error-message {
  margin-top: 1rem;
  color: #f87171;
  text-align: center;
}

.recommendations-section {
  margin-top: 2rem;
}

.recommendations-section h3 {
  margin-bottom: 0.5rem;
  color: #0f0;
}

.recommendation-list {
  list-style: none;
  padding: 0;
  margin: 0;
  background-color: #333;
  border-radius: 10px;
  border: 1px solid #444;
}

.recommendation-list li {
  padding: 10px 15px;
  cursor: pointer;
}

.recommendation-list li:hover {
  background-color: #2a9d8f55;
}
</style>
