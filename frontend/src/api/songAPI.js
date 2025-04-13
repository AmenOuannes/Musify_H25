import axios from "axios";
import { URL } from "./api";


export async function postSong(song_name, genre, artist_name, release_date, url, token) {
    try {
        const response = await axios.post(URL + "/songs", {
            song_name: encodeURIComponent(song_name),
            genre: encodeURIComponent(genre),
            artist_name: encodeURIComponent(artist_name),
            release_date,
            url: encodeURIComponent(url),
        }, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })

        return response.data
    } catch (error) {
        throw new Error(error.response?.data?.message  || 'Unexpected error');
    }
}

export async function getSongs(limit = 10, research = '') {
    try {
        const params = { limit }
        if (research) params.research = encodeURIComponent(research);
        const response = await axios.get(`${URL}/songs`, { params })
        return response.data
    } catch (error) {
        throw new Error(error.response?.data?.message  || 'Unexpected error');
    }
}

export async function getSongByName(song_name) {
    try {
        song_name = encodeURIComponent(song_name);
        const response = await axios.get(`${URL}/songs/${song_name}`)
        return response.data
    } catch (error) {
        throw new Error(error.response?.data?.message  || 'Unexpected error');
    }
}
