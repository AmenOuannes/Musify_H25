<template>
  <div class="playlist-page" v-if="playlist">
    <div class="playlist-hero">
      <div class="playlist-hero-info">
        <h1>{{ playlist.playlist_name }}</h1>
        <p class="meta">
          👤 {{ playlist.owner }}
          <span v-if="playlist.private">• 🔒 Private</span>
        </p>
        <div class="action-buttons">

          <button class="play-btn" @click="playPlaylist">
            ▶ Play
          </button>

          <button
              v-if="playlist.owner === username"
              @click="showAddSongModal = true"
              class="add-song-btn"
          >
            ➕ Add Song
          </button>

          <button class="like-btn" @click="toggleLike">
            {{ isLiked ? '💔 Unlike' : '❤️ Like' }}
          </button>
        </div>
      </div>

      <div class="playlist-hero-right">
        <div class="summary-card">
          <h3>Songs</h3>
          <p>{{ songs.length }}</p>
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
            v-bind="playlist.owner === username ? { onRemove: () => confirmRemove(song.song_name) } : {}"
        />
      </div>
      <div v-else class="empty-message">No songs in this playlist yet.</div>
    </div>

    <teleport to="body">
      <div
          v-if="showAddSongModal && playlist.owner === username"
          class="modal-overlay"
          @click.self="showAddSongModal = false"
      >
        <div class="modal-content">
          <AddSongToPlaylist
              :playlistName="playlist.playlist_name"
              @close="handleAddSongClose"
              @song-added="refreshSongs"
          />
        </div>
      </div>

      <div v-if="confirmPopup" class="modal-overlay" @click.self="confirmPopup = false">
        <div class="modal-content">
          <h3>Confirm Removal</h3>
          <p>Are you sure you want to remove "{{ songToRemove }}" from the playlist?</p>
          <div class="popup-actions">
            <button @click="performRemove" class="confirm-btn">Yes</button>
            <button @click="confirmPopup = false" class="cancel-btn">Cancel</button>
          </div>
        </div>
      </div>
    </teleport>
  </div>

  <div v-else class="loading">
    <p>Loading playlist...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex'
import {
  getPlaylistByName,
  getPlaylistSongs,
  deleteSongFromPlaylist,
  getLikedPlaylists,
  likePlaylist,
  unlikePlaylist
} from '@/api/playlistAPI'
import SongDisplay from '@/Songs/SongDisplay.vue'
import AddSongToPlaylist from '@/MyPlaylists/AddSongsToPlaylist.vue'

const route = useRoute()
const router = useRouter()
const store = useStore()

const token = store.getters.currentToken
const username = store.getters.currentUser.username

const playlist = ref(null)
const songs = ref([])
const showAddSongModal = ref(false)
const confirmPopup = ref(false)
const songToRemove = ref(null)
const isLiked = ref(false)

const goToSong = (name) => {
  const formatted = name.toLowerCase().replace(/\s+/g, '_')
  router.push({ name: 'SongDetail', params: { name: formatted } })
}

const playPlaylist = () => {
  const formatted = playlist.value.playlist_name.toLowerCase().replace(/\s+/g, '_')
  router.push({
    name: 'PlaylistPlayer',
    params: { name: formatted },
    query: { owner: playlist.value.owner.toLowerCase() }
  })
}

const refreshSongs = async () => {
  try {
    const cleanedName = route.params.name.replace(/_/g, ' ').toLowerCase()
    const result = await getPlaylistSongs(cleanedName, playlist.value.owner)
    songs.value = result.songs || []
  } catch (err) {
    console.error('Failed to fetch songs from playlist:', err)
  }
}

const confirmRemove = (name) => {
  songToRemove.value = name
  confirmPopup.value = true
}

const performRemove = async () => {
  try {
    await deleteSongFromPlaylist(playlist.value.playlist_name, songToRemove.value, token)
    confirmPopup.value = false
    await refreshSongs()
  } catch (err) {
    console.error('Failed to remove song:', err)
  }
}

const handleAddSongClose = () => {
  showAddSongModal.value = false
  refreshSongs()
}

const checkIfLiked = async (playlistName) => {
  try {
    const response = await getLikedPlaylists(playlistName, token)
    const data = response.playlists
    isLiked.value = Array.isArray(data) && data.length > 0
  } catch (err) {
    console.error('Error checking if playlist is liked:', err)
  }
}

const toggleLike = async () => {
  try {
    if (!playlist.value || !playlist.value.playlist_name) return

    if (isLiked.value) {
      await unlikePlaylist(playlist.value.playlist_name, token)
    } else {
      await likePlaylist(playlist.value.playlist_name, token)
    }
    isLiked.value = !isLiked.value
  } catch (err) {
    console.error('Error toggling playlist like:', err)
  }
}

onMounted(async () => {
  try {
    const cleaned = route.params.name.replace(/_/g, ' ').toLowerCase()
    const data = await getPlaylistByName(cleaned)
    playlist.value = data

    await checkIfLiked(data.playlist_name)
    await refreshSongs()
  } catch (err) {
    console.error('Failed to load playlist:', err)
  }
})
</script>

<style scoped>
.playlist-page {
  padding: 2rem;
  color: #f0f0f0;
  background-color: #111;
  max-width: 1400px;
  margin: auto;
}

.playlist-hero {
  display: flex;
  justify-content: space-between;
  gap: 2rem;
  align-items: center;
  background-color: #1a1a1a;
  padding: 2rem;
  border-radius: 20px;
  margin-bottom: 3rem;
  flex-wrap: wrap;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
}

.playlist-hero-info {
  flex: 1;
  min-width: 260px;
}

.playlist-hero-info h1 {
  font-size: 2.4rem;
  font-weight: 800;
  margin-bottom: 0.6rem;
  color: #22c55e;
}

.meta {
  font-size: 1rem;
  color: #ccc;
  margin-bottom: 1.2rem;
}

.action-buttons {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}

.add-song-btn {
  background-color: #1ed760;
  color: #111;
  border: none;
  padding: 0.6rem 1.2rem;
  font-weight: bold;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-song-btn:hover {
  background-color: #1db954;
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

.like-btn {
  background-color: #ef4444;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 20px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
}

.like-btn:hover {
  background-color: #dc2626;
}

.playlist-hero-right {
  min-width: 200px;
}

.summary-card {
  background-color: #222;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  text-align: center;
  color: white;
  box-shadow: 0 4px 16px rgba(0, 255, 100, 0.1);
}

.summary-card h3 {
  margin: 0;
  font-size: 1rem;
  color: #aaa;
}

.summary-card p {
  margin: 0.4rem 0 0 0;
  font-size: 1.6rem;
  font-weight: bold;
  color: #0f0;
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
  color: #bbb;
  font-style: italic;
  margin-top: 1rem;
}

/* Modals */
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
  .playlist-hero {
    flex-direction: column;
    text-align: center;
  }

  .playlist-hero-right {
    width: 100%;
  }

  .action-buttons {
    justify-content: center;
  }
}
</style>
