import axios from "axios";
import { URL } from "./api";

export async function postAlbum(album_name, genre, artist_name, release_date, image, token) {
    try {
        const response = await axios.post(`${URL}/albums/`, {
            album_name: encodeURIComponent(album_name.toLowerCase()),
            genre: encodeURIComponent(genre.toLowerCase()),
            artist_name: encodeURIComponent(artist_name.toLowerCase()),
            release_date,
            image
        }, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.error || 'Unexpected error');
    }
}

export async function getAlbums(limit = 10, research = '') {
    try {
        const params = { limit };
        if (research) params.research = encodeURIComponent(research.toLowerCase());

        const response = await axios.get(`${URL}/albums`, { params });
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.error || 'Unexpected error');
    }
}

export async function getAlbumByName(album_name) {
    try {
        album_name = encodeURIComponent(album_name.toLowerCase());
        const response = await axios.get(`${URL}/albums/${album_name}`);
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.error || 'Unexpected error');
    }
}

export async function getAlbumSongs(album_name) {
    try {
        album_name = encodeURIComponent(album_name.toLowerCase());
        const response = await axios.get(`${URL}/albums/${album_name}/songs`);
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.error || 'Unexpected error');
    }
}

export async function addSongToAlbum(album_name, song_name, token) {
    try {
        album_name = encodeURIComponent(album_name.toLowerCase());
        song_name = encodeURIComponent(song_name.toLowerCase());

        const response = await axios.post(`${URL}/albums/${album_name}/songs/${song_name}`, {}, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.error || 'Unexpected error');
    }
}

export async function deleteSongFromAlbum(album_name, song_name, token) {
    try {
        album_name = encodeURIComponent(album_name.toLowerCase());
        song_name = encodeURIComponent(song_name.toLowerCase());

        const response = await axios.delete(`${URL}/albums/${album_name}/songs/${song_name}`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.error || 'Unexpected error');
    }
}
