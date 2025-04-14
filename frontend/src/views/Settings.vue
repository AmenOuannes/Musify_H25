<template>
  <div class="settings-page">
    <div class="settings-container">
      <h1>⚙️ Settings</h1>
      <p>Manage your profile information</p>

      <div v-if="loading" class="loading">Loading user data...</div>
      <div v-else-if="error" class="error-message">{{ error }}</div>

      <form v-else class="form-wrapper" @submit.prevent="saveAll">
        <div
            class="form-group"
            v-for="(label, field) in fieldLabels"
            :key="field"
        >
          <label class="label">{{ label }}</label>

          <input
              v-if="field !== 'password' && field !== 'birth_date'"
              type="text"
              class="input"
              v-model="editableUserData[field]"
          />

          <input
              v-else-if="field === 'birth_date'"
              type="date"
              class="input"
              v-model="editableUserData.birth_date"
          />

          <!-- Password fields -->
          <template v-else>
            <div class="password-wrapper">
              <input
                  :type="showPassword ? 'text' : 'password'"
                  class="input"
                  v-model="editableUserData.password"
                  placeholder="New password"
              />
              <button type="button" class="toggle" @click="togglePasswordVisibility">
                {{ showPassword ? '🙈' : '👁️' }}
              </button>
            </div>

            <div class="password-wrapper">
              <input
                  :type="showPassword ? 'text' : 'password'"
                  class="input"
                  v-model="confirmPassword"
                  placeholder="Confirm new password"
              />
              <button type="button" class="toggle" @click="togglePasswordVisibility">
                {{ showPassword ? '🙈' : '👁️' }}
              </button>
            </div>

            <p v-if="editableUserData.password && !isPasswordValid(editableUserData.password)" class="error-message" style="margin-top: 5px">
              Password must be 8+ chars with uppercase, lowercase, number, and special character.
            </p>

            <p v-if="editableUserData.password && confirmPassword && editableUserData.password !== confirmPassword" class="error-message" style="margin-top: 5px">
              Passwords do not match.
            </p>
          </template>
        </div>

        <button class="submit-btn" type="submit" :disabled="passwordInvalid">
          Save Changes
        </button>

        <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { putUser, login, getUser } from '@/api/AuthApi'

const store = useStore()
const router = useRouter()

const user = ref(store.getters.currentUser)
const token = ref(store.getters.currentToken)

const editableUserData = reactive({
  username: user.value?.username || '',
  first_name: user.value?.first_name || '',
  last_name: user.value?.last_name || '',
  email: user.value?.email || '',
  password: user.value?.password || '',
  birth_date: user.value?.birth_date ? formatDate(user.value.birth_date) : ''
})

const confirmPassword = ref(user.value?.password || '',)
const showPassword = ref(false)
const loading = ref(false)
const error = ref(null)
const successMessage = ref(null)

function formatDate(date) {
  const d = new Date(date)
  return d.toISOString().split('T')[0]
}

const isPasswordValid = (pwd) => {
  const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$/
  return regex.test(pwd)
}

const passwordInvalid = computed(() => {
  const pwd = editableUserData.password
  return pwd && (!isPasswordValid(pwd) || pwd !== confirmPassword.value)
})

const loadUserData = () => {
  const current = store.getters.currentUser
  Object.assign(editableUserData, {
    username: current.username,
    first_name: current.first_name,
    last_name: current.last_name,
    email: current.email,
    password: current.password,
    birth_date: current.birth_date ? formatDate(current.birth_date) : ''
  })
}

const saveAll = async () => {
  loading.value = true
  error.value = null
  successMessage.value = null

  if (editableUserData.password && passwordInvalid.value) {
    error.value = 'Password does not meet requirements or does not match.'
    loading.value = false
    return
  }

  try {
    const payload = {
      username: editableUserData.username,
      first_name: editableUserData.first_name,
      last_name: editableUserData.last_name,
      email: editableUserData.email,
      ...(editableUserData.password && { password: editableUserData.password }),
      ...(editableUserData.birth_date && { birth_date: editableUserData.birth_date })
    }

    const updated = await putUser(payload, token.value)
    const { token: newToken } = await login(updated.user_name, updated.password)
    const fullUser = await getUser(newToken)

    await store.dispatch('login', {
      user: fullUser,
      token: newToken
    })

    successMessage.value = '✅ Profile updated successfully!'
    router.replace('/home')
  } catch (err) {
    error.value = 'Error updating user: ' + (err.response?.data?.message || err.message)
  } finally {
    loading.value = false
  }
}

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

const fieldLabels = {
  username: 'Username',
  first_name: 'First Name',
  last_name: 'Last Name',
  email: 'Email',
  password: 'Password',
  birth_date: 'Birth Date'
}

onMounted(() => {
  if (!store.getters.isLoggedIn) {
    error.value = 'You must be logged in.'
    setTimeout(() => router.push('/signin'), 2000)
  } else {
    loadUserData()
  }
})
</script>

<style scoped>
.settings-page {
  padding: 2rem;
  background-color: #121212;
  color: white;
  min-height: 100vh;
}

.settings-container {
  background-color: #1e1e1e;
  padding: 2rem 2.5rem;
  border-radius: 16px;
  max-width: 700px;
  margin: auto;
  box-shadow: 0 0 25px rgba(0, 255, 100, 0.1);
}

.settings-container h1 {
  font-size: 2.5rem;
  color: #1ed760;
  margin-bottom: 0.5rem;
}

.settings-container p {
  color: #ccc;
  margin-bottom: 2rem;
}

.form-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1.8rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.label {
  font-weight: bold;
  color: #1ed760;
  margin-bottom: 0.5rem;
}

.input {
  padding: 0.9rem 1.2rem;
  border: none;
  border-radius: 10px;
  background-color: #282828;
  color: white;
  font-size: 1rem;
  transition: border 0.2s, box-shadow 0.2s;
  width: 100%;
  box-sizing: border-box;
}

.input:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(30, 215, 96, 0.5);
}

.password-wrapper {
  position: relative;
  margin-bottom: 1rem;
}

.toggle {
  position: absolute;
  top: 50%;
  right: 15px;
  transform: translateY(-50%);
  background: none;
  color: #ccc;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
}

.toggle:hover {
  color: #1ed760;
}

.submit-btn {
  background-color: #1ed760;
  border: none;
  padding: 0.9rem 1.5rem;
  font-size: 1rem;
  color: black;
  font-weight: bold;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.submit-btn:hover {
  background-color: #1db954;
  transform: translateY(-1px);
}

.submit-btn:disabled {
  background-color: #999;
  cursor: not-allowed;
}

.loading {
  font-size: 1.2rem;
  text-align: center;
  color: #1ed760;
}

.error-message {
  background-color: rgba(255, 0, 0, 0.1);
  color: #ff6b6b;
  padding: 10px 15px;
  border-left: 4px solid red;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.success-message {
  background-color: rgba(0, 255, 100, 0.1);
  color: #3ae374;
  padding: 10px 15px;
  border-left: 4px solid #1ed760;
  border-radius: 8px;
  margin-top: 1rem;
}
</style>
