import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'
import store from './Store/Store.js' // ici

store.dispatch('initializeApp').then(() => {
    const app = createApp(App)
    app.use(router)
    app.use(store)
    app.mount('#app')
})
