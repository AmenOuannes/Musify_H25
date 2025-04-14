<template>
  <div id="app">
    <Sidebar />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import Sidebar from "@/components/Sidebar.vue";
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  background-color: #111;
  color: white;
  font-family: 'Segoe UI', sans-serif;
}

#app {
  display: flex;
  min-height: 100vh;
  width: 100%;
}

.main-content {
  flex: 1;
  margin-left: 220px; /* ✅ Matches sidebar width */
  padding: 2rem;
  background-color: #111;
  box-sizing: border-box;
  min-height: 100vh;
}
</style>
