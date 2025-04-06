import axios from "axios";
import { URL } from "./api";


export async function postSong(song_name, genre, artist, release_date, url, token) {
    try {
        const response = await axios.post(URL + "/songs", {
            song_name: song_name.toLowerCase(),
            genre: genre.toLowerCase(),
            artist: artist.toLowerCase(),
            release_date,
            url
        },  {
            headers: {Authorization: `Bearer ${token}`}
        })

        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error);
    }
}

export async function getSongs(limit = 5, research = '') {
    try {
        const params = {
            limit,
        }
        if (research) params.research = research.toLowerCase();

        const response = await axios.post(URL + "/songs",
            {
            params: params
        })

        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error);
    }
}

export async function getSongByName(artist_name) {
    try {
        artist_name = artist_name.toLowerCase();
        const response = await axios.post(URL + "/songs/" + artist_name)

        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error);
    }
}