import axios from 'axios';
import { handleRequest,API_URL } from './api_lab';

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