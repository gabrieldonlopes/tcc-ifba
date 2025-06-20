import axios from 'axios';
import { handleRequest,API_URL } from './api_lab';

const get_machine_config = (machine_key) => 
    handleRequest(
        (config) => axios.get(`${API_URL}/machine_config/${machine_key}`, config), 
        null,
        true // precisa da chave de api
    );

export {
    get_machine_config
}