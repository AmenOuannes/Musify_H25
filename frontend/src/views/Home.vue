<template>
  <div class="home-wrapper">
    <div class="center-container">
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
/* Main container with left padding to shift content right */
.home-wrapper {
  width: 100%;
  height: 100%;
  min-height: calc(100vh - 60px);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

/* Center container for vertical alignment */
.center-container {
  width: 100%;
  max-width: 900px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Welcome section */
.welcome-banner {
  text-align: center;
  margin-bottom: 3rem;
  width: 100%;
  animation: fadeInDown 1s ease-out;
}

.welcome-banner h1 {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  background: linear-gradient(90deg, #2a9d8f, #e9c46a);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.subtitle {
  font-size: 1.4rem;
  color: #e0e0e0;
  font-weight: 300;
  letter-spacing: 0.5px;
}

/* Columns layout */
.columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  width: 90%;
}

.left-column,
.right-column {
  background: rgba(26, 26, 26, 0.8);
  padding: 2.5rem;
  border-radius: 24px;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(10px);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.left-column:hover,
.right-column:hover {
  transform: translateY(-8px);
  box-shadow: 0 18px 36px rgba(0, 0, 0, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.left-column h2,
.right-column h2 {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 1.8rem;
  color: #ffffff;
  border-left: 5px solid #2a9d8f;
  padding-left: 1rem;
  display: flex;
  align-items: center;
}

/* Animations */
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive design */
@media (max-width: 900px) {
  .columns {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .welcome-banner h1 {
    font-size: 2.5rem;
  }

  .subtitle {
    font-size: 1.2rem;
  }

  .left-column,
  .right-column {
    padding: 1.8rem;
  }
}
</style>