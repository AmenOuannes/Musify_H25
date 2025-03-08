<template>
  <div id="app">
    <Sidebar />
    <TopBar />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import Sidebar from "@/components/Sidebar.vue";
import TopBar from "@/components/TopBar.vue";
</script>

<style>
/* Global styles to remove default margins and padding */
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  background-color: #111; /* Match the background color */
  color: white; /* Default text color */
}

#app {
  display: flex;
  min-height: 100vh;
}

.main-content {
  margin-left: 120px; /* Matches the sidebar width + buffer */
  margin-top: 60px; /* Matches the top bar height */
  flex-grow: 1;
  padding: 20px;
  background-color: #111;
  color: white;
  min-height: 100vh;
  box-sizing: border-box; /* Ensures padding is included in the width */
}
</style>