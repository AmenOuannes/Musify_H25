<template>
  <div class="playlist-page" v-if="playlist">
    <div class="playlist-header">
      <h1>{{ playlist.playlist_name }}</h1>
      <p class="meta">By {{ playlist.owner }} <span v-if="playlist.private">• Private</span></p>
      <div class="action-buttons">
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

    <div class="songs-list" v-if="songs.length > 0">
      <h2>Songs</h2>
      <SongDisplay
          v-for="song in songs"
          :key="song.song_name"
          :song="song"
          @click="goToSong(song.song_name)"
          v-bind="playlist.owner === username ? { onRemove: () => confirmRemove(song.song_name) } : {}"
      />
    </div>

    <div v-else>
      <p>No songs in this playlist yet.</p>
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

  <div v-else>
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
  deleteSongFromPlaylist
} from '@/api/playlistAPI'
import {
  getLikedPlaylists,
  likePlaylist,
  unlikePlaylist
} from '@/api/playlistAPI.js'
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
  color: white;
  background-color: #111;
}

.playlist-header {
  margin-bottom: 2rem;
}

.playlist-header h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: #2a9d8f;
}

.playlist-header .meta {
  font-size: 1.1rem;
  color: #ccc;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.add-song-btn {
  padding: 8px 16px;
  background-color: #2a9d8f;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-weight: bold;
}

.like-btn {
  padding: 8px 16px;
  background-color: #e76f51;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-weight: bold;
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
