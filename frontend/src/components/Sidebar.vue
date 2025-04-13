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

    <!-- 🔥 Login / Profile + dropdown -->
    <div class="login-wrapper">
      <div v-if="isLoggedIn" class="profile-button">
        <button @click.stop="toggleDropdown">Profile</button>
        <div v-if="isDropdownVisible" class="dropdown-menu" ref="dropdown">
          <ul>
            <li><router-link to="/settings"> Settings</router-link></li>
            <li><a href="#" @click.prevent="logout"> Logout</a></li>
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
      this.$router.push('/')
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
  width: 100px;
  background: #222;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  display: flex;
  flex-direction: column;
  padding: 10px;
  justify-content: space-between;
}

.logo {
  color: #0f0;
  font-size: 28px;
  text-align: left;
  margin: 10px 0 20px 10px;
  cursor: pointer;
  line-height: 40px;
}

.menu {
  list-style: none;
  padding: 0;
  margin: 0;
  flex-grow: 1;
}

.menu li {
  margin-bottom: 15px;
  text-align: left;
}

.menu li a {
  text-decoration: none;
  color: white;
  padding: 8px;
  display: block;
  font-size: 14px;
  border-radius: 5px;
  transition: background 0.3s ease, color 0.3s;
}

.menu li a:hover {
  background: #0f0;
  color: black;
}

.login-wrapper {
  margin-top: auto;
  padding: 10px;
  text-align: center;
}

.login-button,
.profile-button button {
  background-color: #0f0;
  color: black;
  border: none;
  padding: 8px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  width: 100%;
  transition: background-color 0.3s ease;
  text-decoration: none;
}

.login-button:hover,
.profile-button button:hover {
  background-color: #0c0;
}

.profile-button {
  position: relative;
}

/* Dropdown style */
.dropdown-menu {
  position: absolute;
  bottom: 45px;
  left: 0;
  width: 100%;
  background-color: #444;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 255, 0, 0.2);
  z-index: 1001;
}

.dropdown-menu ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.dropdown-menu ul li a {
  display: block;
  padding: 10px;
  color: white;
  font-size: 14px;
  text-decoration: none;
}

.dropdown-menu ul li a:hover {
  background-color: #0f0;
  color: black;
}
</style>
