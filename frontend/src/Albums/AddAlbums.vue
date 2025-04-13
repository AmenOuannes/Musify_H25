<template>
  <div class="add-album-form">
    <h2>Add an Album</h2>
    <form @submit.prevent="submitAlbum">
      <input type="text" v-model="album_name" placeholder="Album Name" required />
      <input type="text" v-model="genre" placeholder="Genre" required />

      <input
          v-if="!prefilledArtist"
          type="text"
          v-model="artist_name"
          placeholder="Artist Name"
          required
      />

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
import { ref, defineProps, watchEffect } from 'vue'
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
const artist_name = ref('')
const release_date = ref('')
const image = ref('')
const loading = ref(false)
const success = ref(false)
const error = ref(null)

watchEffect(() => {
  if (props.prefilledArtist) {
    artist_name.value = props.prefilledArtist
  }
})

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
  background: #1e1e1e;
  color: white;
  padding: 2rem;
  border-radius: 16px;
  max-width: 500px;
  margin: 0 auto;
  box-shadow: 0 0 15px rgba(0, 255, 0, 0.05);
}

form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

input {
  padding: 0.9rem 1rem;
  border-radius: 10px;
  border: 1px solid #444;
  background-color: #333;
  color: white;
  font-size: 0.95rem;
  transition: border 0.3s, box-shadow 0.3s;
}

input::placeholder {
  color: #aaa;
}

input:focus {
  border-color: #0f0;
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 255, 0, 0.2);
}

button {
  padding: 1rem;
  border-radius: 10px;
  background-color: #0f0;
  color: white; /* ✅ texte blanc */
  font-weight: bold;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

button:disabled {
  background-color: #555;
  cursor: not-allowed;
}

button:hover:enabled {
  background-color: #00e600;
}

</style>

