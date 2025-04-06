<template>
  <div class="settings">
    <h1>Settings</h1>
    <p>Configure your account and preferences here.</p>

    <div v-if="loading" class="loading">
      Chargement de vos données...
    </div>

    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-else class="settings-container">
      <!-- Nom d'utilisateur -->
      <div class="field-group">
        <div class="field-label">Nom d'utilisateur</div>
        <div class="field-value" v-if="!editFields.username">{{ userData.username }}</div>
        <input
            v-else
            type="text"
            class="field-input"
            v-model="editableUserData.username"
        >
        <button
            v-if="!editFields.username"
            class="edit-btn"
            @click="startEditing('username')"
        >
          Modifier
        </button>
        <div class="action-btns" v-if="editFields.username">
          <button class="save-btn" @click="saveField('username')">Enregistrer</button>
          <button class="cancel-btn" @click="cancelEdit('username')">Annuler</button>
        </div>
      </div>

      <!-- Prénom -->
      <div class="field-group">
        <div class="field-label">Prénom</div>
        <div class="field-value" v-if="!editFields.first_name">{{ userData.first_name }}</div>
        <input
            v-else
            type="text"
            class="field-input"
            v-model="editableUserData.first_name"
        >
        <button
            v-if="!editFields.first_name"
            class="edit-btn"
            @click="startEditing('first_name')"
        >
          Modifier
        </button>
        <div class="action-btns" v-if="editFields.first_name">
          <button class="save-btn" @click="saveField('first_name')">Enregistrer</button>
          <button class="cancel-btn" @click="cancelEdit('first_name')">Annuler</button>
        </div>
      </div>

      <!-- Nom de famille -->
      <div class="field-group">
        <div class="field-label">Nom de famille</div>
        <div class="field-value" v-if="!editFields.last_name">{{ userData.last_name }}</div>
        <input
            v-else
            type="text"
            class="field-input"
            v-model="editableUserData.last_name"
        >
        <button
            v-if="!editFields.last_name"
            class="edit-btn"
            @click="startEditing('last_name')"
        >
          Modifier
        </button>
        <div class="action-btns" v-if="editFields.last_name">
          <button class="save-btn" @click="saveField('last_name')">Enregistrer</button>
          <button class="cancel-btn" @click="cancelEdit('last_name')">Annuler</button>
        </div>
      </div>

      <!-- Email -->
      <div class="field-group">
        <div class="field-label">Email</div>
        <div class="field-value" v-if="!editFields.email">{{ userData.email }}</div>
        <input
            v-else
            type="email"
            class="field-input"
            v-model="editableUserData.email"
        >
        <button
            v-if="!editFields.email"
            class="edit-btn"
            @click="startEditing('email')"
        >
          Modifier
        </button>
        <div class="action-btns" v-if="editFields.email">
          <button class="save-btn" @click="saveField('email')">Enregistrer</button>
          <button class="cancel-btn" @click="cancelEdit('email')">Annuler</button>
        </div>
      </div>

      <!-- Mot de passe -->
      <div class="field-group">
        <div class="field-label">Mot de passe</div>
        <div class="field-value" v-if="!editFields.password">••••••••</div>
        <div class="password-container" v-else>
          <input
              :type="showPassword ? 'text' : 'password'"
              class="field-input"
              v-model="editableUserData.password"
              placeholder="Nouveau mot de passe"
          >
          <button type="button" class="toggle-password" @click="togglePasswordVisibility">
            {{ showPassword ? '🔒' : '👁️' }}
          </button>
        </div>
        <button
            v-if="!editFields.password"
            class="edit-btn"
            @click="startEditing('password')"
        >
          Modifier
        </button>
        <div class="action-btns" v-if="editFields.password">
          <button class="save-btn" @click="saveField('password')">Enregistrer</button>
          <button class="cancel-btn" @click="cancelEdit('password')">Annuler</button>
        </div>
      </div>

      <!-- Message de succès -->
      <div class="success-message" v-if="successMessage">
        {{ successMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import { putUser } from "../api/AuthApi"; // Importez uniquement la fonction putUser

export default {
  name: "Settings",
  setup() {
    const store = useStore();
    const router = useRouter();

    // Vérification si l'utilisateur est connecté
    const isSignedIn = ref(store.getters.isLoggedIn);
    const token = ref(store.state.token);

    // Récupération des données utilisateur depuis le store
    const user = ref(store.state.user);

    // Données utilisateur
    const userData = reactive({
      username: user.value ? user.value.username : '',
      first_name: user.value ? user.value.first_name : '',
      last_name: user.value ? user.value.last_name : '',
      email: user.value ? user.value.email : '',
      password: '',
      birth_date: user.value ? user.value.birth_date : ''
    });

    // Copie des données pour l'édition
    const editableUserData = reactive({
      username: '',
      first_name: '',
      last_name: '',
      email: '',
      password: '',
      birth_date: ''
    });

    // État d'édition pour chaque champ
    const editFields = reactive({
      username: false,
      first_name: false,
      last_name: false,
      email: false,
      password: false
    });

    // États pour les notifications et le chargement
    const showPassword = ref(false);
    const loading = ref(false);
    const error = ref(null);
    const successMessage = ref(null);

    // Vérifier si l'utilisateur est connecté au chargement
    onMounted(() => {
      if (!isSignedIn.value) {
        error.value = "Vous devez être connecté pour accéder à cette page";
        setTimeout(() => {
          router.push('/login');
        }, 2000);
      }
    });

    // Démarrer l'édition d'un champ
    const startEditing = (fieldName) => {
      editableUserData[fieldName] = fieldName === 'password' ? '' : userData[fieldName];
      editFields[fieldName] = true;
    };

    // Sauvegarder un champ
    const saveField = async (fieldName) => {
      try {
        // Si le champ est vide et que c'est le mot de passe, ne pas l'envoyer
        if (fieldName === 'password' && !editableUserData.password) {
          editFields[fieldName] = false;
          return;
        }

        loading.value = true;

        // Préparation des données complètes pour la mise à jour
        const updateData = {
          ...userData,
          [fieldName]: editableUserData[fieldName]
        };

        // Appel API pour mettre à jour l'utilisateur
        await putUser(updateData);

        // Mise à jour des données locales
        if (fieldName !== 'password') {
          userData[fieldName] = editableUserData[fieldName];

          // Mise à jour du store Vuex si nécessaire
          const updatedUser = {
            ...user.value,
            [fieldName]: editableUserData[fieldName]
          };
          store.commit('setUser', updatedUser);
        }

        // Afficher un message de succès
        successMessage.value = `${fieldName} mis à jour avec succès`;
        setTimeout(() => {
          successMessage.value = null;
        }, 3000);

        // Fermer l'édition
        editFields[fieldName] = false;
        loading.value = false;
      } catch (error) {
        loading.value = false;
        error.value = "Erreur lors de la mise à jour: " + error.message;
        console.error("Erreur lors de la mise à jour:", error);
        setTimeout(() => {
          error.value = null;
        }, 3000);
      }
    };

    // Annuler l'édition d'un champ
    const cancelEdit = (fieldName) => {
      editFields[fieldName] = false;
    };

    // Basculer la visibilité du mot de passe
    const togglePasswordVisibility = () => {
      showPassword.value = !showPassword.value;
    };

    return {
      userData,
      editableUserData,
      editFields,
      showPassword,
      loading,
      error,
      successMessage,
      startEditing,
      saveField,
      cancelEdit,
      togglePasswordVisibility
    };
  }
};
</script>

<style scoped>
.settings {
  body {
    background-color: #111;
    color: white;
    font-family: Arial, sans-serif;
    padding: 20px;
  }

  h1 {
    font-size: 40px;
    margin: 0;
    color: white;
  }

  p {
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

  .field-value {
    font-size: 16px;
    padding: 8px 0;
    color: #ccc;
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

  .edit-btn {
    position: absolute;
    right: 0;
    top: 0;
    background-color: limegreen;
    color: black;
    border: none;
    border-radius: 4px;
    padding: 5px 15px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s;
  }

  .edit-btn:hover {
    background-color: #0f0;
  }

  .action-btns {
    margin-top: 10px;
  }

  .save-btn, .cancel-btn {
    padding: 8px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    margin-right: 10px;
  }

  .save-btn {
    background-color: limegreen;
    color: black;
  }

  .save-btn:hover {
    background-color: #0f0;
  }

  .cancel-btn {
    background-color: #e74c3c;
    color: white;
  }

  .cancel-btn:hover {
    background-color: #c0392b;
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
}
</style>