<template>
  <div class="artist-page" v-if="artist">
    <div class="artist-hero">
      <img :src="artist.image" alt="Artist Image" class="artist-hero-img" />
      <div class="artist-hero-info">
        <h1>{{ artist.artist_name }} <span v-if="artist.celebrity">⭐</span></h1>
        <p><strong>Genre:</strong> {{ artist.genre }}</p>
        <p><strong>Followers:</strong> {{ artist.followers.toLocaleString() }}</p>
        <div class="profile-link">
          <button class="green-btn" @click="visitProfile" :disabled="!artist?.profile_url">
            🔗 Visit Profile
          </button>
        </div>
        <div class="action-buttons">
          <button class="green-btn" @click="playArtist">
            <span class="icon">▶</span> Play
          </button>
          <button class="green-btn" @click="showAddSongModal = true">
            <span class="plus-icon">➕</span> Add Song
          </button>
          <button class="green-btn" @click="showAddAlbumModal = true">
            <span class="plus-icon">➕</span> Add Album
          </button>
          <button class="red-btn" @click="toggleLike">
            {{ isLiked ? '💔 Unlike' : '❤️ Like' }}
          </button>
        </div>
      </div>
    </div>

    <div class="media-lists">
      <div class="songs-section">
        <h2>Songs</h2>
        <div v-if="songs.length > 0">
          <SongDisplay
              v-for="song in songs"
              :key="song.song_name"
              :song="song"
              @click="goToSong(song.song_name)"
          />
        </div>
        <div v-else class="empty-message">No songs found for this artist.</div>
      </div>

      <div class="albums-section">
        <h2>Albums</h2>
        <div v-if="albums.length > 0">
          <AlbumDisplay
              v-for="album in albums"
              :key="album.album_name"
              :album="album"
              @click="goToAlbum(album.album_name)"
          />
        </div>
        <div v-else class="empty-message">No albums found for this artist.</div>
      </div>
    </div>

    <teleport to="body">
      <div v-if="showAddSongModal" class="modal-overlay" @click.self="showAddSongModal = false">
        <div class="modal-content">
          <AddSongs :prefilledArtist="artist.artist_name" @close="handleAddSongClose" />
        </div>
      </div>
    </teleport>

    <teleport to="body">
      <div v-if="showAddAlbumModal" class="modal-overlay" @click.self="showAddAlbumModal = false">
        <div class="modal-content">
          <AddAlbum :prefilledArtist="artist.artist_name" @close="handleAddAlbumClose" />
        </div>
      </div>
    </teleport>
  </div>

  <div v-else>
    <p>Loading artist...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex'
import {
  getArtistByName,
  getArtistsAlbums,
  getArtistsSongs,
  getLikedArtists,
  likeArtist,
  unlikeArtist
} from '@/api/artistsAPI'
import AddSongs from '@/Songs/AddSongs.vue'
import AddAlbum from '@/Albums/AddAlbums.vue'
import SongDisplay from '@/Songs/SongDisplay.vue'
import AlbumDisplay from '@/Albums/AlbumDisplay.vue'

const route = useRoute()
const router = useRouter()
const store = useStore()
const token = store.getters.currentToken

const artist = ref(null)
const songs = ref([])
const albums = ref([])
const isLiked = ref(false)
const showAddSongModal = ref(false)
const showAddAlbumModal = ref(false)

const goToSong = (name) => {
  const formatted = name.toLowerCase().replace(/\s+/g, '_')
  router.push({ name: 'SongDetail', params: { name: formatted } })
}

const goToAlbum = (name) => {
  const formatted = name.toLowerCase().replace(/\s+/g, '_')
  router.push({ name: 'AlbumDetail', params: { name: formatted } })
}

const handleAddAlbumClose = () => {
  showAddAlbumModal.value = false
  loadData()
}

const handleAddSongClose = () => {
  showAddSongModal.value = false
  loadData()
}

