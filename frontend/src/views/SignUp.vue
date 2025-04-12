<template>
  <div class="auth-container">
    <h2>Create an Account</h2>

    <form @submit.prevent="handleSignUp">
      <input v-model="username" type="text" placeholder="Username" required />
      <input v-model="firstName" type="text" placeholder="First Name" required />
      <input v-model="lastName" type="text" placeholder="Last Name" required />
      <input v-model="birthDate" type="date" required />
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <input v-model="confirmPassword" type="password" placeholder="Confirm Password" required />

      <button type="submit" :disabled="loading">
        {{ loading ? 'Creating...' : 'Create Account' }}
      </button>
      <p v-if="error" class="error-message">{{ error }}</p>
    </form>

    <p class="switch-link">
      Already have an account?
      <router-link to="/signin">Sign In</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { postUser, login, getUser } from '@/api/AuthApi'

const store = useStore()
const router = useRouter()

const username = ref('')
const firstName = ref('')
const lastName = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const birthDate = ref('')
const loading = ref(false)
const error = ref(null)

const handleSignUp = async () => {
  error.value = null

  const dateRegex = /^\d{4}-\d{2}-\d{2}$/
  if (!dateRegex.test(birthDate.value)) {
    error.value = "Birth date must be in YYYY-MM-DD format."
    return
  }

  if (password.value !== confirmPassword.value) {
    error.value = "Passwords do not match."
    return
  }

  const strongPasswordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/
  if (!strongPasswordRegex.test(password.value)) {
    error.value = "Password must be 8+ chars with a number, special char, upper & lowercase."
    return
  }

  loading.value = true
  try {
    await postUser({
      username: username.value,
      first_name: firstName.value,
      last_name: lastName.value,
      email: email.value,
      password: password.value,
      birth_date: birthDate.value
    })

    const { token } = await login(username.value, password.value)
    const user = await getUser(token)

    await store.dispatch('login', { user, token })
    router.push('/home')
  } catch (err) {
    error.value = err.message
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
