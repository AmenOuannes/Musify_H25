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
          :showDelete="true"
          @click="goToPlaylist(playlist.playlist_name)"
          @delete="confirmDelete(playlist.playlist_name)"
      />
    </div>

    <teleport to="body">
      <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
        <div class="modal-content">
          <AddPlaylist @close="handleModalClose" />
        </div>
      </div>
    </teleport>

    <teleport to="body">
      <div v-if="confirmPopup" class="modal-overlay" @click.self="confirmPopup = false">
        <div class="modal-content">
          <h3>Confirm Deletion</h3>
          <p>Are you sure you want to delete the playlist "{{ playlistToDelete }}"?</p>
          <div class="popup-actions">
            <button @click="performDelete" class="confirm-btn">Yes</button>
            <button @click="confirmPopup = false" class="cancel-btn">Cancel</button>
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { getPlaylists, deletePlaylist } from '@/api/playlistAPI'
import AddPlaylist from '@/MyPlaylists/AddPlaylists.vue'
import PlaylistDisplay from '@/Playlists/PlaylistDisplay.vue'

const router = useRouter()
const store = useStore()

const playlists = ref([])
const searchQuery = ref('')
const showAddModal = ref(false)

const confirmPopup = ref(false)
const playlistToDelete = ref(null)

const username = store.getters.currentUser.username
const token = store.getters.currentToken

const fetchPlaylists = async () => {
  try {
    const data = await getPlaylists(50, searchQuery.value, username)
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

const confirmDelete = (name) => {
  playlistToDelete.value = name
  confirmPopup.value = true
}

const performDelete = async () => {
  try {
    await deletePlaylist(playlistToDelete.value, token)
    confirmPopup.value = false
    await fetchPlaylists()
  } catch (err) {
    console.error('Failed to delete playlist:', err)
    alert('Failed to delete playlist. Try again later.')
  }
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
  background-color: #0f0;
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
  color: white;
}

.popup-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 1.5rem;
  gap: 1rem;
}

.confirm-btn,
.cancel-btn {
  flex: 1;
  padding: 10px;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.confirm-btn {
  background-color: #e63946;
  color: white;
}

.cancel-btn {
  background-color: #aaa;
  color: #111;
}
</style>
