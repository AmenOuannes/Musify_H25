<template>
  <aside class="sidebar">
    <h1 class="logo" @click="goHome">Musify</h1>
    <nav>
      <ul class="menu">
        <li><router-link to="/artists">Artists</router-link></li>
        <li><router-link to="/albums">Albums</router-link></li>
        <li><router-link to="/songs">Songs</router-link></li>
        <li><router-link to="/playlists">Playlists</router-link></li>
        <li><router-link to="/myplaylists">My Playlists</router-link></li>
        <li><router-link to="/favorite/artists">My Favorites artist</router-link></li>
        <li><router-link to="/favorite/playlists">My Favorites Playlists</router-link></li>

      </ul>
    </nav>
  </aside>
</template>

<script>
export default {
  methods: {
    goHome() {
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
.sidebar {
  width: 100px;
  background: #222;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  display: flex;
  flex-direction: column;
  padding: 10px;
}

.sidebar .logo {
  color: #0f0;
  font-size: 28px;
  text-align: left;
  margin: 10px 0 20px 10px;
  cursor: pointer;
  line-height: 40px;
}

.sidebar .menu {
  list-style: none;
  padding: 0;
  width: 100%;
  margin-top: 0;
}

.sidebar .menu li,
.playlist-list li {
  margin-bottom: 15px;
  text-align: left;
}

.sidebar .menu li a,
.playlist-list li a {
  text-decoration: none;
  color: white;
  padding: 8px;
  display: block;
  font-size: 14px;
  border-radius: 5px;
  transition: background 0.3s ease, color 0.3s;
}

.sidebar .menu li a:hover,
.playlist-list li a:hover {
  background: #0f0;
  color: black;
}

.sidebar-divider {
  width: 100%;
  height: 2px;
  background-color: #0f0;
  margin: 15px 0;
  border: none;
}

.recents-title {
  font-size: 14px;
  color: #0f0;
  margin-bottom: 10px;
  text-transform: uppercase;
  text-align: left;
}

.playlist-list {
  list-style: none;
  padding: 0;
  width: 100%;
}
</style>