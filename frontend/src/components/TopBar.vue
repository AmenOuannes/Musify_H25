<template>
  <div class="top-bar">
    <div class="search-bar">
      <input type="text" placeholder="Search..." />
    </div>
    <div class="auth-buttons">
      <div v-if="isLoggedIn" class="profile-button">
        <button @click.stop="toggleDropdown">Profile</button>
        <div v-if="isDropdownVisible" class="dropdown-menu" ref="dropdown">
          <ul>
            <li><router-link to="/settings">Settings</router-link></li>
            <li><a href="#" @click="logout">Logout</a></li>
          </ul>
        </div>
      </div>
      <router-link v-else to="/signin" class="login-button">Login</router-link>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "TopBar",
  data() {
    return {
      isDropdownVisible: false,
    };
  },
  computed: {
    ...mapGetters(["isLoggedIn"]),
  },
  methods: {
    ...mapActions(["logout"]),
    toggleDropdown() {
      this.isDropdownVisible = !this.isDropdownVisible;
    },
    async logout() {
      await this.$store.dispatch("logout");
      this.$router.push("/signin");
    },
    handleClickOutside(event) {
      if (this.$refs.dropdown && !this.$refs.dropdown.contains(event.target)) {
        this.isDropdownVisible = false;
      }
    },
  },
  mounted() {
    document.addEventListener("click", this.handleClickOutside);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
  },
};
</script>

<style scoped>
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #333;
  padding: 10px 20px;
  height: 60px;
  position: fixed;
  top: 0;
  left: 120px;
  right: 0;
  z-index: 1000;
}

.search-bar {
  flex-grow: 1;
  margin-right: 20px;
}

.search-bar input {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: none;
  font-size: 16px;
  background-color: #444;
  color: white;
}

.search-bar input::placeholder {
  color: #999;
}

.auth-buttons {
  display: flex;
  align-items: center;
}

.profile-button {
  position: relative;
}

.profile-button button {
  background-color: #0f0;
  color: black;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.profile-button button:hover {
  background-color: #0c0;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: #444;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  z-index: 1001;
}

.dropdown-menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.dropdown-menu ul li {
  padding: 10px 20px;
}

.dropdown-menu ul li a {
  text-decoration: none;
  color: white;
  font-size: 14px;
  display: block;
}

.dropdown-menu ul li:hover {
  background-color: #555;
}

.login-button {
  background-color: #0f0;
  color: black;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  text-decoration: none;
  transition: background 0.3s ease;
}

.login-button:hover {
  background-color: #0c0;
}
</style>
