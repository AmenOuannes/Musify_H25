<template>
  <div class="add-song-form">
    <h2>Add a Song</h2>
    <form @submit.prevent="submitSong">
      <input type="text" v-model="song_name" placeholder="Song Name" required />
      <input type="text" v-model="genre" placeholder="Genre" required />
      <input v-if="!prefilledArtist" type="text" v-model="artist_name" placeholder="Artist Name" required />
      <input type="date" v-model="release_date" required />
      <input type="text" v-model="url" placeholder="URL" required />
      <button type="submit" :disabled="loading">
        {{ loading ? 'Adding...' : 'Add Song' }}
      </button>
      <p v-if="success">✅ Song added successfully!</p>
      <p v-if="error">❌ {{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref, defineProps } from 'vue'
import { postSong } from '@/api/songAPI'
import { useStore } from 'vuex'

const props = defineProps({
  prefilledArtist: String
})

const store = useStore()
const token = store.getters.currentToken
const emit = defineEmits(['close'])

const song_name = ref('')
const genre = ref('')
const artist_name = ref(props.prefilledArtist || '')
const release_date = ref('')
const url = ref('')
const loading = ref(false)
const success = ref(false)
const error = ref(null)

const submitSong = async () => {
  loading.value = true
  error.value = null

  try {
    await postSong(song_name.value, genre.value, artist_name.value, release_date.value, url.value, token)
    success.value = true
    setTimeout(() => {
      emit('close')
    }, 800)
  } catch (err) {
    error.value = 'Request failed with status code 400'
  } finally {
    loading.value = false
  }
}
</script>



<style scoped>
.album-search {
  padding: 2rem;
  color: white;
  background-color: #111;
}

.search-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
}

.search-bar input {
  padding: 10px 15px;
  border-radius: 20px;
  border: 1px solid #888;
  width: 250px;
  background-color: #222;
  color: white;
}

.add-album button {
  padding: 10px 15px;
  border-radius: 20px;
  background-color: #0f0;;
  color: white;
  border: none;
  font-weight: bold;
  cursor: pointer;
}

.album-list {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  justify-content: flex-start;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-content {
  background-color: #222;
  padding: 2rem;
  border-radius: 10px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 0 10px black;
}
</style>

