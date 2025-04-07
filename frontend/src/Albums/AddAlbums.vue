<template>
  <div class="add-album-form">
    <h2>Add an Album</h2>
    <form @submit.prevent="submitAlbum">
      <input type="text" v-model="album_name" placeholder="Album Name" required />
      <input type="text" v-model="genre" placeholder="Genre" required />
      <input v-if="!prefilledArtist" type="text" v-model="artist_name" placeholder="Artist Name" required />
      <input type="date" v-model="release_date" required />
      <input type="text" v-model="image" placeholder="Image URL" required />
      <button type="submit" :disabled="loading">
        {{ loading ? 'Adding...' : 'Add Album' }}
      </button>
      <p v-if="success">✅ Album added successfully!</p>
      <p v-if="error">❌ {{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref, defineProps } from 'vue'
import { postAlbum } from '@/api/albumAPI'
import { useStore } from 'vuex'

const props = defineProps({
  prefilledArtist: String
})

const store = useStore()
const token = store.getters.currentToken
const emit = defineEmits(['close'])

const album_name = ref('')
const genre = ref('')
const artist_name = ref(props.prefilledArtist || '')
const release_date = ref('')
const image = ref('')
const loading = ref(false)
const success = ref(false)
const error = ref(null)

const submitAlbum = async () => {
  loading.value = true
  error.value = null

  try {
    await postAlbum(
        album_name.value,
        genre.value,
        artist_name.value,
        release_date.value,
        image.value,
        token
    )
    success.value = true
    setTimeout(() => {
      emit('close')
    }, 800)
  } catch (err) {
    error.value = err.message || 'Failed to add album'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.add-album-form {
  color: white;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

input {
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #444;
  background-color: #333;
  color: white;
}

button {
  padding: 0.5rem;
  border-radius: 4px;
  background-color: #2a9d8f;
  color: white;
  border: none;
  cursor: pointer;
}

button:disabled {
  background-color: #555;
  cursor: not-allowed;
}
</style>