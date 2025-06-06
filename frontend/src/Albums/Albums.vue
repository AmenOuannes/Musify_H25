<template>
  <div class="album-search">
    <div class="search-container">
      <div class="search-bar">
        <input
            type="text"
            v-model="searchQuery"
            placeholder="Search for an album..."
            @input="handleInput"
            @blur="hideDropdown"
        />
      </div>
      <div class="add-album">
        <button @click="showAddModal = true">Add Album</button>
      </div>
    </div>

    <div class="album-list">
      <AlbumDisplay
          v-for="album in albums"
          :key="album.album_name"
          :album="album"
          @click="goToAlbum(album.album_name)"
      />
    </div>

    <teleport to="body">
      <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
        <div class="modal-content">
          <AddAlbum @close="handleModalClose" />
        </div>
      </div>
    </teleport>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getAlbums } from '@/api/albumAPI'
import AddAlbum from '@/Albums/AddAlbums.vue'
import AlbumDisplay from '@/Albums/AlbumDisplay.vue'

const router = useRouter()
const albums = ref([])
const searchQuery = ref('')
const showAddModal = ref(false)
const showDropdown = ref(false)

const fetchAlbums = async () => {
  try {
    const data = await getAlbums(25, searchQuery.value)
    albums.value = (data.albums || []).map(album => ({
      ...album,
      image: album.cover_image || '' // ✅ map to what AlbumDisplay expects
    }))
  } catch (err) {
    console.error('Error fetching albums:', err)
    albums.value = []
  }
}

const handleInput = () => {
  showDropdown.value = searchQuery.value.length > 0
  fetchAlbums()
}

const hideDropdown = () => {
  setTimeout(() => {
    showDropdown.value = false
  }, 200)
}

const goToAlbum = (name) => {
  const formatted = name.toLowerCase().replace(/\s+/g, '_')
  router.push({ name: 'AlbumDetail', params: { name: formatted } })
}

const handleModalClose = () => {
  showAddModal.value = false
  fetchAlbums()
}

onMounted(() => {
  fetchAlbums()
})
</script>

<style scoped>
.album-search {
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

.add-album {
  margin-left: 2rem;
}

.add-album button {
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

.add-album button:hover {
  background-color: #1db954;
  transform: scale(1.03);
}

.album-list {
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
</style>
