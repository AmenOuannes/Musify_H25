import axios from "axios";
import store from "@/Store/Store.js";
export const URL = "/api";

export async function login(username, password) {
    try {
        const response = await axios.post(URL + "/users/login", {
            username,
            password
        }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error);
    }
}

export async function getUsers() {
    try {
        const response = await axios.get(URL + "/users");
        return response.data;
    }catch(err) {
        console.error(err);
        throw new Error(err.message);
    }
}

export async function getUser(token) {
    try {
        const response = await axios.get(URL + "/users/user", {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        return response.data;
    } catch (err) {
        console.error(err);
        throw new Error(err.message);
    }
}

export async function postUser({ username, first_name, last_name, email, password, birth_date }) {
    try {
        const response = await axios.post(`${URL}/users`, {
            username,
            first_name,
            last_name,
            email,
            password,
            birth_date
        }, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
        return response.data
    } catch (err) {
        console.error(err)
        throw new Error(err.response?.data?.message || err.message)
    }
}

export async function putUser({ username, first_name, last_name, email, password, birth_date }, currentToken) {
    try {
        const response = await axios.put(`${URL}/users`, {
            username,
            first_name,
            last_name,
            email,
            password,
            birth_date
        }, {
            headers: {
                Authorization: `Bearer ${currentToken}`
            }
        })

        return { username, password }
    } catch (err) {
        console.error(err)
        throw new Error(err.response?.data?.message || err.message)
    }
}