import axios from "axios";
export const URL = "/api";

export async function login(username, password) {
    try {
        username = username.toLowerCase();
        const response = await axios.post(URL + "/users/login", {
            username,
            password
        });
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(error);
    }
}

export async function getUsers(limit = 10, research = "") {
    try {
        const params = {
            limit,
        }

        if (research) params.research = research.toLowerCase();

        const response = await axios.get(URL + "/users", {
            params: params
        });
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
            username: username.toLowerCase(),
            first_name: first_name.toLowerCase(),
            last_name: last_name.toLowerCase(),
            email,
            password,
            birth_date
        })
        return response.data
    } catch (err) {
        console.error(err)
        throw new Error(err.response?.data?.message || err.message)
    }
}

export async function putUser({ username, first_name, last_name, email, password, birth_date }, currentToken) {
    try {
        username = username.toLowerCase()
        const response = await axios.put(`${URL}/users`, {
            username: username,
            first_name: first_name.toLowerCase(),
            last_name: last_name.toLowerCase(),
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