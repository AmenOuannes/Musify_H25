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
      <div
          class="artist-card"
          v-for="artist in artists"
          :key="artist.artist_name"
          @click="goToArtist(artist.artist_name)"
      >
        <img
            :src="artist.image"
            alt="artist image"
            class="artist-image"
        />
        <div class="artist-info">
          <h3 class="artist-name">
            {{ artist.artist_name }}
            <span v-if="artist.celebrity">⭐</span>
          </h3>
          <p class="artist-genre">{{ artist.genre }}</p>
          <p class="artist-followers">{{ artist.followers.toLocaleString() }} followers</p>
        </div>
      </div>
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
    const data = await getArtists(20, searchQuery.value)
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
  flex-wrap: wrap;
  gap: 1.5rem;
  justify-content: flex-start;
}

.artist-card {
  background-color: #1e1e1e;
  border: 1px solid #444;
  border-radius: 10px;
  padding: 1rem;
  width: 200px;
  cursor: pointer;
  transition: transform 0.2s;
}

.artist-card:hover {
  transform: scale(1.05);
}

.artist-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

.artist-info {
  text-align: center;
}

.artist-name {
  font-size: 1.1rem;
  font-weight: bold;
  color: #2a9d8f;
}

.artist-genre,
.artist-followers {
  font-size: 0.9rem;
  color: #ccc;
}

/* Modal Styles */
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
