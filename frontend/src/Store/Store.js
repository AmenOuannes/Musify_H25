import { createStore } from 'vuex'
import Cookies from 'js-cookie'
import { getUser } from '@/api/authApi'

export default createStore({
    state: {
        user: null,
        token: Cookies.get('ufood-token') || null,
    },
    getters: {
        currentToken: state => state.token,
        currentUserData: state => state.userData,
    },
    mutations: {
        setUser(state, user) {
            state.user = user
        },
        updateUserData(state, newUserData) {
            state.currentUserData = newUserData;
        },
        setToken(state, token) {
            state.token = token
            Cookies.set('ufood-token', token, { expires: 7 })
        },
        clearUser(state) {
            state.user = null
        },
        clearToken(state) {
            state.token = null
            Cookies.remove('ufood-token')
        },
        removeToken(state) {
            state.token = null;
            localStorage.removeItem('token');
        },
        updateUserData(state, userData) {
            state.userData = userData;
        },
    },
    actions: {
        async initializeApp({ commit }) {
            try {
                const token = Cookies.get('ufood-token')
                if (token) {
                    const response = await getUser(token)
                    if (response.status === 200) {
                        commit('setUser', response.data)
                        commit('setToken', token)
                    } else {
                        commit('clearUser')
                        commit('clearToken')
                    }
                }
            } catch (error) {
                commit('clearUser')
                commit('clearToken')
                window.location.href = '/signin'
            }
        },
        login({ commit }, { user, token }) {
            commit('setUser', user)
            commit('setToken', token)
        },
        logout({ commit }) {
            commit('clearUser')
            commit('clearToken')
        },
    },
    getters: {
        isLoggedIn: (state) => !!state.user && !!state.token,
        currentUser: (state) => state.user,
        currentToken: (state) => state.token,
    },
})
