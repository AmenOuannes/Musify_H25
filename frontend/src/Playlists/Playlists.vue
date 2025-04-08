<template>
  <div class="playlist-search">
    <div class="search-container">
      <div class="search-bar">
        <input
            type="text"
            v-model="searchQuery"
            placeholder="Search for a playlist..."
        />
      </div>
      <div class="add-playlist">
        <button @click="showAddModal = true">Add Playlist</button>
      </div>
    </div>

    <div class="playlist-list">
      <PlaylistDisplay
          v-for="playlist in playlists"
          :key="playlist.playlist_name"
          :playlist="playlist"
          @click="goToPlaylist(playlist.playlist_name)"
      />
    </div>

    <teleport to="body">
      <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
        <div class="modal-content">
          <AddPlaylist @close="handleModalClose" />
        </div>
      </div>
    </teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { getPlaylists } from '@/api/playlistAPI'
import AddPlaylist from '@/Playlists/AddPlaylists.vue'
import PlaylistDisplay from '@/Playlists/PlaylistDisplay.vue'

const router = useRouter()
const playlists = ref([])
const searchQuery = ref('')
const showAddModal = ref(false)

const fetchPlaylists = async () => {
  try {
    const data = await getPlaylists(50, searchQuery.value)
    playlists.value = data.playlists || []
  } catch (err) {
    console.error('Error fetching playlists:', err)
    playlists.value = []
  }
}

const goToPlaylist = (name) => {
  const formatted = name.toLowerCase().replace(/\s+/g, '_')
  router.push({ name: 'PlaylistDetail', params: { name: formatted } })
}

const handleModalClose = () => {
  showAddModal.value = false
  fetchPlaylists()
}

watch(searchQuery, fetchPlaylists)
onMounted(fetchPlaylists)
</script>

<style scoped>
.playlist-search {
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

.add-playlist button {
  padding: 10px 15px;
  border-radius: 20px;
  background-color: #2a9d8f;
  color: white;
  border: none;
  font-weight: bold;
  cursor: pointer;
}

.playlist-list {
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
