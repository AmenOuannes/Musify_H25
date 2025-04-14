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
import ArtistDisplay from '@/Artists/ArtistDisplay.vue'

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
  background-color: #121212;
}

.search-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  align-items: center;
  margin-bottom: 3rem;
  padding: 0 1rem;
}

.search-bar {
  flex: 1 1 200px;
}

.search-bar input {
  width: 100%;
  padding: 1.2rem 1.5rem;
  border-radius: 2rem;
  border: none;
  background-color: #282828;
  color: white;
  font-size: 1rem;
  box-shadow: 0 2px 6px rgba(0,0,0,0.3);
  transition: all 0.2s ease;
}

.search-bar input:focus {
  outline: none;
  box-shadow: 0 0 0 3px #1ed760;
}

.add-artist {
  margin-left: 2rem;
}

.add-artist button {
  padding: 1.2rem 2rem;
  border-radius: 2rem;
  background-color: #1ed760;
  color: white;
  border: none;
  font-weight: bold;
  cursor: pointer;
  font-size: 1.1rem;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.add-artist button:hover {
  background-color: #1db954;
  transform: scale(1.03);
}

.artist-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2rem;
  padding: 1rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0,0,0,0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
  padding: 2rem;
}

.modal-content {
  background-color: #282828;
  padding: 3rem;
  border-radius: 1.5rem;
  width: 100%;
  max-width: 550px;
  border: 2px solid #1ed760;
  box-shadow: 0 6px 25px rgba(30, 215, 96, 0.3);
}

@media (max-width: 600px) {
  .artist-search {
    padding: 1.5rem;
  }

  .search-container {
    flex-direction: column;
    gap: 1.5rem;
    padding: 0;
  }

  .search-bar,
  .add-artist {
    width: 100%;
  }

  .add-artist {
    margin-left: 0;
    margin-top: 1rem;
  }

  .artist-list {
    grid-template-columns: 1fr;
    gap: 1.5rem;
    padding: 0.5rem;
  }

  .modal-content {
    padding: 2rem;
  }
}

@media (hover: none) {
  .add-artist button {
    padding: 1.3rem 2.2rem;
  }

  .search-bar input {
    padding: 1.3rem 1.8rem;
  }
}
</style>