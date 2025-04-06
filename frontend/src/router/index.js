import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import SignIn from '../views/SignIn.vue'
import SignUp from '../views/SignUp.vue'
import Favorites from '../views/Favorites.vue'
import Artists from '../Search/Artists.vue'
import Songs from '../Search/Songs.vue'
import Albums from '../Search/Albums.vue'
import Playlists from '../views/Playlists.vue'
import MyPlaylists from '../views/MyPlaylists.vue'
import Settings from '../views/Settings.vue'
import Users from '../views/users.vue'
import store from '../Store/Store.js'

const routes = [
    { path: '/', redirect: '/home' },
    { path: '/signin', component: SignIn },
    { path: '/signup', component: SignUp },
    { path: '/home', component: Home, meta: { requiresAuth: true } },
    { path: '/favorites', component: Favorites, meta: { requiresAuth: true } },
    { path: '/artists', component: Artists, meta: { requiresAuth: true } },
    { path: '/songs', component: Songs, meta: { requiresAuth: true } },
    { path: '/albums', component: Albums, meta: { requiresAuth: true } },
    { path: '/playlists', component: Playlists, meta: { requiresAuth: true } },
    { path: '/myplaylists', component: MyPlaylists, meta: { requiresAuth: true } },
    { path: '/settings', component: Settings, meta: { requiresAuth: true } },
    { path: '/users', component: Users, meta: { requiresAuth: true } },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

// Garde de navigation
router.beforeEach((to, from, next) => {
    const isLoggedIn = store.getters.isLoggedIn
    if (to.meta.requiresAuth && !isLoggedIn) {
        next('/signin')
    } else if ((to.path === '/signin' || to.path === '/signup') && isLoggedIn) {
        next('/home')
    } else {
        next()
    }
})

export default router
