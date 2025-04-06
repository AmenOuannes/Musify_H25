import axios from "axios";
import { URL } from "./api";


export async function postSong(song_name, genre, artist, release_date, url) {
    try {
        const response = await axios.post(URL + "/songs", {
            song_name,
            genre,
            artist,
            release_date,
            url
        },  {
            headers: {
                'Content-Type': 'application/json'
            }
        })

        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error);
    }
}

export async function getSongs(limit = 5, q = '') {
    try {
        const response = await axios.post(URL + "/songs",
            )

        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error);
    }
}

export async function getSongByName(artist_name) {
    try {
        const response = await axios.post(URL + "/songs/" + artist_name)

        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error);
    }
}