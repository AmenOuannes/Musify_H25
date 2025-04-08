import axios from "axios";
export const URL = "/api";

export async function likePlaylist(playlist_name, token) {
    try {
        const response = await axios.post(`${URL}/users/likes/playlists/${playlist_name.toLowerCase()}`, {}, {
            headers: { Authorization: `Bearer ${token}` }
        });
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.message || 'Unexpected error');
    }
}

export async function unlikePlaylist(playlist_name, token) {
    try {
        const response = await axios.delete(`${URL}/users/likes/playlists/${playlist_name.toLowerCase()}`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.message || 'Unexpected error');
    }
}

export async function getLikedPlaylists(token) {
    try {
        const response = await axios.get(`${URL}/users/likes/playlists`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.message || 'Unexpected error');
    }
}

export async function getPlaylists(limit = 10, research = "", owner = "") {
    try {
        const params = { limit };
        if (research) params.research = research.toLowerCase();
        if (owner) params.owner = owner.toLowerCase();

        const response = await axios.get(`${URL}/playlists`, { params });
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.error || "Unexpected error");
    }
}

export async function getPlaylistByName(playlist_name) {
    try {
        playlist_name = playlist_name.toLowerCase();
        const response = await axios.get(`${URL}/playlists/${playlist_name}`);
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.error || "Unexpected error");
    }
}

export async function postPlaylist(playlist_name, isPrivate, token) {
    try {
        playlist_name = playlist_name.toLowerCase();
        const response = await axios.post(`${URL}/playlists`, {
            playlist_name,
            private: isPrivate ? 1 : 0
        }, {
            headers: { Authorization: `Bearer ${token}` }
        });
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.error || "Unexpected error");
    }
}

export async function deletePlaylist(playlist_name, token) {
    try {
        playlist_name = playlist_name.toLowerCase();
        const response = await axios.delete(`${URL}/playlists/${playlist_name}`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.error || "Unexpected error");
    }
}

export async function getPlaylistSongs(playlist_name, owner ) {
    try {
        playlist_name = playlist_name.toLowerCase();
        owner = owner.toLowerCase();
        const params = {owner};

        const response = await axios.get(`${URL}/playlists/${playlist_name}/songs`, { params });
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.error || "Unexpected error");
    }
}

export async function getSongFromPlaylist(playlist_name, song_name) {
    try {
        playlist_name = playlist_name.toLowerCase();
        song_name = song_name.toLowerCase();
        const response = await axios.get(`${URL}/playlists/${playlist_name}/songs/${song_name}`);
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.error || "Unexpected error");
    }
}

export async function postSongToPlaylist(playlist_name, song_name, token) {
    try {
        playlist_name = playlist_name.toLowerCase();
        song_name = song_name.toLowerCase();
        const response = await axios.post(`${URL}/playlists/${playlist_name}/songs/${song_name}`, {}, {
            headers: { Authorization: `Bearer ${token}` }
        });
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.error || "Unexpected error");
    }
}

export async function deleteSongFromPlaylist(playlist_name, song_name, token) {
    try {
        playlist_name = playlist_name.toLowerCase();
        song_name = song_name.toLowerCase();
        const response = await axios.delete(`${URL}/playlists/${playlist_name}/songs/${song_name}`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.error || "Unexpected error");
    }
}