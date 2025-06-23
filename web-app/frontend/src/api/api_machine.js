import axios from 'axios';
import { handleRequest,API_URL } from './api_lab';

const get_machine_config = (machine_key) => 
    handleRequest(
        (config) => axios.get(`${API_URL}/machine_config/${machine_key}`, config), 
        null,
        true // precisa da chave de api
    );

const update_last_check = (token, machine_key,new_check) =>
    handleRequest(
        (config) => axios.patch(`${API_URL}/machine_config/update/${machine_key}/last_check`, new_check, config),
        token,
        true // precisa da chave de api
    );

const update_state_cleanliness = (token, machine_key,new_state) =>
    handleRequest(
        (config) => axios.patch(`${API_URL}/machine_config/update/${machine_key}/state_cleanliness`, new_state, config),
        token,
        true // precisa da chave de api
    );

const get_tasks_for_machine = (token,machine_key) => 
    handleRequest(
        (config) => axios.get(`${API_URL}/tasks/machine/${machine_key}`, config),
        token,
        true
    );
export {
    get_machine_config,update_last_check,update_state_cleanliness,get_tasks_for_machine
}