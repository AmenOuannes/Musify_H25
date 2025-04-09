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
    </div>

    <div class="playlist-list">
      <PlaylistDisplay
          v-for="playlist in playlists"
          :key="playlist.playlist_name"
          :playlist="playlist"
          @click="goToPlaylist(playlist.playlist_name)"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { getPlaylists } from '@/api/playlistAPI'
import PlaylistDisplay from '@/Playlists/PlaylistDisplay.vue'

const router = useRouter()
const playlists = ref([])
const searchQuery = ref('')

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

.playlist-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
