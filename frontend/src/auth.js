import { reactive } from "vue";

export const auth = reactive({
    isLoggedIn: false, // Default to logged out
    isAdmin: false, // Default to non-admin
    user: null, // Store user data when logged in

    login(user, isAdmin = false) {
        this.isLoggedIn = true;
        this.isAdmin = isAdmin;
        this.user = user;
    },

    logout() {
        this.isLoggedIn = false;
        this.isAdmin = false;
        this.user = null;
    },
});