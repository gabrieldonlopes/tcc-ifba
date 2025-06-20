import axios from 'axios';
import { handleRequest } from './api_lab';

const API_URL = import.meta.env.VITE_API_URL;
const API_KEY = import.meta.env.VITE_API_KEY;

const defaultHeaders = {
    'Authorization': API_KEY
};

const create_new_task = (token, taskData) => 
    handleRequest(
        (config) => axios.post(`${API_URL}/tasks/new`, taskData, config),
        token,
        true // precisa de api-key
    );

const complete_task = (token,task_id) =>
    handleRequest(
        (config) => axios.patch(`${API_URL}/tasks/complete/${task_id}`,{}, config),
        token,
        true
    )

export {
    create_new_task,complete_task
};