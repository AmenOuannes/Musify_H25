import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import SignIn from '../views/SignIn.vue'
import SignUp from '../views/SignUp.vue'
import FavoriteArtists from '../Favorites/FavoriteArtists.vue'
import Artists from '../Artists/Artists.vue'
import Songs from '../Songs/Songs.vue'
import Albums from '../Albums/Albums.vue'
import Playlists from '../Playlists/Playlists.vue'
import FavoritePlaylists from '../Favorites/FavoritePlaylists.vue'
import MyPlaylists from '../MyPlaylists/MyPlaylists.vue'
import Settings from '../views/Settings.vue'
import Users from '../views/users.vue'
import store from '../Store/Store.js'

const routes = [
    { path: '/', redirect: '/home' },
    { path: '/signin', component: SignIn },
    { path: '/signup', component: SignUp },
    { path: '/home', component: Home, meta: { requiresAuth: true } },
    { path: '/artists', component: Artists, meta: { requiresAuth: true } },
    {
        path: '/artists/:name',
        name: 'ArtistDetail',
        component: () => import('../Artists/Artist.vue'),
        meta: { requiresAuth: true }
    },
    { path: '/songs', component: Songs, meta: { requiresAuth: true } },
    {
        path: '/songs/:name',
        name: 'SongDetail',
        component: () => import('../Songs/Song.vue'),
        meta: { requiresAuth: true }
    },
    { path: '/albums', component: Albums, meta: { requiresAuth: true } },
    {
        path: '/albums/:name',
        name: 'AlbumDetail',
        component: () => import('../Albums/Album.vue'),
        meta: { requiresAuth: true }
    },
    { path: '/playlists', component: Playlists, meta: { requiresAuth: true } },
    {path: '/favorite/playlists', component: FavoritePlaylists, meta: { requiresAuth: true } },

    {
        path: '/playlists/:name',
        name: 'PlaylistDetail',
        component: () => import('../Playlists/Playlist.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/playlists/:name/play',
        name: 'PlaylistPlayer',
        component: () => import('@/views/PlaylistPlayer.vue'),
        meta: { requiresAuth: true }
    },
    {path: '/favorite/artists', component: FavoriteArtists, meta: { requiresAuth: true } },
    { path: '/myplaylists', component: MyPlaylists, meta: { requiresAuth: true } },
    { path: '/settings', component: Settings, meta: { requiresAuth: true } },
    { path: '/users', component: Users, meta: { requiresAuth: true } }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

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
