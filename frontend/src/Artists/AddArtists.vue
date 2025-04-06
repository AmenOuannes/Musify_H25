<template>
  <div class="add-artist-form">
    <h2>Add a New Artist</h2>
    <form @submit.prevent="submitArtist">
      <div class="form-group">
        <label for="artist_name">Artist Name:</label>
        <input
            type="text"
            v-model="artist_name"
            id="artist_name"
            required
        />
      </div>

      <div class="form-group">
        <label for="genre">Genre:</label>
        <input
            type="text"
            v-model="genre"
            id="genre"
            required
        />
      </div>

      <div class="form-group">
        <label for="profile_url">Profile URL:</label>
        <input
            type="url"
            v-model="profile_url"
            id="profile_url"
            required
        />
      </div>

      <div class="form-group">
        <label for="image">Image URL:</label>
        <input
            type="url"
            v-model="image"
            id="image"
            required
        />
      </div>

      <div class="form-group">
        <label for="followers">Followers:</label>
        <input
            type="number"
            v-model="followers"
            id="followers"
            required
        />
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? 'Adding...' : 'Add Artist' }}
      </button>

      <p v-if="success">✅ Artist added successfully!</p>
      <p v-if="error">❌ {{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { postArtists } from '@/api/artistsAPI'

const store = useStore()
const token = store.getters.currentToken

const emit = defineEmits(['close'])

const artist_name = ref('')
const genre = ref('')
const profile_url = ref('')
const image = ref('')
const followers = ref(0)

const loading = ref(false)
const success = ref(false)
const error = ref(null)

const submitArtist = async () => {
  loading.value = true
  success.value = false
  error.value = null

  try {
    await postArtists(
        artist_name.value,
        genre.value,
        profile_url.value,
        image.value,
        followers.value,
        token
    )
    success.value = true

    setTimeout(() => {
      emit('close') // Close modal and trigger parent refresh
    }, 1000)
  } catch (err) {
    error.value = 'Failed to add artist.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.add-artist-form {
  max-width: 400px;
  margin: 4rem auto;
  background-color: #1e1e1e;
  padding: 2rem;
  border-radius: 10px;
  color: white;
  border: 1px solid #444;
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

input {
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
