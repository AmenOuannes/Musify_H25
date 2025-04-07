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
form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
