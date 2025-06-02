import React, { useState, useContext } from 'react';
import { AuthContext,AuthProvider } from '../contexts/AuthContext.jsx';
import { Link } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
const Login = () => {
    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });

    const { login } = useContext(AuthContext);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        login(formData.username, formData.password);
    };

    return (
    <>
        <ToastContainer position="top-right" autoClose={3000} />
        <div className="flex flex-col items-center justify-center min-h-screen">
            <div className="w-full max-w-md p-8 rounded-lg shadow-1xl bg-gray-800">
                <h1 className="text-3xl font-bold text-center mb-6">
                    TCC - teste
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
                    <button type="submit">Login</button>
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