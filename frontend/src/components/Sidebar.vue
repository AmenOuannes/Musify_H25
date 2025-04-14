<template>
  <aside class="sidebar">
    <h1 class="logo" @click="goHome">Musify</h1>

    <nav class="menu-section">
      <ul class="menu">
        <li><router-link to="/artists">Artists</router-link></li>
        <li><router-link to="/albums">Albums</router-link></li>
        <li><router-link to="/songs">Songs</router-link></li>
        <li><router-link to="/playlists">Playlists</router-link></li>

        <li class="divider"></li>

        <li><router-link to="/myplaylists">My Playlists</router-link></li>
        <li><router-link to="/favorite/artists">My Favorite Artists</router-link></li>
        <li><router-link to="/favorite/playlists">My Favorite Playlists</router-link></li>
      </ul>
    </nav>

    <div class="login-wrapper">
      <div v-if="isLoggedIn" class="profile-button">
        <button @click.stop="toggleDropdown">Profile</button>
        <div v-if="isDropdownVisible" class="dropdown-menu" ref="dropdown">
          <ul>
            <li><router-link to="/settings">⚙ Settings</router-link></li>
            <li><a href="#" @click.prevent="logout">🚪 Logout</a></li>
          </ul>
        </div>
      </div>

      <router-link v-else to="/signin" class="login-button">Login</router-link>
    </div>
  </aside>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'Sidebar',
  data() {
    return {
      isDropdownVisible: false,
    }
  },
  computed: {
    ...mapGetters(['isLoggedIn']),
  },
  methods: {
    ...mapActions(['logout']),
    toggleDropdown() {
      this.isDropdownVisible = !this.isDropdownVisible
    },
    logout() {
      this.$store.dispatch('logout')
      this.$router.push('/signin')
    },
    handleClickOutside(event) {
      if (this.$refs.dropdown && !this.$refs.dropdown.contains(event.target)) {
        this.isDropdownVisible = false
      }
    },
    goHome() {
      this.$router.push('/home')
    },
  },
  mounted() {
    document.addEventListener('click', this.handleClickOutside)
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside)
  },
}
</script>

<style scoped>
.sidebar {
  width: 220px;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  background: #1a1a1a;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 1.5rem 1rem 2rem;
  box-shadow: 2px 0 10px rgba(0, 255, 0, 0.1);
  box-sizing: border-box;
  overflow: hidden;
}

.logo {
  color: #0f0;
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 1.5rem;
  cursor: pointer;
  text-align: left;
  padding-left: 5px;
}

.menu-section {
  flex-grow: 1;
  overflow-y: auto;
  padding-right: 4px;
  margin-bottom: 2rem;
}

.menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu li {
  margin-bottom: 12px;
}

.menu li a {
  text-decoration: none;
  color: #ccc;
  padding: 10px;
  display: block;
  font-size: 15px;
  border-radius: 8px;
  transition: background 0.3s ease, color 0.3s;
}

.menu li a:hover {
  background-color: #0f0;
  color: #111;
}

.divider {
  border-top: 1px solid #333;
  margin: 1rem 0;
}

.login-wrapper {
  margin-top: auto;
  text-align: center;
}

.login-button,
.profile-button button {
  width: 100%;
  padding: 10px 12px;
  font-size: 15px;
  font-weight: bold;
  color: black;
  background-color: #0f0;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-button:hover,
.profile-button button:hover {
  background-color: #0c0;
}

.profile-button {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  bottom: 45px;
  left: 0;
  width: 100%;
  background-color: #333;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 255, 0, 0.2);
  z-index: 1001;
}

.dropdown-menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.dropdown-menu ul li a {
  display: block;
  padding: 10px;
  color: white;
  font-size: 14px;
  text-decoration: none;
  transition: background-color 0.2s;
}

.dropdown-menu ul li a:hover {
  background-color: #0f0;
  color: #111;
}
</style>
