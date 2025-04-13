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
.add-song-form {
  background-color: #1a1a1a;
  padding: 2rem;
  border-radius: 16px;
  color: white;
  max-width: 500px;
  margin: 0 auto;
  box-shadow: 0 0 25px rgba(0, 255, 0, 0.1);
}

h2 {
  color: #00ff00;
  text-align: center;
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

input {
  padding: 0.75rem 1rem;
  border-radius: 20px;
  border: 1px solid #444;
  background-color: #222;
  color: white;
  font-size: 1rem;
  transition: border-color 0.2s;
}

input:focus {
  border-color: #00ff00;
  outline: none;
}

button {
  padding: 0.75rem 1rem;
  border-radius: 20px;
  background-color: #00ff00;
  color: black;
  font-weight: bold;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #00cc00;
}

button:disabled {
  background-color: #006600;
  cursor: not-allowed;
}

p {
  text-align: center;
  margin-top: 1rem;
  font-size: 0.95rem;
}

p.success {
  color: #00ff00;
}

p.error {
  color: #ff4d4d;
}
</style>


