<template>
  <div class="signup">
    <h1>Sign Up</h1>
    <form @submit.prevent="signup">
      <input type="text" v-model="username" placeholder="Username" required />
      <input type="password" v-model="password" placeholder="Password" required />
      <button type="submit">Sign Up</button>
    </form>
    <p>Already have an account? <router-link to="/signin">Sign In</router-link></p>
  </div>
</template>

<script>
import { auth } from "@/auth"; // Import the auth state

export default {
  name: "SignUp",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    signup() {
      // Simulate a signup (replace with actual API call)
      auth.login({ username: this.username }); // Automatically log in after signup
      this.$router.push("/"); // Redirect to home after signup
    },
  },
};
</script>

<style scoped>
.signup {
  background-color: #222;
  padding: 40px;
  border-radius: 10px;
  text-align: center;
  width: 100%;
  max-width: 400px;
}

h1 {
  font-size: 40px;
  margin: 0 0 20px;
  color: #0f0;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

input {
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #444;
  font-size: 16px;
  background-color: #333;
  color: white;
}

button {
  background-color: #0f0;
  color: black;
  border: none;
  padding: 10px;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s ease;
}

button:hover {
  background-color: #0c0;
}

p {
  font-size: 16px;
  margin: 20px 0 0;
  color: #ccc;
}

a {
  color: #0f0;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>