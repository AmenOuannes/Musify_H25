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
      <div
          class="song-item"
          v-for="song in songs"
          :key="song.song_name"
          @click="goToSong(song.song_name)"
      >
        <span class="song-name">{{ song.song_name }}</span>
        <span class="song-duration">{{ song.duration || '--:--' }}</span>
      </div>
    </div>

    <div v-else>
      <p>No songs in this album yet.</p>
    </div>

    <teleport to="body">
      <div v-if="showAddSongModal" class="modal-overlay" @click.self="showAddSongModal = false">
        <div class="modal-content">
          <AddSongToAlbum
              :albumName="album.album_name"
              @close="handleAddSongClose"
              @song-added="refreshSongs"
          />
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
import { getAlbumByName, getAlbumSongs } from '@/api/albumAPI'
import AddSongToAlbum from '@/Albums/AddSongToAlbum.vue'

const route = useRoute()
const router = useRouter()
const album = ref(null)
const songs = ref([])
const showAddSongModal = ref(false)

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
/* Previous styles remain the same */
.add-song-btn {
  padding: 8px 16px;
  background-color: #2a9d8f;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
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