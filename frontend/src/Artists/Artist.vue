<template>
  <div class="artist-page" v-if="artist">
    <h1>{{ artist.artist_name }} <span v-if="artist.celebrity">⭐</span></h1>
    <img :src="artist.image" alt="Artist Image" class="artist-img" />
    <p><strong>Genre:</strong> {{ artist.genre }}</p>
    <p><strong>Followers:</strong> {{ artist.followers.toLocaleString() }}</p>
    <p>
      <strong>Profile:</strong>
      <a :href="artist.profile_url" target="_blank">{{ artist.profile_url }}</a>
    </p>

    <div class="action-buttons">
      <button class="add-song-btn" @click="showAddSongModal = true">➕ Add Song</button>
      <button class="add-album-btn" @click="showAddAlbumModal = true">➕ Add Album</button>
    </div>

    <div class="media-lists">
      <div class="songs-section" v-if="songs.length > 0">
        <h2>Songs</h2>
        <SongDisplay
            v-for="song in songs"
            :key="song.song_name"
            :song="song"
            @click="goToSong(song.song_name)"
        />
      </div>

      <div class="albums-section" v-if="albums.length > 0">
        <h2>Albums</h2>
        <AlbumDisplay
            v-for="album in albums"
            :key="album.album_name"
            :album="album"
            @click="goToAlbum(album.album_name)"
        />
      </div>
    </div>

    <div v-if="songs.length === 0 && albums.length === 0" class="empty-message">
      <p>No songs or albums found for this artist.</p>
    </div>

    <!-- MODALS -->
    <teleport to="body">
      <div v-if="showAddSongModal" class="modal-overlay" @click.self="showAddSongModal = false">
        <div class="modal-content">
          <AddSongs :prefilledArtist="artist.artist_name" @close="showAddSongModal = false" />
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
import { getArtistByName } from '@/api/artistsAPI'
import { getSongs } from '@/api/songAPI'
import { getAlbums } from '@/api/albumAPI'
import AddSongs from '@/Songs/AddSongs.vue'
import AddAlbum from '@/Albums/AddAlbums.vue'
import SongDisplay from '@/Songs/SongDisplay.vue'
import AlbumDisplay from '@/Albums/AlbumDisplay.vue'

const route = useRoute()
const router = useRouter()
const artist = ref(null)
const songs = ref([])
const albums = ref([])
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

const loadData = async () => {
  try {
    const cleanedName = route.params.name.replace(/_/g, ' ').toLowerCase()
    const artistData = await getArtistByName(cleanedName)
    artist.value = artistData

    const allSongs = await getSongs(100)
    songs.value = allSongs.songs.filter(song =>
        song.artist_name.toLowerCase() === artist.value.artist_name.toLowerCase()
    )

    const allAlbums = await getAlbums(100)
    albums.value = allAlbums.albums.filter(album =>
        album.artist_name.toLowerCase() === artist.value.artist_name.toLowerCase()
    )
  } catch (err) {
    console.error('Error loading artist data:', err)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.artist-page {
  padding: 2rem;
  color: white;
  background-color: #111;
  width: 100%;
}

.artist-img {
  width: 100%;
  max-height: 300px;
  object-fit: cover;
  border-radius: 10px;
  margin: 1rem 0;
}

h1 {
  font-size: 2rem;
  color: #2a9d8f;
  margin-bottom: 1rem;
}

p {
  margin-bottom: 0.8rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.add-song-btn,
.add-album-btn {
  background-color: #2a9d8f;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}

.media-lists {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  margin-top: 2.5rem;
}

.songs-section,
.albums-section {
  flex: 1 1 45%;
  min-width: 300px;
}

.songs-section h2,
.albums-section h2 {
  margin-bottom: 1rem;
  font-size: 1.4rem;
  color: #2a9d8f;
}

.songs-section > *,
.albums-section > * {
  margin-bottom: 1rem;
}

.empty-message {
  margin-top: 2rem;
  color: #bbb;
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
