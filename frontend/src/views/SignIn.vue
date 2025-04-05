<template>
  <div class="auth-container">
    <h2>Sign In</h2>

    <form @submit.prevent="handleSignIn">
      <input v-model="username" type="text" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit" :disabled="loading">
        {{ loading ? 'Signing in...' : 'Sign In' }}
      </button>
      <p v-if="error" class="error-message">{{ error }}</p>
    </form>

    <p class="switch-link">
      Don't have an account?
      <router-link to="/signup">Create one</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { login, getUser } from '@/api/AuthApi'

const store = useStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref(null)

const handleSignIn = async () => {
  loading.value = true
  error.value = null

  try {
    const { token } = await login(username.value, password.value)
    const user = await getUser(token)

    await store.dispatch('login', { user, token })
    router.push('/home')
  } catch (err) {
    error.value = 'Invalid username or password.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 5rem auto;
  padding: 2rem;
  background-color: #1e1e1e;
  border-radius: 10px;
  color: white;
  text-align: center;
  box-shadow: 0 0 10px #000;
}

h2 {
  margin-bottom: 1.5rem;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

input {
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #444;
  background-color: #333;
  color: white;
  font-size: 16px;
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

.error-message {
  color: red;
  margin-top: 10px;
}

.switch-link {
  margin-top: 1.5rem;
  font-size: 14px;
  color: #ccc;
}

.switch-link a {
  color: #0f0;
  text-decoration: none;
}

.switch-link a:hover {
  text-decoration: underline;
}
</style>
