import axios from "axios";
import { URL } from "./api";

export async function postArtits(artist_name, genre, profile_url) {
    try {
        const response = await axios.post(URL + "/artists", {
            artist_name,
            genre,
            profile_url
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

export async function getArtits(limit = 5) {
    try {
        const response = await axios.post(URL + "/artists")

        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error);
    }
}

export async function getArtitsByName(artist_name) {
    try {
        const response = await axios.post(URL + "/artists/" + artist_name)

        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error);
    }
}