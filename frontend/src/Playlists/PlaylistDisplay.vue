<template>
  <div class="playlist-card">
    <div class="info" @click="$emit('click')">
      <h3 class="playlist-name">{{ playlist.playlist_name }}</h3>
      <div class="meta">
        <span>👤 {{ playlist.owner }}</span>
        <span v-if="playlist.private">🔒 Private</span>
      </div>
    </div>

    <div class="actions">
      <button class="action-btn view-btn" @click.stop="goToPlaylist">👁 View</button>
      <button class="action-btn play-btn" @click.stop="playPlaylist">▶ Play</button>
      <button
          v-if="showDelete"
          class="action-btn delete-btn"
          @click.stop="$emit('delete', playlist.playlist_name)"
      >
        🗑 Delete
      </button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  playlist: Object,
  showDelete: Boolean
})

const router = useRouter()

const goToPlaylist = () => {
  const formatted = props.playlist.playlist_name.toLowerCase().replace(/\s+/g, '_')
  router.push({ name: 'PlaylistDetail', params: { name: formatted } })
}

const playPlaylist = () => {
  const formatted = props.playlist.playlist_name.toLowerCase().replace(/\s+/g, '_')
  router.push({
    name: 'PlaylistPlayer',
    params: { name: formatted },
    query: { owner: props.playlist.owner.toLowerCase() }
  })
}
</script>

<style scoped>
.playlist-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #1e1e1e;
  border: 1px solid #2a2a2a;
  border-radius: 12px;
  padding: 1.2rem 1.5rem;
  color: white;
  gap: 2rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 4px 12px rgba(0, 255, 0, 0.05);
}

.playlist-card:hover {
  transform: scale(1.01);
  box-shadow: 0 8px 18px rgba(0, 255, 0, 0.08);
}

.info {
  flex: 1;
  cursor: pointer;
}

.playlist-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: #22c55e;
  margin-bottom: 0.5rem;
}

.meta {
  font-size: 0.95rem;
  color: #aaa;
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.actions {
  display: flex;
  flex-direction: row;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.action-btn {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  font-weight: bold;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.2s;
  white-space: nowrap;
}

.view-btn {
  background-color: #2dd4bf;
  color: #111;
}

.view-btn:hover {
  background-color: #1ac6ad;
}

.play-btn {
  background-color: #22c55e;
  color: #111;
}

.play-btn:hover {
  background-color: #1ea347;
}

.delete-btn {
  background-color: #ef4444;
  color: white;
}

.delete-btn:hover {
  background-color: #dc2626;
}

@media (max-width: 600px) {
  .playlist-card {
    flex-direction: column;
    align-items: flex-start;
  }

  .actions {
    width: 100%;
    justify-content: flex-start;
  }
}
</style>
