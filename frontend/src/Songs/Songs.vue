<template>
  <div class="song-search">
    <div class="search-container">
      <div class="search-bar">
        <input
            type="text"
            v-model="searchQuery"
            placeholder="Search for a song..."
            @input="handleInput"
            @blur="hideDropdown"
        />
      </div>
      <div class="add-song">
        <button @click="showAddModal = true">Add Song</button>
      </div>
    </div>

    <div class="song-list">
      <!-- Use SongDisplay instead of raw HTML cards -->
      <SongDisplay
          v-for="song in displayedSongs"
          :key="song.song_name"
          :song="song"
          @click="goToSong(song.song_name)"
      />
    </div>

    <!-- MODAL -->
    <teleport to="body">
      <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
        <div class="modal-content">
          <AddSong @close="handleModalClose" />
        </div>
      </div>
    </teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getSongs } from '@/api/songAPI'
import AddSong from '@/Songs/AddSongs.vue'
import SongDisplay from '@/Songs/SongDisplay.vue' // ✅ import the new component

const router = useRouter()
const songs = ref([])
const searchQuery = ref('')
const showAddModal = ref(false)
const showDropdown = ref(false)

const displayedSongs = computed(() => {
  if (!searchQuery.value) return songs.value
  return songs.value.filter(song =>
      song.song_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      song.artist_name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const fetchSongs = async () => {
  try {
    const data = await getSongs(50)
    songs.value = data.songs || []
  } catch (err) {
    console.error('Error fetching songs:', err)
    songs.value = []
  }
}

const handleInput = () => {
  showDropdown.value = searchQuery.value.length > 0
}

const hideDropdown = () => {
  setTimeout(() => {
    showDropdown.value = false
  }, 200)
}

const goToSong = (name) => {
  const formatted = name.toLowerCase().replace(/\s+/g, '_')
  router.push({ name: 'SongDetail', params: { name: formatted } })
}

const handleModalClose = () => {
  showAddModal.value = false
  fetchSongs()
}

onMounted(() => {
  fetchSongs()
})
</script>

<style scoped>
.song-search {
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

.add-song button {
  padding: 10px 15px;
  border-radius: 20px;
  background-color: #2a9d8f;
  color: white;
  border: none;
  font-weight: bold;
  cursor: pointer;
}

.song-list {
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
}
</style>
