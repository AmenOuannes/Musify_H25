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
  </div>

  <div v-else>
    <p>Loading artist...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getArtistByName } from '@/api/artistsAPI'

const route = useRoute()
const artist = ref(null)
const error = ref(null)

onMounted(async () => {
  try {
    const cleanedName = route.params.name.replace(/_/g, ' ').toLowerCase()
    console.log("Fetching:", cleanedName)

    const data = await getArtistByName(cleanedName)
    artist.value = data // 👈 FIXED HERE
  } catch (err) {
    error.value = 'Artist not found or error occurred.'
    console.error(err)
  }
})
</script>


<style scoped>
.artist-page {
  max-width: 600px;
  margin: 4rem auto;
  color: white;
  background-color: #111;
  padding: 2rem;
  border-radius: 12px;
  border: 1px solid #333;
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
</style>
