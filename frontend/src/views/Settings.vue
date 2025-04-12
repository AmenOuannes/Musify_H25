<template>
  <div class="settings">
    <h1>Settings</h1>
    <p>Configure your account and preferences here.</p>

    <div v-if="loading" class="loading">Chargement de vos données...</div>
    <div v-else-if="error" class="error-message">{{ error }}</div>

    <div v-else class="settings-container">
      <div class="field-group" v-for="(label, field) in fieldLabels" :key="field">
        <div class="field-label">{{ label }}</div>

        <!-- Text fields -->
        <input
            v-if="field !== 'password' && field !== 'birth_date'"
            type="text"
            class="field-input"
            v-model="editableUserData[field]"
        />

        <!-- Date picker -->
        <input
            v-else-if="field === 'birth_date'"
            type="date"
            class="field-input"
            v-model="editableUserData.birth_date"
        />

        <!-- Password field -->
        <div class="password-container" v-else>
          <input
              :type="showPassword ? 'text' : 'password'"
              class="field-input"
              v-model="editableUserData.password"
              placeholder="Nouveau mot de passe"
          />
          <button type="button" class="toggle-password" @click="togglePasswordVisibility">
            {{ showPassword ? '🔒' : '👁️' }}
          </button>
          <p v-if="passwordInvalid" class="error-message" style="margin-top: 5px;">
            Le mot de passe doit contenir au moins 8 caractères, une majuscule, une minuscule, un chiffre et un caractère spécial.
          </p>
        </div>
      </div>

      <button class="save-btn" @click="saveAll" :disabled="passwordInvalid">Modifier</button>
      <div class="success-message" v-if="successMessage">{{ successMessage }}</div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { putUser, login, getUser } from '@/api/AuthApi'

export default {
  name: 'Settings',
  setup() {
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
      birth_date: user.value?.birth_date ? formatDateForInput(user.value.birth_date) : ''
    })

    const showPassword = ref(false)
    const loading = ref(false)
    const error = ref(null)
    const successMessage = ref(null)

    function formatDateForInput(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toISOString().split('T')[0]
    }

    const isPasswordValid = (password) => {
      const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$/
      return regex.test(password)
    }

    const passwordInvalid = computed(() => {
      return editableUserData.password && !isPasswordValid(editableUserData.password)
    })

    const loadUserData = async () => {
      try {
        const currentUser = store.getters.currentUser
        Object.assign(editableUserData, {
          username: currentUser.username,
          first_name: currentUser.first_name,
          last_name: currentUser.last_name,
          email: currentUser.email,
          password: currentUser.password,
          birth_date: currentUser.birth_date ? formatDateForInput(currentUser.birth_date) : ''
        })
      } catch (err) {
        console.error('Failed to load user data:', err)
      }
    }

    onMounted(() => {
      if (!store.getters.isLoggedIn) {
        error.value = 'Vous devez être connecté pour accéder à cette page'
        setTimeout(() => router.push('/signin'), 2000)
      } else {
        loadUserData()
      }
    })

    const saveAll = async () => {
      loading.value = true
      error.value = null
      successMessage.value = null

      if (editableUserData.password && passwordInvalid.value) {
        error.value = 'Le mot de passe ne respecte pas les critères de sécurité.'
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

        await putUser(payload, token.value)

        const { token: newToken } = await login(
            payload.username,
            editableUserData.password || payload.password
        )

        const updatedUser = await getUser(newToken)

        await store.dispatch('login', {
          user: updatedUser,
          token: newToken
        })

        successMessage.value = 'Profile updated successfully!'
        router.replace('/home')
      } catch (err) {
        error.value = 'Error: ' + (err.response?.data?.message || err.message)
        console.error('Update error:', err)
      } finally {
        loading.value = false
      }
    }

    const togglePasswordVisibility = () => {
      showPassword.value = !showPassword.value
    }

    return {
      editableUserData,
      showPassword,
      loading,
      error,
      successMessage,
      saveAll,
      togglePasswordVisibility,
      passwordInvalid,
      fieldLabels: {
        username: "Nom d'utilisateur",
        first_name: 'Prénom',
        last_name: 'Nom de famille',
        email: 'Email',
        password: 'Mot de passe',
        birth_date: 'Date de naissance'
      }
    }
  }
}
</script>

<style scoped>
.settings {
  background-color: #111;
  color: white;
  font-family: Arial, sans-serif;
  padding: 20px;
}

.settings h1 {
  font-size: 40px;
  margin: 0;
  color: white;
}

.settings p {
  font-size: 20px;
  margin: 10px 0;
  color: #ccc;
}

.settings-container {
  background-color: #1e1e1e;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
  padding: 20px;
  margin-top: 20px;
  color: white;
}

.field-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
  position: relative;
  padding-bottom: 10px;
  border-bottom: 1px solid #333;
}

.field-label {
  font-weight: bold;
  color: #0f0;
  margin-bottom: 5px;
}

.field-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #555;
  border-radius: 4px;
  font-size: 16px;
  background-color: #222;
  color: white;
}

.password-container {
  position: relative;
}

.toggle-password {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: #ccc;
}

.save-btn {
  background-color: limegreen;
  color: black;
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 20px;
}

.save-btn:hover {
  background-color: #0f0;
}

.loading {
  text-align: center;
  padding: 20px;
  font-size: 18px;
  color: limegreen;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 10px;
  border-radius: 4px;
  margin-top: 20px;
}

.success-message {
  background-color: #d4edda;
  color: #155724;
  padding: 10px;
  border-radius: 4px;
  margin-top: 10px;
}
</style>