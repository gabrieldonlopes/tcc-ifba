import axios from 'axios';

const API_URL = "http://localhost:8000";
const API_KEY = "4de3df2d3c9df240127d7e21d31fbed13e5bf22fde0e010bd3999a260d5be333";

const handleRequest = async (requestFunction, token = null, useApiKey = false) => {
    try {
        const headers = {};

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        if (useApiKey) {
            headers['api-key'] = API_KEY;
        }

        const config = { headers };

        const response = await requestFunction(config);
        return response.data;
    } catch (error) {
        const errorMessage = error.response?.data?.message || error.message || "Erro desconhecido";
        throw new Error(errorMessage);
    }
};

const get_labs_for_user = (token) => 
    handleRequest((config) => axios.get(`${API_URL}/users/me/labs`, config), token);

const create_new_lab = (token, labData) => 
    handleRequest(
        (config) => axios.post(`${API_URL}/lab/new_lab`, labData, config),
        token,
        true // precisa de api-key
    );

export { get_labs_for_user, create_new_lab };