const checkIfLiked = async (artistName) => {
  try {
    const response = await getLikedArtists(artistName, token)
    const data = response.artists
    if (Array.isArray(data) && data.length > 0) {
      isLiked.value = true
    } else {
      isLiked.value = false
    }
  } catch (err) {
    console.error('Error checking if artist is liked:', err)
  }
}

const toggleLike = async () => {
  try {
    if (!artist.value || !artist.value.artist_name) return

    if (isLiked.value) {
      await unlikeArtist(artist.value.artist_name, token)
    } else {
      await likeArtist(artist.value.artist_name, token)
    }
    isLiked.value = !isLiked.value
  } catch (err) {
    console.error('Error toggling like:', err)
  }
}

const loadData = async () => {
  try {
    const cleanedName = route.params.name.replace(/_/g, ' ').toLowerCase()
    const artistData = await getArtistByName(cleanedName)
    artist.value = artistData

    await checkIfLiked(artistData.artist_name)

    const allSongsRes = await getArtistsSongs(artistData.artist_name)
    songs.value = allSongsRes.songs

    const allAlbumsRes = await getArtistsAlbums(artistData.artist_name)
    albums.value = allAlbumsRes.albums
  } catch (err) {
    console.error('Error loading artist data:', err)
  }
}

const visitProfile = () => {
  if (artist.value?.profile_url) {
    window.open(artist.value.profile_url, '_blank')
  } else {
    console.warn('No profile URL found for this artist.')
  }
}

const playArtist = () => {
  const formatted = artist.value.artist_name.toLowerCase().replace(/\s+/g, '_')
  router.push({ name: 'ArtistPlayer', params: { name: formatted } })
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.artist-page {
  padding: 2rem;
  color: #f0f0f0;
  background-color: #111;
  max-width: 1400px;
  margin: auto;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* ========== HERO ========== */
.artist-hero {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  align-items: center;
  margin-bottom: 3rem;
  background-color: #1a1a1a;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.4);
}

.artist-hero-img {
  width: 280px;
  height: 280px;
  object-fit: cover;
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.6);
}

.artist-hero-info {
  flex: 1;
  min-width: 250px;
}

.artist-hero-info h1 {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 0.8rem;
  color: #22c55e;
}

.artist-hero-info p {
  font-size: 1.1rem;
  margin-bottom: 0.6rem;
  line-height: 1.4;
}

/* ========== SHARED BUTTON STYLES ========== */
button {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.6rem 1.2rem;
  font-size: 0.95rem;
  font-weight: bold;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

/* Green buttons (play, add, visit profile) */
.green-btn {
  background-color: #22c55e;
  color: #111;
}
.green-btn:hover {
  background-color: #1ea347;
}

/* Red button (like/unlike) */
.red-btn {
  background-color: #e76f51;
  color: white;
}
.red-btn:hover {
  background-color: #d55a3c;
}

/* Icon color (for ➕) */
.plus-icon {
  color: #1ed760;
  font-size: 1.2rem;
}

/* ========== BUTTON CONTAINERS ========== */
.profile-link {
  margin-top: 0.5rem;
}
.profile-link button {
  width: fit-content;
}

.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

/* ========== MEDIA SECTIONS ========== */
.media-lists {
  display: flex;
  gap: 2rem;
  justify-content: space-between;
  align-items: flex-start;
}

.songs-section,
.albums-section {
  flex: 1;
  background-color: #1a1a1a;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.4);
}

.songs-section h2,
.albums-section h2 {
  font-size: 1.6rem;
  font-weight: 700;
  color: #22c55e;
  margin-bottom: 1rem;
  border-left: 4px solid #22c55e;
  padding-left: 0.75rem;
}

.empty-message {
  margin-top: 1rem;
  text-align: center;
  font-style: italic;
  color: #bbb;
}

/* ========== MODAL STYLES ========== */
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
}

/* ========== RESPONSIVE ========== */
@media (max-width: 900px) {
  .media-lists {
    flex-direction: column;
  }

  .songs-section,
  .albums-section {
    width: 100%;
  }

  .artist-hero {
    flex-direction: column;
    text-align: center;
  }

  .artist-hero-img {
    width: 200px;
    height: 200px;
  }
}

</style>