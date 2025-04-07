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
          v-for="album in displayedAlbums"
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
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getAlbums } from '@/api/albumAPI'
import AddAlbum from '@/Albums/AddAlbums.vue'
import AlbumDisplay from '@/Albums/AlbumDisplay.vue' // ✅ imported new component

const router = useRouter()
const albums = ref([])
const searchQuery = ref('')
const showAddModal = ref(false)
const showDropdown = ref(false)

const displayedAlbums = computed(() => {
  if (!searchQuery.value) return albums.value
  return albums.value.filter(album =>
      album.album_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      album.artist_name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const fetchAlbums = async () => {
  try {
    const data = await getAlbums(50)
    albums.value = data.albums || []
  } catch (err) {
    console.error('Error fetching albums:', err)
    albums.value = []
  }
}

const handleInput = () => {
  showDropdown.value = searchQuery.value.length > 0
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

.add-album button {
  padding: 10px 15px;
  border-radius: 20px;
  background-color: #2a9d8f;
  color: white;
  border: none;
  font-weight: bold;
  cursor: pointer;
}

.album-list {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  justify-content: flex-start;
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
