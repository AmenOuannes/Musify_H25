<template>
  <div class="playlist-card">
    <div class="info" @click="$emit('click')">
      <h3>{{ playlist.playlist_name }}</h3>
      <p>👤 {{ playlist.owner }}</p>
      <p v-if="playlist.private">🔒 Private</p>
    </div>
    <div class="actions">
      <button @click.stop="goToPlaylist">View</button>
      <button @click.stop="playPlaylist">▶ Play</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const props = defineProps({ playlist: Object })
const router = useRouter()

const goToPlaylist = () => {
  const formatted = props.playlist.playlist_name.toLowerCase().replace(/\s+/g, '_')
  router.push({ name: 'PlaylistDetail', params: { name: formatted } })
}

const playPlaylist = () => {
  const formatted = props.playlist.playlist_name.toLowerCase().replace(/\s+/g, '_')
  router.push({ name: 'PlaylistPlayer', params: { name: formatted } })
}
</script>

<style scoped>
.playlist-card {
  background-color: #1e1e1e;
  border: 1px solid #444;
  border-radius: 10px;
  padding: 1rem;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info {
  flex-grow: 1;
  cursor: pointer;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

button {
  padding: 5px 10px;
  background-color: #2a9d8f;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}
</style>
