import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/Home.vue";
import Library from "@/views/Library.vue";
import Favorites from "@/views/Favorites.vue";
import Playlists from "@/views/Playlists.vue";
import Settings from "@/views/Settings.vue";
import SignIn from "@/views/SignIn.vue";
import SignUp from "@/views/SignUp.vue";
import users from "@/views/users.vue";

const routes = [
    {
        path: "/",
        name: "Home",
        component: Home,
    },
    {
        path: "/library",
        name: "Library",
        component: Library,
    },
    {
        path: "/favorites",
        name: "Favorites",
        component: Favorites,
    },
    {
        path: "/playlists",
        name: "Playlists",
        component: Playlists,
    },
    {
        path: "/settings",
        name: "Settings",
        component: Settings,
    },
    {
        path: "/signin",
        name: "SignIn",
        component: SignIn,
    },
    {
        path: "/signup",
        name: "SignUp",
        component: SignUp,
    },
    {
        path: "/users",
        name: "users",
        component: users,
    },

];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;