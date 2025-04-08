<template>
  <div class="add-playlist-form">
    <h2>Add a Playlist</h2>
    <form @submit.prevent="submitPlaylist">
      <input type="text" v-model="playlist_name" placeholder="Playlist Name" required />

      <label>
        <input type="checkbox" v-model="isPrivate" />
        Private Playlist
      </label>

      <button type="submit" :disabled="loading">
        {{ loading ? 'Creating...' : 'Create Playlist' }}
      </button>

      <p v-if="success">✅ Playlist created successfully!</p>
      <p v-if="error">❌ {{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { postPlaylist } from '@/api/playlistAPI'
import { useStore } from 'vuex'

const playlist_name = ref('')
const isPrivate = ref(false)
const loading = ref(false)
const success = ref(false)
const error = ref(null)

const emit = defineEmits(['close'])
const store = useStore()
const token = store.getters.currentToken

const submitPlaylist = async () => {
  loading.value = true
  error.value = null
  success.value = false

  try {
    await postPlaylist(playlist_name.value, isPrivate.value ? 1 : 0, token)
    success.value = true
    setTimeout(() => emit('close'), 800)
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.add-playlist-form {
  color: white;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

input[type="text"] {
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #444;
  background-color: #333;
  color: white;
}

label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
}

button {
  padding: 0.5rem;
  border-radius: 4px;
  background-color: #2a9d8f;
  color: white;
  border: none;
  cursor: pointer;
  font-weight: bold;
}

button:disabled {
  background-color: #555;
  cursor: not-allowed;
}
</style>
