import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;
const API_KEY = import.meta.env.VITE_API_KEY;

const defaultHeaders = {
    'Authorization': API_KEY
};

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

const get_lab = (lab_id) => 
    handleRequest((config) => axios.get(`${API_URL}/lab/${lab_id}`, config), null, true);

const create_new_lab = (token, labData) => 
    handleRequest(
        (config) => axios.post(`${API_URL}/lab/new_lab`, labData, config),
        token,
        true // precisa de api-key
    );

const update_lab = (token, lab_id, labData) =>
    handleRequest(
        (config) => axios.patch(`${API_URL}/update/${lab_id}`, labData, config),
        token,
        true
    );

const join_lab = (token, lab_id) =>
    handleRequest(
        (config) => axios.post(`${API_URL}/lab/join/${lab_id}`, {}, config),
        token,
        true
    );
    
const delete_lab = (token, lab_id) =>
    handleRequest(
        (config) => axios.delete(`${API_URL}/lab/delete/${lab_id}`, config),
        token,
        true
    );

const get_labs_for_user = (token) => 
    handleRequest((config) => axios.get(`${API_URL}/users/me/labs`, config), token);

const get_machines_for_lab = (lab_id) => 
    handleRequest(
        (config) => axios.get(`${API_URL}/lab/${lab_id}/machines`, config),
        null,
        true
    );

const get_students_for_lab = (lab_id) => 
    handleRequest(
        (config) => axios.get(`${API_URL}/lab/${lab_id}/students`, config),
        null,
        true
    );

const get_tasks_for_lab = (token,lab_id) => 
    handleRequest(
        (config) => axios.get(`${API_URL}/tasks/lab/${lab_id}`, config),
        token,
        true
    );

const get_users_for_lab = () =>
    handleRequest(
        (config) => axios.get(`${API_URL}/${lab_id}/users`, config),
        null,
        true
    );

export {
    get_lab, get_labs_for_user, create_new_lab, update_lab,
    join_lab, delete_lab, get_machines_for_lab, get_users_for_lab,
    handleRequest,get_students_for_lab,get_tasks_for_lab,API_URL
};
