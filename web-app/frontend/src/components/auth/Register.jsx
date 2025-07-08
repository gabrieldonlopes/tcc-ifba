import React, { useState, useContext } from 'react';
import { AuthContext,AuthProvider } from '../../contexts/AuthContext.jsx';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Register = () => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: ''
    });

    const pageBg = "bg-[#0D1117]";
    const cardBg = "bg-[#161D27]";

    const { register } = useContext(AuthContext);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value }); // método esquisitão
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        register(formData.username, formData.email, formData.password); // o AuthContext permite a utilização de seu método por esse componente
    };

    return (
        <>
        <ToastContainer position="top-right" autoClose={3000} />
            <div className={`flex flex-col items-center justify-center min-h-screen ${pageBg}`}>
                <div className={`w-full max-w-md p-8 rounded-lg shadow-2xl ${cardBg}`}>
                    <h1 className="text-3xl font-bold text-gray-300 text-center mb-6">
                        InfoDomus
                    </h1>
                    <form onSubmit={handleSubmit} className='flex flex-col items-center justify-center gap-4 p-6 w-full max-w-md'>
                        <input
                            type="text"
                            name="username"
                            placeholder="Username"
                            onChange={handleChange}
                            className='w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'
                        />
                        <input
                            type="email"
                            name="email"
                            placeholder="Email"
                            onChange={handleChange}
                            className='w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'
                        />
                        <input
                            type="password"
                            name="password"
                            placeholder="Password"
                            onChange={handleChange}
                            className='w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'
                        />
                        <button
                            type="submit"
                            className='w-full py-2 bg-indigo-600 text-white font-semibold rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500'
                        >
                            Register
                        </button>
                    </form>
                </div>
            </div>
            </>
    );
};

export default Register;