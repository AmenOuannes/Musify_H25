<template>
  <div class="add-song-to-album">
    <h3>Add Song to {{ albumName }}</h3>
    <div class="search-container">
      <input
          type="text"
          v-model="searchQuery"
          placeholder="Search for a song..."
          @input="handleSearch"
      />
      <div v-if="showDropdown && filteredSongs.length > 0" class="search-dropdown">
        <div
            v-for="song in filteredSongs"
            :key="song.song_name"
            class="dropdown-item"
            @click="selectSong(song)"
        >
          {{ song.song_name }} - {{ song.artist_name }}
        </div>
      </div>
    </div>
    <button @click="addSong" :disabled="!selectedSong || loading">
      {{ loading ? 'Adding...' : 'Add Song' }}
    </button>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">{{ success }}</p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { getSongs } from '@/api/songAPI'
import { addSongToAlbum } from '@/api/albumAPI'
import { useStore } from 'vuex'

const props = defineProps({
  albumName: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['close', 'song-added'])

const store = useStore()
const token = store.getters.currentToken
const searchQuery = ref('')
const songs = ref([])
const selectedSong = ref(null)
const showDropdown = ref(false)
const loading = ref(false)
const error = ref(null)
const success = ref(null)

const filteredSongs = computed(() => {
  if (!searchQuery.value) return []
  return songs.value.filter(song =>
      song.song_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      song.artist_name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const handleSearch = () => {
  showDropdown.value = searchQuery.value.length > 0
}

const selectSong = (song) => {
  selectedSong.value = song
  searchQuery.value = song.song_name
  showDropdown.value = false
}

const fetchSongs = async () => {
  try {
    const data = await getSongs(50)
    songs.value = data.songs || []
  } catch (err) {
    console.error('Error fetching songs:', err)
    songs.value = []
  }
}

const addSong = async () => {
  if (!selectedSong.value) return

  loading.value = true
  error.value = null
  success.value = null

  try {
    await addSongToAlbum(
        props.albumName,
        selectedSong.value.song_name,
        token
    )
    success.value = 'Song added successfully!'
    setTimeout(() => {
      emit('song-added')
      emit('close')
    }, 1000)
  } catch (err) {
    error.value = err.message || 'Failed to add song to album'
  } finally {
    loading.value = false
  }
}

fetchSongs()
</script>

<style scoped>
.add-song-to-album {
  color: white;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.search-container {
  position: relative;
}

.search-container input {
  padding: 8px 12px;
  width: 100%;
  border-radius: 4px;
  border: 1px solid #444;
  background-color: #333;
  color: white;
}

.search-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  max-height: 200px;
  overflow-y: auto;
  background-color: #333;
  border: 1px solid #444;
  border-radius: 0 0 4px 4px;
  z-index: 10;
}

.dropdown-item {
  padding: 8px 12px;
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: #2a9d8f;
}

button {
  padding: 8px 16px;
  background-color: #2a9d8f;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #555;
  cursor: not-allowed;
}

.error {
  color: #ff6b6b;
}

.success {
  color: #51cf66;
}
</style>