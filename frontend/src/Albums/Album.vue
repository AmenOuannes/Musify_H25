<template>
  <div class="album-page" v-if="album">
    <div class="album-header">
      <img :src="album.image" alt="Album cover" class="album-cover" />
      <div class="album-details">
        <h1>{{ album.album_name }}</h1>
        <p class="artist">By {{ album.artist_name }}</p>
        <p class="meta">
          {{ album.genre }} • {{ formatDate(album.release_date) }}
        </p>
        <button @click="showAddSongModal = true" class="add-song-btn">
          Add Song to Album
        </button>
      </div>
    </div>

    <div class="songs-list" v-if="songs.length > 0">
      <h2>Songs</h2>
      <SongDisplay
          v-for="song in songs"
          :key="song.song_name"
          :song="song"
          @click="goToSong(song.song_name)"
          :onRemove="() => confirmRemove(song.song_name)"
      />
    </div>

    <div v-else>
      <p>No songs in this album yet.</p>
    </div>

    <teleport to="body">
      <div v-if="showAddSongModal" class="modal-overlay" @click.self="showAddSongModal = false">
        <div class="modal-content">
          <AddSongToAlbum
              :albumName="album.album_name"
              :artistName="album.artist_name"
              @close="handleAddSongClose"
              @song-added="refreshSongs"
          />
        </div>
      </div>

      <div v-if="confirmPopup" class="modal-overlay" @click.self="confirmPopup = false">
        <div class="modal-content">
          <h3>Confirm Removal</h3>
          <p>Are you sure you want to remove "{{ songToRemove }}" from the album?</p>
          <div class="popup-actions">
            <button @click="performRemove" class="confirm-btn">Yes</button>
            <button @click="confirmPopup = false" class="cancel-btn">Cancel</button>
          </div>
        </div>
      </div>
    </teleport>
  </div>

  <div v-else>
    <p>Loading album...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getAlbumByName, getAlbumSongs, deleteSongFromAlbum } from '@/api/albumAPI'
import AddSongToAlbum from '@/Albums/AddSongToAlbum.vue'
import SongDisplay from '@/Songs/SongDisplay.vue'
import { useStore } from 'vuex'

const route = useRoute()
const router = useRouter()
const store = useStore()
const album = ref(null)
const songs = ref([])
const showAddSongModal = ref(false)
const confirmPopup = ref(false)
const songToRemove = ref(null)
const token = store.getters.currentToken

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

const goToSong = (name) => {
  const formatted = name.toLowerCase().replace(/\s+/g, '_')
  router.push({ name: 'SongDetail', params: { name: formatted } })
}

const refreshSongs = async () => {
  try {
    const cleaned = route.params.name.replace(/_/g, ' ').toLowerCase()
    const songsData = await getAlbumSongs(cleaned)
    songs.value = songsData.songs || []
  } catch (err) {
    console.error('Failed to refresh songs:', err)
  }
}

const confirmRemove = (name) => {
  songToRemove.value = name
  confirmPopup.value = true
}

const performRemove = async () => {
  try {
    await deleteSongFromAlbum(album.value.album_name, songToRemove.value, token)
    confirmPopup.value = false
    await refreshSongs()
  } catch (err) {
    console.error(err.message)
  }
}

const handleAddSongClose = () => {
  showAddSongModal.value = false
}

onMounted(async () => {
  try {
    const cleaned = route.params.name.replace(/_/g, ' ').toLowerCase()
    const albumData = await getAlbumByName(cleaned)
    album.value = albumData
    await refreshSongs()
  } catch (err) {
    console.error('Failed to load album:', err)
  }
})
</script>

<style scoped>
.album-page {
  padding: 2rem;
  color: white;
  background-color: #111;
}

.album-header {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
  align-items: center;
}

.album-cover {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 10px;
}

.album-details h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: #2a9d8f;
}

.album-details .artist {
  font-size: 1.2rem;
  margin-bottom: 0.3rem;
  color: #ddd;
}

.album-details .meta {
  font-size: 0.95rem;
  color: #aaa;
}

.add-song-btn {
  padding: 8px 16px;
  background-color: #2a9d8f;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-weight: bold;
  margin-top: 1rem;
}

.songs-list {
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
