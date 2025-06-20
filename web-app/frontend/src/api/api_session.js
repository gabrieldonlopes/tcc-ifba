import axios from 'axios';
import { handleRequest,API_URL } from './api_lab';

const get_sessions_for_lab = (lab_id) => 
    handleRequest(
        (config) => axios.get(`${API_URL}/session/lab/${lab_id}`, config),
        null,
        true // precisa da chave de api
    );

const get_sessions_for_machine = (machine_key) => 
    handleRequest(
        (config) => axios.get(`${API_URL}/session/machine/${machine_key}`, config),
        null,
        true // precisa da chave de api
    );

    const get_sessions_for_student = (student_id) => 
        handleRequest(
            (config) => axios.get(`${API_URL}/session/student/${student_id}`, config),
            null,
            true // precisa da chave de api
        );

export {
    get_sessions_for_lab,get_sessions_for_machine,get_sessions_for_student
}