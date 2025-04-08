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
        },  {
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

export async function getArtists(limit = 5, research = "") {
    try {
        const params = { limit };
        if (research) params.research = research.toLowerCase();

        const response = await axios.get(URL + "/artists", { params });

        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.error || 'Unexpected error');
    }
}

export async function getArtistByName(artist_name) {
    try {
        artist_name = artist_name.toLowerCase();
        const response = await axios.get(`${URL}/artists/${artist_name}`);
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.error || 'Unexpected error');
    }
}

export async function likeArtist(artist_name, token) {
    try {
        const response = await axios.post(`${URL}/users/likes/artists/${artist_name.toLowerCase()}`, {}, {
            headers: { Authorization: `Bearer ${token}` }
        });
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.message || 'Unexpected error');
    }
}

export async function unlikeArtist(artist_name, token) {
    try {
        const response = await axios.delete(`${URL}/users/likes/artists/${artist_name.toLowerCase()}`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.message || 'Unexpected error');
    }
}

export async function getLikedArtists(token) {
    try {
        const response = await axios.get(`${URL}/users/likes/artists`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.message || 'Unexpected error');
    }
}