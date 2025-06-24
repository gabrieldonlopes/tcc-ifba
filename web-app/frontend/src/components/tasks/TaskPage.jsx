import React, { useEffect, useState, useContext } from 'react';
import { useParams } from 'react-router-dom';
import { toast, ToastContainer } from 'react-toastify';
import { FiCheckCircle, FiClipboard, FiPlus } from 'react-icons/fi';

import { AuthContext } from '../../contexts/AuthContext.jsx';
// Componentes
import Header from '../Header';
import CreateTaskModal from './CreateTaskModal.jsx';
// API
import { get_tasks_for_lab } from '../../api/api_lab';
import { create_new_task,complete_task } from '../../api/api_tasks.js';

const TaskCard = ({ task, onComplete, token }) => {
    const cardBg = "bg-[#161D27]";

    const handleCompleteTask = async (task_id) => {
        try {
            await complete_task(token, task_id);
            toast.success("Tarefa marcada como completa!");
            onComplete();  // Chama o callback para recarregar a lista
        } catch {
            toast.error("Erro ao completar tarefa.");
        }
    };

    return (
        <div
            className={`${cardBg} group relative p-5 rounded-lg border border-gray-800 hover:border-blue-600 transition-all duration-300`}
        >
            {/* Botão flutuante */}
            {!task.is_complete && (
                <button
                    onClick={() => handleCompleteTask(task.task_id)} // <- CORRIGIDO
                    className="absolute top-3 right-3 px-3 py-1 text-xs rounded-md bg-green-600 text-white opacity-0 group-hover:opacity-100 transition duration-300 shadow hover:bg-green-700 z-10"
                >
                    Completar
                </button>
            )}

            {/* Conteúdo da tarefa */}
            <div className="flex flex-col transition-opacity duration-300 group-hover:opacity-60">
                <div className="w-16 h-16 bg-blue-600/30 rounded-full flex items-center justify-center mb-4 border-2 border-blue-500/50">
                    <FiClipboard size={32} className="text-blue-300" />
                </div>

                <div className="flex-grow">
                    <h3 className="text-white font-bold text-xl truncate" title={task.task_name}>
                        {task.task_name}
                    </h3>
                    <p className="mt-2 text-sm text-gray-400 line-clamp-2">{task.task_description}</p>
                    <div className="mt-2 text-xs text-gray-500">Criado em: {task.task_creation}</div>

                    {task.machine_names?.length > 0 && (
                        <div className="mt-3">
                            <p className="text-xs font-semibold text-gray-300 mb-1">Máquinas:</p>
                            <ul className="text-xs text-gray-400 list-disc list-inside space-y-0.5 max-h-24 overflow-y-auto pr-1">
                                {task.machine_names.map((name, index) => (
                                    <li key={index}>{name}</li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>

                <div className="mt-4">
                    {task.is_complete ? (
                        <span className="text-green-500 font-semibold text-sm flex items-center gap-1">
                            <FiCheckCircle /> Concluída
                        </span>
                    ) : (
                        <span className="text-yellow-400 font-semibold text-sm">Pendente</span>
                    )}
                </div>
            </div>
        </div>
    );
};

const TaskPage = () => {
    const pageBg = "bg-[#0D1117]";
    const cardBg = "bg-[#161D27]";
    const { lab_id } = useParams();

    const { token } = useContext(AuthContext);
    const [tasks, setTasks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [modalOpen, setModalOpen] = useState(false);

    useEffect(() => {
        fetchTasks();
    }, [token, lab_id]);

    const fetchTasks = async () => {
        try {
            setLoading(true);
            const data = await get_tasks_for_lab(token,lab_id); // ajuste aqui conforme sua API
            setTasks(data);
        } catch (err) {
            console.error(err);
            toast.error("Erro ao carregar tarefas.");
        } finally {
            setLoading(false);
        }
    };

    const handleCreateTask = async (payload) => {
        try {
            // Chama a API para criar a nova tarefa
            toast.success("Tarefa criada com sucesso!");
            setModalOpen(false);
            fetchTasks();
        } catch (error) {
            console.error("Erro ao criar tarefa:", error);
            toast.error("Falha ao criar tarefa.");
        }
    };

    return (
        <div className={`${pageBg} min-h-screen text-gray-200`}>
            <Header pageTitle={`Tarefas - ${lab_id}`} />
            <ToastContainer position="bottom-right" autoClose={3000} />

            <main className="container mx-auto p-6 pt-28 md:p-8 md:pt-28">
            <div className={`${cardBg} p-6 rounded-2xl border border-gray-700 shadow-md mb-8`}>
                <div className="flex items-center justify-between">
                    <h2 className="text-xl font-bold text-gray-100">Gerenciar Tarefas</h2>
                    <button
                        onClick={() => setModalOpen(true)}
                        className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg shadow hover:bg-green-700 transition duration-200"
                    >
                        <FiPlus size={18} /> Nova Tarefa
                    </button>
                </div>
            </div>

                {loading ? (
                    <p className="text-center text-gray-400">Carregando tarefas...</p>
                ) : tasks.length > 0 ? (
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
                        {tasks
                        .slice() // cria uma cópia para não mutar o estado original
                        .sort((a, b) => a.is_complete - b.is_complete) // pendentes (false) primeiro
                        .map(task => (
                            <TaskCard key={task.task_id} task={task} onComplete={fetchTasks} token={token} />
                        ))}
                    </div>
                ) : (
                    <div className="text-center py-16 bg-[#161D27] rounded-lg">
                        <h2 className="text-2xl font-bold text-white mb-2">Nenhuma Tarefa Encontrada</h2>
                        <p className="text-gray-400">Não há tarefas cadastradas neste laboratório ({lab_id}).</p>
                    </div>
                )}
            </main>

            {modalOpen && (
                <CreateTaskModal
                    lab_id={lab_id}
                    token={token}
                    onClose={() => setModalOpen(false)}
                    onCreate={handleCreateTask}
                />
            )}
        </div>
    );
};

export default TaskPage;
