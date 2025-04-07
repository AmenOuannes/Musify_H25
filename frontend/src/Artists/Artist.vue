<template>
  <div class="artist-page" v-if="artist">
    <h1>{{ artist.artist_name }} <span v-if="artist.celebrity">⭐</span></h1>
    <img :src="artist.image" alt="Artist Image" class="artist-img" />
    <p><strong>Genre:</strong> {{ artist.genre }}</p>
    <p><strong>Followers:</strong> {{ artist.followers.toLocaleString() }}</p>
    <p>
      <strong>Profile:</strong>
      <a :href="artist.profile_url" target="_blank">{{ artist.profile_url }}</a>
    </p>

    <button class="add-song-btn" @click="showAddModal = true">➕ Add Song</button>

    <teleport to="body">
      <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
        <div class="modal-content">
          <AddSongs :prefilledArtist="artist.artist_name" @close="showAddModal = false" />
        </div>
      </div>
    </teleport>
  </div>

  <div v-else>
    <p>Loading artist...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getArtistByName } from '@/api/artistsAPI'
import AddSongs from '@/Songs/AddSongs.vue'

const route = useRoute()
const artist = ref(null)
const error = ref(null)
const showAddModal = ref(false)

onMounted(async () => {
  try {
    const cleanedName = route.params.name.replace(/_/g, ' ').toLowerCase()
    const data = await getArtistByName(cleanedName)
    artist.value = data
  } catch (err) {
    error.value = 'Artist not found or error occurred.'
    console.error(err)
  }
})
</script>

<style scoped>
.artist-page {
  max-width: 600px;
  margin: 4rem auto;
  color: white;
  background-color: #111;
  padding: 2rem;
  border-radius: 12px;
  border: 1px solid #333;
}

.artist-img {
  width: 100%;
  max-height: 300px;
  object-fit: cover;
  border-radius: 10px;
  margin: 1rem 0;
}

.add-song-btn {
  background-color: #2a9d8f;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  margin-top: 1.5rem;
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



<style scoped>
.artist-page {
  max-width: 600px;
  margin: 4rem auto;
  color: white;
  background-color: #111;
  padding: 2rem;
  border-radius: 12px;
  border: 1px solid #333;
}

.artist-img {
  width: 100%;
  max-height: 300px;
  object-fit: cover;
  border-radius: 10px;
  margin: 1rem 0;
}

h1 {
  font-size: 2rem;
  color: #2a9d8f;
  margin-bottom: 1rem;
}

p {
  margin-bottom: 0.8rem;
}
</style>
