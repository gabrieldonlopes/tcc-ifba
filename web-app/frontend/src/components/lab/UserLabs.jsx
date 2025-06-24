import React, { useState, useEffect, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Modal from 'react-modal';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// Contexto e API
import { AuthContext } from '../../contexts/AuthContext.jsx';
import { get_labs_for_user, create_new_lab,join_lab } from '../../api/api_lab.js';

// Componentes e Ícones
import Header from '../../components/Header.jsx'; // Verifique o caminho para seu Header
import { FiPlus, FiLogIn, FiMonitor, FiX, FiArrowRight } from 'react-icons/fi';

// Define o elemento raiz para o Modal
Modal.setAppElement('#root');

const UserLabs = () => {
    const { token } = useContext(AuthContext);
    const [labs, setLabs] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [newLabData, setNewLabData] = useState({ lab_id: '', lab_name: '', classes: '' });
    const [manualLabId, setManualLabId] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchLabs = async () => {
            if (token) {
                try {
                    const data = await get_labs_for_user(token);
                    setLabs(data);
                } catch (error) {
                    toast.error('Erro ao carregar seus laboratórios.');
                }
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
        try {
            await create_new_lab(token, newLabData);
            toast.success('Laboratório criado com sucesso!');
            const updatedLabs = await get_labs_for_user(token);
            setLabs(updatedLabs);
            closeModal();
        } catch (error) {
            const errorMessage = error.response?.data?.error || 'Erro ao criar o laboratório.';
            toast.error(errorMessage);
        }
    };

    const handleManualLabEntry = async () => {
        const trimmedId = manualLabId.trim();
        if (!trimmedId) {
            toast.warn('Por favor, insira um ID de laboratório.');
            return;
        }

        try {
            await join_lab(token, trimmedId);
            toast.success('Você foi adicionado ao laboratório com sucesso!');
        } catch (error) {
            if (error.response?.status === 409) {
                toast.info('Você já está vinculado a este laboratório.');
            } else {
                const errorMessage = error.response?.data?.error || 'Erro ao participar do laboratório.';
                toast.error(errorMessage);
                return;
            }
        }

        try {
            const updatedLabs = await get_labs_for_user(token);
            setLabs(updatedLabs);
        } catch {
            // Isso é secundário, então só avisa caso falhe
            toast.warn('Não foi possível atualizar a lista de laboratórios.');
        }

    };

    // Estilo do Fundo da Página (mais escuro como na imagem)
    //const pageBg = "bg-[#0D1117]"; 
    // Estilo do Fundo dos Cards (tom azulado escuro)
    const cardBg = "bg-[#161D27]";
    const pageBg = "bg-[#0D1117]";

    return (
        <div className={`${pageBg} flex flex-col min-h-screen `}>
            <ToastContainer position="bottom-right" autoClose={3000} />
            <Header pageTitle="Meus Laboratórios" />

            {/* Container principal que centraliza o conteúdo */}
            <main className="flex flex-col flex-grow items-center justify-center p-4">
                <div className="w-full max-w-2xl space-y-8">
                    
                    {/* Lista de Laboratórios em Cards */}
                    {labs.length > 0 && (
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                            {labs.map((lab) => (
                                <Link
                                    key=    {lab.lab_id}
                                    to={`/lab/${lab.lab_id}`}
                                    className={`group ${cardBg} p-6 rounded-lg border border-gray-800 hover:border-blue-700 transition-all duration-300 transform hover:-translate-y-1`}
                                >
                                    <FiMonitor className="text-blue-500 mb-4" size={28} />
                                    <h3 className="text-xl font-bold text-gray-100 truncate">{lab.lab_name}</h3>
                                    <p className="text-sm text-gray-400">ID: {lab.lab_id}</p>
                                </Link>
                            ))}
                        </div>
                    )}
                    
                    {/* Seção de Ações */}
                    <div className={`${cardBg} p-6 rounded-lg border border-gray-800`}>
                        <h2 className="text-lg font-semibold text-gray-200 mb-5">Outras Opções</h2>
                        <div className="flex flex-col md:flex-row gap-4">
                            {/* Botão para Criar Novo Lab */}
                            <button
                                onClick={openModal}
                                className="flex-1 flex items-center justify-center gap-2 px-5 py-3 bg-gray-800 text-gray-200 rounded-md font-semibold hover:bg-green-600 hover:text-white transition-all duration-300"
                            >
                                <FiPlus />
                                Criar Novo Lab
                            </button>
                            
                            {/* Formulário para Entrar com ID */}
                            <div className="flex-1 flex items-center gap-2">
                                <input
                                    type="text"
                                    placeholder="Ou insira um ID de Lab"
                                    value={manualLabId}
                                    onChange={(e) => setManualLabId(e.target.value)}
                                    className="w-full px-4 py-3 border border-gray-700 bg-gray-900/50 text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                />
                                <button
                                    onClick={handleManualLabEntry}
                                    className="p-3.5 bg-gray-800 text-gray-300 rounded-md font-semibold hover:bg-blue-600 hover:text-white transition-all"
                                >
                                    <FiArrowRight size={20} />
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </main>

            {/* Modal para Criação de Lab */}
            <Modal
                isOpen={isModalOpen}
                onRequestClose={closeModal}
                contentLabel="Criar Novo Lab"
                className={`modal-content ${cardBg} p-8 rounded-lg shadow-2xl max-w-md w-full text-white border border-gray-700 outline-none`}
                overlayClassName="modal-overlay fixed inset-0  bg-opacity-75 flex items-center justify-center p-4"
            >
                <div className="flex justify-between items-center mb-6">
                    <h2 className="text-2xl font-bold">Criar Novo Lab</h2>
                    <button onClick={closeModal} className="text-gray-500 hover:text-white transition-colors">
                        <FiX size={24} />
                    </button>
                </div>
                <form onSubmit={handleCreateLab} className="flex flex-col gap-5">
                    <input
                        type="text"
                        placeholder="ID do Lab (ex: efase01)"
                        value={newLabData.lab_id}
                        onChange={(e) => setNewLabData({ ...newLabData, lab_id: e.target.value })}
                        className="w-full px-4 py-3 border border-gray-700 bg-gray-900/50 text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                    />
                    <input
                        type="text"
                        placeholder="Nome do Lab (ex: Laboratório 1)"
                        value={newLabData.lab_name}
                        onChange={(e) => setNewLabData({ ...newLabData, lab_name: e.target.value })}
                        className="w-full px-4 py-3 border border-gray-700 bg-gray-900/50 text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                    />
                    <input
                        type="text"
                        placeholder="Turmas (separadas por vírgula)"
                        value={newLabData.classes}
                        onChange={(e) => setNewLabData({ ...newLabData, classes: e.target.value })}
                        className="w-full px-4 py-3 border border-gray-700 bg-gray-900/50 text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                    />
                    <div className="flex justify-end gap-4 mt-4">
                        <button type="button" onClick={closeModal} className="px-5 py-2 bg-gray-700 text-gray-300 rounded-md hover:bg-gray-600 transition-all">
                            Cancelar
                        </button>
                        <button type="submit" className="flex items-center gap-2 px-5 py-2 bg-blue-600 text-white rounded-md font-semibold hover:bg-blue-700 transition-all">
                            Criar Lab
                        </button>
                    </div>
                </form>
            </Modal>
        </div>
    );
};

export default UserLabs;