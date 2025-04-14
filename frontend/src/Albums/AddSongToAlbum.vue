<template>
  <div class="add-song-to-album">
    <h2>Add a Song to {{ albumName }}</h2>

    <form @submit.prevent="submit">
      <div class="form-group">
        <label for="song">Select Song:</label>
        <select v-model="selectedSongName" required>
          <option disabled value="">-- Choose a song --</option>
          <option
              v-for="song in filteredSongs"
              :key="song.song_name"
              :value="song.song_name"
          >
            {{ song.song_name }}
          </option>
        </select>
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? 'Adding...' : 'Add Song' }}
      </button>

      <p v-if="success" class="success-message">✅ Song added to album!</p>
      <p v-if="error" class="error-message">❌ {{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { getSongs } from '@/api/songAPI'
import { addSongToAlbum } from '@/api/albumAPI'

const store = useStore()
const token = store.getters.currentToken

const props = defineProps({
  albumName: String,
  artistName: String
})

const emit = defineEmits(['close', 'song-added'])

const selectedSongName = ref('')
const allSongs = ref([])
const filteredSongs = ref([])

const loading = ref(false)
const success = ref(false)
const error = ref(null)

const fetchSongs = async () => {
  try {
    const response = await getSongs(100)
    allSongs.value = response.songs || []

    filteredSongs.value = allSongs.value.filter(
        song => song.artist_name.toLowerCase() === props.artistName.toLowerCase()
    )
  } catch (err) {
    console.error('Error fetching songs:', err)
  }
}

const submit = async () => {
  loading.value = true
  success.value = false
  error.value = null

  try {
    await addSongToAlbum(props.albumName, selectedSongName.value, token)
    success.value = true
    emit('song-added')
    setTimeout(() => emit('close'), 100)
  } catch (err) {
    error.value = 'Failed to add song to album.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchSongs()
})
</script>

<style scoped>
.add-song-to-album {
  color: white;
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #2a9d8f;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
}

select {
  width: 100%;
  padding: 10px;
  background-color: #222;
  border: 1px solid #555;
  border-radius: 5px;
  color: white;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #2a9d8f;
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
</style>
