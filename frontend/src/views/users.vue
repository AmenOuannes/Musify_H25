<template>
  <div class="p-4">
    <h1 class="text-xl font-bold mb-4">Liste des utilisateurs</h1>
    <ul>
      <li v-for="user in users" :key="user.id" class="mb-2">
        {{ user.id }} - {{ user.name }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const users = ref([])

onMounted(async () => {
  try {
    const res = await axios.get('http://127.0.0.1:5000/users')
    users.value = res.data.users
  } catch (err) {
    console.error('Erreur lors de la récupération des utilisateurs :', err)
  }
})
</script>

<style>
body {
  font-family: Arial, sans-serif;
}
</style>
