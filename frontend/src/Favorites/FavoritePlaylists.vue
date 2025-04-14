<template>
  <div class="playlist-search">
    <div class="search-container">
      <div class="search-bar">
        <input
            v-model="searchQuery"
            type="text"
            placeholder="Search your favorite playlists..."
        />
      </div>
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

.playlist-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2rem;
  padding: 1rem;
}
</style>
