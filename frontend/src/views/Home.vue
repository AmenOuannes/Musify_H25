<template>
  <div class="home">
    <div class="welcome-banner">
      <h1>Welcome back, {{ user?.first_name || 'there' }} 👋</h1>
      <p class="subtitle">Ready to dive back into your musical universe?</p>
    </div>

    <div class="columns">
      <div class="left-column">
        <h2>📀 Your Favorite Playlists</h2>
        <PlaylistDisplay
            v-for="playlist in playlists"
            :key="playlist.playlist_name"
            :playlist="playlist"
            @click="goToPlaylist(playlist.playlist_name)"
        />
      </div>

      <div class="right-column">
        <h2>🎤 Your Favorite Artists</h2>
        <ArtistDisplay
            v-for="artist in artists"
            :key="artist.artist_name"
            :artist="artist"
            @click="goToArtist(artist.artist_name)"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { getLikedArtists } from '@/api/artistsAPI'
import { getLikedPlaylists } from '@/api/playlistAPI'
import ArtistDisplay from '@/Artists/ArtistDisplay.vue'
import PlaylistDisplay from '@/Playlists/PlaylistDisplay.vue'

const store = useStore()
const router = useRouter()

const user = store.getters.currentUser
const token = store.getters.currentToken

const artists = ref([])
const playlists = ref([])

const fetchLikedArtists = async () => {
  try {
    const data = await getLikedArtists("", token)
    artists.value = Array.isArray(data) ? data : data?.artists || []
  } catch (err) {
    console.error("Failed to fetch liked artists:", err)
  }
}

const fetchLikedPlaylists = async () => {
  try {
    const data = await getLikedPlaylists("", token)
    playlists.value = Array.isArray(data) ? data : data?.playlists || []
  } catch (err) {
    console.error("Failed to fetch liked playlists:", err)
  }
}

const goToArtist = (name) => {
  const formattedName = name.toLowerCase().replace(/\s+/g, '_')
  router.push({ name: 'ArtistDetail', params: { name: formattedName } })
}

const goToPlaylist = (name) => {
  const formatted = name.toLowerCase().replace(/\s+/g, '_')
  router.push({ name: 'PlaylistDetail', params: { name: formatted } })
}

onMounted(() => {
  fetchLikedArtists()
  fetchLikedPlaylists()
})
</script>

<style scoped>
.home {
  padding: 2rem;
  color: white;
  background-color: #111;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.welcome-banner {
  text-align: center;
  margin-bottom: 2rem;
  animation: fadeIn 1s ease-out;
}

.welcome-banner h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.25rem;
  color: #aaa;
}

.columns {
  display: flex;
  justify-content: space-between;
  gap: 2rem;
}

.left-column,
.right-column {
  flex: 1;
  background-color: #1a1a1a;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease;
}

.left-column:hover,
.right-column:hover {
  transform: translateY(-5px);
}

.left-column h2,
.right-column h2 {
  margin-bottom: 1rem;
  font-size: 1.4rem;
  border-bottom: 1px solid #333;
  padding-bottom: 0.5rem;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
