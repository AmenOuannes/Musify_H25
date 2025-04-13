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
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  background-color: #111;
  color: white;
}

#app {
  display: flex;
  min-height: 100vh;
}

.main-content {
  margin-left: 120px;
  margin-top: 60px;
  flex-grow: 1;
  padding: 20px;
  background-color: #111;
  color: white;
  min-height: 100vh;
  box-sizing: border-box;
}
</style>