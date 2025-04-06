import axios from "axios";
import { URL } from "./api";

export async function postArtists(artist_name, genre, profile_url, image, followers, token) {
    try {
        followers = 0
        const response = await axios.post(`${URL}/artists`, {
            artist_name: artist_name.toLowerCase(),
            genre: genre.toLowerCase(),
            profile_url,
            image,
            followers
        }, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        return response.data;
    } catch (error) {
        console.error("Failed to post artist:", error.response?.data || error.message);
        throw new Error(error.response?.data?.message || "Something went wrong");
    }
}

export async function getArtists(limit = 5, research = "") {
    try {
        const params = { limit };
        if (research) params.research = research.toLowerCase();

        const response = await axios.get(URL + "/artists", { params });

        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error);
    }
}

export async function getArtistByName(artist_name) {
    try {
        artist_name = artist_name.toLowerCase();
        const response = await axios.get(`${URL}/artists/${artist_name}`);
        console.log(response);
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error);
    }
}