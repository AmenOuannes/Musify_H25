<template>
  <div class="album-page" v-if="album">
    <div class="album-hero">
      <img :src="album.image" alt="Album Cover" class="album-hero-img" />
      <div class="album-hero-info">
        <h1>{{ album.album_name }}</h1>
        <p><strong>Artist:</strong> {{ album.artist_name }}</p>
        <p><strong>Genre:</strong> {{ album.genre }}</p>
        <p><strong>Release:</strong> {{ formatDate(album.release_date) }}</p>
        <div class="action-buttons">
          <button class="play-btn" @click="playAlbum">
            ▶ Play
          </button>
          <button class="add-song-btn" @click="showAddSongModal = true">
            <span class="plus-icon">➕</span> Add Song
          </button>
        </div>
      </div>
    </div>

    <div class="songs-section">
      <h2>Songs</h2>
      <div v-if="songs.length > 0" class="songs-list">
        <SongDisplay
            v-for="song in songs"
            :key="song.song_name"
            :song="song"
            @click="goToSong(song.song_name)"
            :onRemove="() => confirmRemove(song.song_name)"
        />
      </div>
      <div v-else class="empty-message">No songs in this album yet.</div>
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
    songs.value = songsData.songs
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

const playAlbum = () => {
  const formatted = album.value.album_name.toLowerCase().replace(/\s+/g, '_')
  router.push({
    name: 'AlbumPlayer',
    params: { name: formatted }
  })
}

onMounted(async () => {
  try {
    const cleaned = route.params.name.replace(/_/g, ' ').toLowerCase()
    const albumData = await getAlbumByName(cleaned)
    album.value = {
      ...albumData,
      image: albumData.cover_image || albumData.image || ''
    }
    await refreshSongs()
  } catch (err) {
    console.error('Failed to load album:', err)
  }
})
</script>

<style scoped>
.album-page {
  padding: 2rem;
  color: #f0f0f0;
  background-color: #111;
  max-width: 1400px;
  margin: auto;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.album-hero {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  align-items: center;
  margin-bottom: 3rem;
  background-color: #1a1a1a; /* unified with song section */
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.4);
}

.album-hero-img {
  width: 240px;
  height: 240px;
  object-fit: cover;
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.6);
}

.album-hero-info {
  flex: 1;
  min-width: 250px;
}

.album-hero-info h1 {
  font-size: 2.4rem;
  font-weight: 800;
  margin-bottom: 0.8rem;
  color: #22c55e; /* match Songs section heading color */
}

.album-hero-info p {
  font-size: 1.05rem;
  margin-bottom: 0.4rem;
  line-height: 1.5;
}

.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.add-song-btn {
  background-color: #22c55e;
  color: #111;
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-song-btn:hover {
  background-color: #1ea347;
}

.play-btn {
  background-color: #22c55e;
  color: #111;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 20px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
}

.play-btn:hover {
  background-color: #1ea347;
}

.songs-section {
  background-color: #1a1a1a;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.4);
}

.songs-section h2 {
  font-size: 1.6rem;
  font-weight: 700;
  color: #22c55e;
  margin-bottom: 1.5rem;
  border-left: 4px solid #22c55e;
  padding-left: 0.75rem;
}

.songs-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.empty-message {
  text-align: center;
  color: #aaa;
  font-style: italic;
  font-size: 1rem;
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
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.8);
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

@media (max-width: 900px) {
  .album-hero {
    flex-direction: column;
    text-align: center;
  }

  .album-hero-img {
    width: 200px;
    height: 200px;
  }

  .songs-section {
    padding: 1.5rem;
  }
}

.plus-icon {
  color: #1ed760; /* Spotify green pop */
  margin-right: 0.4rem;
  font-size: 1.2rem;
}
</style>
