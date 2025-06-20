import React, { useState, useContext } from 'react';
import { AuthContext,AuthProvider } from '../../contexts/AuthContext.jsx';
import { Link } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { get_labs_for_user } from '../../api/api_lab.js';

const Login = () => {
    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });

    const pageBg = "bg-[#0D1117]";
    const cardBg = "bg-[#161D27]";
    const { login,token } = useContext(AuthContext);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        await login(formData.username, formData.password);

        //const labs = get_labs_for_user(token);
        //console.log(labs);
    };

    return (
    <>
        <ToastContainer position="top-right" autoClose={3000} />
        <div className={`${pageBg} flex flex-col items-center justify-center min-h-screen`}>
            <div className={`w-full max-w-md p-8 rounded-lg shadow-1xl ${cardBg}`}>
                <h1 className="text-3xl font-bold text-center mb-6">
                    InfoDomus
                </h1>
                <form onSubmit={handleSubmit} className='flex flex-col items-center justify-center gap-4 p-6 w-full max-w-md'>
                    <input
                        type="text"
                        name="username"
                        placeholder="Username"
                        onChange={handleChange}
                        className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    />
                    <input
                        type="password"
                        name="password"
                        placeholder="Password"
                        onChange={handleChange}
                        className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    />
                        <button className={`w-full py-2 bg-indigo-600 text-white font-semibold rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500` }type="submit">Login</button>
                </form>
                <div className="mt-6 text-center">
                    <span className="text-sm text-gray-600">
                        Não tem uma conta?
                    </span>
                    <Link
                        to="/register"
                        className="text-sm text-indigo-600 hover:text-indigo-800 font-semibold ml-1"
                    >
                        Registre-se
                    </Link>
                </div>
            </div>
        </div>
        </>
    );
};

export default Login;