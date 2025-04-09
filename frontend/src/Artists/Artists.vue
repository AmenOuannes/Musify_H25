<template>
  <div class="artist-search">
    <div class="search-container">
      <div class="search-bar">
        <input
            type="text"
            v-model="searchQuery"
            placeholder="Search for an artist..."
            @input="handleInput"
            @blur="hideDropdown"
        />
      </div>
      <div class="add-artist">
        <button @click="showAddModal = true">Add Artist</button>
      </div>
    </div>

    <div class="artist-list">
      <ArtistDisplay
          v-for="artist in artists"
          :key="artist.artist_name"
          :artist="artist"
          @click="goToArtist(artist.artist_name)"
      />
    </div>

    <!-- MODAL -->
    <teleport to="body">
      <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
        <div class="modal-content">
          <AddArtist @close="handleModalClose" />
        </div>
      </div>
    </teleport>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getArtists } from '@/api/artistsAPI'
import AddArtist from '@/Artists/AddArtists.vue'
import ArtistDisplay from '@/Artists/ArtistDisplay.vue' // ✅ imported component

const router = useRouter()
const artists = ref([])
const searchQuery = ref('')
const showDropdown = ref(false)
const showAddModal = ref(false)

const handleInput = () => {
  showDropdown.value = searchQuery.value.length > 0
  fetchArtists()
}

const hideDropdown = () => {
  setTimeout(() => {
    showDropdown.value = false
  }, 200)
}

const goToArtist = (name) => {
  const formattedName = name.toLowerCase().replace(/\s+/g, '_')
  router.push({ name: 'ArtistDetail', params: { name: formattedName } })
}

const fetchArtists = async () => {
  try {
    const data = await getArtists(25, searchQuery.value)
    artists.value = data.artists || []
  } catch (err) {
    console.error('Error fetching artists:', err)
    artists.value = []
  }
}

const handleModalClose = () => {
  showAddModal.value = false
  fetchArtists()
}

onMounted(() => {
  fetchArtists()
})
</script>

<style scoped>
.artist-search {
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

.add-artist button {
  padding: 10px 15px;
  border-radius: 20px;
  background-color: #2a9d8f;
  color: white;
  border: none;
  font-weight: bold;
  cursor: pointer;
}

.artist-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
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
