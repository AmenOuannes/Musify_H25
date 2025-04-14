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
    const data = await getPlaylists(50, searchQuery.value,1, username)
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
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
  transition: all 0.2s ease;
}

.search-bar input:focus {
  outline: none;
  box-shadow: 0 0 0 3px #1ed760;
}

.add-playlist {
  margin-left: 2rem;
}

.add-playlist button {
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

.add-playlist button:hover {
  background-color: #1db954;
  transform: scale(1.03);
}

.playlist-list {
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

@media (max-width: 600px) {
  .playlist-search {
    padding: 1.5rem;
  }

  .search-container {
    flex-direction: column;
    gap: 1.5rem;
    padding: 0;
  }

  .search-bar,
  .add-playlist {
    width: 100%;
  }

  .add-playlist {
    margin-left: 0;
    margin-top: 1rem;
  }

  .playlist-list {
    grid-template-columns: 1fr;
    gap: 1.5rem;
    padding: 0.5rem;
  }

  .modal-content {
    padding: 2rem;
  }
}
</style>
