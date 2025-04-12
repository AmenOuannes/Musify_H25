<template>
  <div class="playlist-search">
    <div class="search-container">
      <input
          v-model="searchQuery"
          type="text"
          placeholder="Search your favorite playlists..."
          class="search-input"
      />
    </div>

    <div class="playlist-list">
      <PlaylistDisplay
          v-for="playlist in playlists"
          :key="playlist.playlist_name"
          :playlist="playlist"
          @click="goToPlaylist(playlist.playlist_name, playlist.owner)"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import PlaylistDisplay from '@/Playlists/PlaylistDisplay.vue'
import { getLikedPlaylists } from '@/api/playlistAPI.js'

const router = useRouter()
const store = useStore()

const playlists = ref([])
const searchQuery = ref('')
const token = store.getters.currentToken

const fetchLikedPlaylists = async () => {
  try {
    const data = await getLikedPlaylists(searchQuery.value, token)
    playlists.value = Array.isArray(data) ? data : data?.playlists || []
  } catch (err) {
    console.error('Error fetching liked playlists:', err)
    playlists.value = []
  }
}

const goToPlaylist = (name, owner) => {
  const formattedName = name.toLowerCase().replace(/\s+/g, '_')
  router.push({ name: 'Playlist', params: { name: formattedName, owner } })
}

onMounted(fetchLikedPlaylists)
watch(searchQuery, fetchLikedPlaylists)
</script>

<style scoped>
.playlist-search {
  padding: 2rem;
  color: white;
  background-color: #111;
}

.search-container {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 2rem;
}

.search-input {
  padding: 10px 15px;
  border-radius: 20px;
  border: 1px solid #888;
  background-color: #222;
  color: white;
  width: 250px;
}

.playlist-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
