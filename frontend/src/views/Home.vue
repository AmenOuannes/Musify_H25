<template>
  <div class="home">
    <h1>Bienvenue, {{ user?.username || 'Utilisateur' }}</h1>
    <!-- Tu peux afficher d'autres infos de l'utilisateur ici -->
    <p>Ton email : {{ user?.email }}</p>
  </div>
</template>

<script setup>
import { useStore } from 'vuex'

const store = useStore()

const user = store.getters.currentUser
</script>

<style scoped>
.home {
  padding: 2rem;
  text-align: center;
}
</style>
