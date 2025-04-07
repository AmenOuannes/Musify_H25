import axios from "axios";
import { URL } from "./api";


export async function postSong(song_name, genre, artist_name, release_date, url, token) {
    try {
        const response = await axios.post(URL + "/songs", {
            song_name: song_name.toLowerCase(),
            genre: genre.toLowerCase(),
            artist_name: artist_name.toLowerCase(),
            release_date,
            url
        }, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })

        return response.data
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.error || 'Unexpected error');
    }
}

export async function getSongs(limit = 10, research = '') {
    try {
        const params = { limit }
        if (research) params.research = research
        const response = await axios.get(`${URL}/songs`, { params })
        return response.data
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.error || 'Unexpected error');
    }
}

export async function getSongByName(song_name) {
    try {
        song_name = song_name.toLowerCase()
        const response = await axios.get(`${URL}/songs/${song_name}`)
        return response.data
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.error || 'Unexpected error');
    }
}
