import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext.jsx';
import { get_labs_for_user, create_new_lab } from '../api/api_lab.js';
import { Link, useNavigate } from 'react-router-dom';
import Modal from 'react-modal';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const UserLabs = () => {
    const { token } = useContext(AuthContext);
    const [labs, setLabs] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [newLabData, setNewLabData] = useState({
        lab_id: '',
        lab_name: '',
        classes: '',
    });
    const [manualLabId, setManualLabId] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchLabs = async () => {
            try {
                const data = await get_labs_for_user(token);
                setLabs(data);
            } catch (error) {
                toast.error('Erro ao carregar labs.');
            }
        };

        fetchLabs();
    }, [token]);

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => {
        setNewLabData({ lab_id: '', lab_name: '', classes: '' });
        setIsModalOpen(false);
    };

    const handleCreateLab = async (e) => {
        e.preventDefault();
        if (!newLabData.lab_id || !newLabData.lab_name || !newLabData.classes) {
            toast.error('Por favor, preencha todos os campos.');
            return;
        }
        try {
            await create_new_lab(token, newLabData);
            toast.success('Lab criado com sucesso!');
            closeModal();
            const updatedLabs = await get_labs_for_user(token);
            setLabs(updatedLabs);
        } catch (error) {
            toast.error('Erro ao criar lab.');
        }
    };

    const handleManualLabEntry = () => {
        if (manualLabId) {
            navigate(`/lab/${manualLabId}`);
        }
    };

    return (
        <>
            <ToastContainer position="top-right" autoClose={3000} />
            <div className="flex flex-col items-center justify-center min-h-screen text-white">
                <div className="w-full max-w-3xl p-10 rounded-2xl shadow-2xl bg-gray-800 space-y-6">
                    <h1 className="text-4xl font-bold text-center mb-8">
                        Selecione um Lab
                    </h1>

                    {labs.length === 0 ? (
                        <p className="text-center text-gray-300">Você não possui labs.</p>
                    ) : (
                        <div className="flex flex-col gap-4">
                            {labs.map((lab) => (
                                <Link
                                    key={lab.lab_id}
                                    to={`/lab/${lab.lab_id}`}
                                    className="w-full px-5 py-3 bg-gray-700 text-white rounded-xl text-lg font-medium text-center hover:bg-indigo-600 transition transform hover:scale-105"
                                >
                                    {lab.lab_name} ({lab.lab_id})
                                </Link>
                            ))}
                        </div>
                    )}

                    <button
                        onClick={openModal}
                        className="w-full px-6 py-3 bg-green-600 text-white rounded-xl text-lg font-semibold hover:bg-green-700 transition transform hover:scale-105"
                    >
                        Criar novo Lab
                    </button>

                    <div className="flex gap-3">
                        <input
                            type="text"
                            placeholder="ID do Lab"
                            value={manualLabId}
                            onChange={(e) => setManualLabId(e.target.value)}
                            className="flex-1 px-4 py-3 border border-gray-600 bg-gray-700 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        />
                        <button
                            onClick={handleManualLabEntry}
                            className="px-6 py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition transform hover:scale-105"
                        >
                            Entrar
                        </button>
                    </div>
                </div>
            </div>

            <Modal
                isOpen={isModalOpen}
                onRequestClose={closeModal}
                contentLabel="Criar novo Lab"
                className="modal-content bg-gray-800 p-8 rounded-2xl shadow-2xl max-w-md mx-auto text-white space-y-6"
                overlayClassName="modal-overlay fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center"
            >
                <h2 className="text-3xl font-bold mb-6">Criar Novo Lab</h2>
                <form onSubmit={handleCreateLab} className="flex flex-col gap-4">
                    <input
                        type="text"
                        placeholder="ID do Lab"
                        value={newLabData.lab_id}
                        onChange={(e) => setNewLabData({ ...newLabData, lab_id: e.target.value })}
                        className="w-full px-4 py-3 border border-gray-600 bg-gray-700 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                    />
                    <input
                        type="text"
                        placeholder="Nome do Lab"
                        value={newLabData.lab_name}
                        onChange={(e) => setNewLabData({ ...newLabData, lab_name: e.target.value })}
                        className="w-full px-4 py-3 border border-gray-600 bg-gray-700 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                    />
                    <input
                        type="text"
                        placeholder="Turmas (ex: 1ano,2ano)"
                        value={newLabData.classes}
                        onChange={(e) => setNewLabData({ ...newLabData, classes: e.target.value })}
                        className="w-full px-4 py-3 border border-gray-600 bg-gray-700 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                    />
                    <div className="flex justify-end gap-4">
                        <button
                            type="button"
                            onClick={closeModal}
                            className="px-5 py-3 bg-gray-600 text-white rounded-xl hover:bg-gray-700 transition transform hover:scale-105"
                        >
                            Cancelar
                        </button>
                        <button
                            type="submit"
                            className="px-5 py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition transform hover:scale-105"
                        >
                            Criar Lab
                        </button>
                    </div>
                </form>
            </Modal>
        </>
    );
};

export default UserLabs;
