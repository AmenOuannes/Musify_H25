import axios from "axios";
import { URL } from "./api";

export async function postAlbum(album_name, genre, artist_name, release_date, image, token) {
    try {
        const response = await axios.post(`${URL}/albums/`, {
            album_name: album_name.toLowerCase(),
            genre: genre.toLowerCase(),
            artist_name: artist_name.toLowerCase(),
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
        throw new Error(error);
    }
}

export async function getAlbums(limit = 10, research = '') {
    try {
        const params = { limit };
        if (research) params.research = research;

        const response = await axios.get(`${URL}/albums`, { params });
        return response.data;
    } catch (error) {
        console.error(error);
        throw error;
    }
}

export async function getAlbumByName(album_name) {
    try {
        album_name = album_name.toLowerCase();
        const response = await axios.get(`${URL}/albums/${album_name}`);
        return response.data;
    } catch (error) {
        console.error(error);
        throw error;
    }
}

export async function getAlbumSongs(album_name) {
    try {
        album_name = album_name.toLowerCase();
        const response = await axios.get(`${URL}/albums/${album_name}/songs`);
        return response.data;
    } catch (error) {
        console.error(error);
        throw error;
    }
}

export async function addSongToAlbum(album_name, song_name, token) {
    try {
        album_name = album_name.toLowerCase();
        song_name = song_name.toLowerCase();

        const response = await axios.post(`${URL}/albums/${album_name}/songs/${song_name}`, {}, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error);
    }
}

export async function deleteSongFromAlbum(album_name, song_name, token) {
    try {
        album_name = album_name.toLowerCase();
        song_name = song_name.toLowerCase();

        const response = await axios.delete(`${URL}/albums/${album_name}/songs/${song_name}`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error);
    }
}
