import axios from "axios";
import {URL} from "./api";


export async function postArtists(artist_name, genre, profile_url, image, followers, token) {
    try {
        followers = 0
        const response = await axios.post(`${URL}/artists`, {
            artist_name: encodeURIComponent(artist_name),
            genre: encodeURIComponent(genre),
            profile_url: encodeURIComponent(profile_url),
            image: encodeURIComponent(image),
            followers
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

export async function getArtists(limit = 5, research = "") {
    try {
        const params = {limit};
        if (research) params.research = encodeURIComponent(research);

        const response = await axios.get(URL + "/artists", {params});

        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.error || 'Unexpected error');
    }
}

export async function getArtistByName(artist_name) {
    try {
        artist_name = encodeURIComponent(artist_name);
        const response = await axios.get(`${URL}/artists/${artist_name}`);
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.error || 'Unexpected error');
    }
}

export async function likeArtist(artist_name, token) {
    try {
        console.log("Sending artist to like:", token)

        const response = await axios.post(
            `${URL}/users/likes/artists/${encodeURIComponent(artist_name)}`,{},
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

        return response.data
    } catch (error) {
        console.error("❌ likeArtist error:", error.response?.data?.message || error.message)
        throw new Error(error.response?.data?.message || 'Unexpected error')
    }
}

export async function unlikeArtist(artist_name, token) {
    try {
        const response = await axios.delete(`${URL}/users/likes/artists/${encodeURIComponent(artist_name)}`, {
            headers: {Authorization: `Bearer ${token}`}
        });
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.message || 'Unexpected error');
    }
}

export async function getLikedArtists(research, token) {
    try {
        const params = {};
        if (research) params.research = encodeURIComponent(research);
        const response = await axios.get(`${URL}/users/likes/artists`, {
            params,
            headers: {Authorization: `Bearer ${token}`}
        });
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.message || 'Unexpected error');
    }
}

export async function getRecommendedArtists(token) {
    try {
        const response = await axios.get(`${URL}/users/likes/artists/recommended`, {
            headers: {Authorization: `Bearer ${token}`}
        });
        console.log(response);
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error.response?.data?.message || 'Unexpected error');
    }
}