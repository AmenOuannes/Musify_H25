<template>
  <div class="settings">
    <h1>Settings</h1>
    <p>Configure your account and preferences here.</p>

    <div v-if="loading" class="loading">Chargement de vos données...</div>
    <div v-else-if="error" class="error-message">{{ error }}</div>

    <div v-else class="settings-container">
      <div class="field-group" v-for="(label, field) in fieldLabels" :key="field">
        <div class="field-label">{{ label }}</div>

        <input
            v-if="field !== 'password' && field !== 'birth_date'"
            type="text"
            class="field-input"
            v-model="editableUserData[field]"
        />

        <input
            v-else-if="field === 'birth_date'"
            type="date"
            class="field-input"
            v-model="editableUserData.birth_date"
        />

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

        const newUser = await putUser(payload, token.value)

        const { token: newToken } = await login(
            newUser.user_name,
            newUser.password
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
  font-family: 'Segoe UI', Arial, sans-serif;
  padding: 30px;
  min-height: 100vh;
}

.settings-header {
  text-align: center;
  margin-bottom: 40px;
  position: relative;
}

.settings-header:after {
  content: "";
  position: absolute;
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, #0f0, #00ff9d);
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 2px;
}

.settings h1 {
  font-size: 48px;
  margin: 0;
  color: white;
  text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
  letter-spacing: 2px;
}

.settings p {
  font-size: 18px;
  margin: 15px 0;
  color: #aaa;
}

.settings-container {
  background-color: rgba(30, 30, 30, 0.8);
  border-radius: 15px;
  box-shadow: 0 0 30px rgba(0, 255, 0, 0.15),
  0 5px 15px rgba(0, 0, 0, 0.4);
  padding: 30px;
  margin: 0 auto;
  max-width: 700px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 0, 0.1);
}

.field-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 25px;
  position: relative;
  padding-bottom: 15px;
  border-bottom: 1px solid #333;
}

.field-label {
  font-weight: bold;
  color: #0f0;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  font-size: 18px;
}

.field-icon {
  margin-right: 10px;
  font-size: 22px;
}

.input-wrapper {
  position: relative;
}

.field-input {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #333;
  border-radius: 8px;
  font-size: 16px;
  background-color: whitesmoke;
  color: black;
  transition: all 0.3s ease;
}

.field-input:focus {
  border-color: #0f0;
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 255, 0, 0.2);
}

.password-container {
  position: relative;
}

.toggle-password {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: #ccc;
  font-size: 18px;
  transition: color 0.3s;
}

.toggle-password:hover {
  color: #0f0;
}

.save-btn {
  background: linear-gradient(135deg, #0f0, #00bf00);
  color: black;
  padding: 14px 30px;
  font-size: 18px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 25px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  transition: transform 0.3s, box-shadow 0.3s;
  box-shadow: 0 4px 6px rgba(0, 255, 0, 0.2);
}

.save-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 10px rgba(0, 255, 0, 0.3);
}

.save-btn:active {
  transform: translateY(1px);
}

.btn-icon {
  margin-right: 10px;
  font-size: 20px;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  font-size: 18px;
  color: #0f0;
}

.loader {
  border: 4px solid rgba(0, 255, 0, 0.1);
  border-radius: 50%;
  border-top: 4px solid #0f0;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  background-color: rgba(248, 215, 218, 0.9);
  color: #721c24;
  padding: 12px 15px;
  border-radius: 8px;
  margin-top: 15px;
  display: flex;
  align-items: center;
  border-left: 4px solid #f44336;
}

.error-icon {
  margin-right: 10px;
  font-size: 20px;
}

.success-message {
  background-color: rgba(212, 237, 218, 0.9);
  color: #155724;
  padding: 12px 15px;
  border-radius: 8px;
  margin-top: 15px;
  display: flex;
  align-items: center;
  border-left: 4px solid #28a745;
}

.success-icon {
  margin-right: 10px;
  font-size: 20px;
}

/* Animation pour les champs */
@keyframes fieldFocus {
  0% { transform: scale(0.98); }
  50% { transform: scale(1.01); }
  100% { transform: scale(1); }
}

.field-input:focus {
  animation: fieldFocus 0.3s ease;
}
.custom-eye {
  position: relative;
  width: 22px;
  height: 14px;
  border: 2px solid #0f0;
  border-radius: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.eye-ball {
  width: 8px;
  height: 8px;
  background: whitesmoke;
  border-radius: 50%;
  transition: transform 0.3s;
}

.eye-slash {
  position: absolute;
  width: 26px;
  height: 2px;
  background: white;
  transform: rotate(45deg);
}

.eye-closed .eye-ball {
  transform: scale(0.8);
}

.toggle-password:hover .custom-eye {
  border-color: #00ff9d;
}
</style>