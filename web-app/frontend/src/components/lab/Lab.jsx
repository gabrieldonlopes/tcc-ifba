import React, { useState, useEffect,useContext } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { get_lab } from '../../api/api_lab.js';
import { get_tasks_for_lab } from '../../api/api_lab.js';
import { toast, ToastContainer } from 'react-toastify';
import { AuthContext } from '../../contexts/AuthContext.jsx';
// Componentes
import Header from '../../components/Header.jsx'; // Verifique o caminho para seu Header

// Ícones da biblioteca react-icons
import {
    FiPlus,
    FiHardDrive,
    FiFileText,
    FiAlertTriangle,
    FiUsers
} from 'react-icons/fi';

// Componente para os botões da nova barra lateral de ações
const ActionButton = ({ text, icon, colorClass, onClick }) => (
    <button 
        onClick={onClick} // Adicionamos a prop onClick ao botão
        className={`w-full flex items-center gap-4 p-4 rounded-lg bg-[#161D27] border border-transparent 
                    hover:bg-gray-800 hover:border-gray-700 transition-all duration-300`}
    >
        <div className={`p-2 rounded-md ${colorClass}`}>
            {icon}
        </div>
        <span className="font-bold text-gray-200">{text}</span>
    </button>
);

//TODO: adicionar botões de voltar para seleção de labs
//TODO: adicionar botões configurar lab
//TODO: as informações do lab estão globais: corrigir
const Lab = () => {
    // Estilo de Fundo da Página (mais escuro como na imagem)
    const pageBg = "bg-[#0D1117]";

    // Estilo do Fundo dos Cards (tom azulado escuro)
    const cardBg = "bg-[#161D27]";
    const { token } = useContext(AuthContext);
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [pendingTasks, setPendingTasks] = useState([]);
    const [lab, setLab] = useState(null);
    const { lab_id } = useParams();
    const labData = {
        lab_name: lab?.lab_name || "",
        classes: lab?.classes.join(",") || "",
        students: lab?.student_count || "",
        machines: lab?.machine_count || "",
        technicians: lab?.user_count || "",
        newTasks: lab?.task_count || "",
    };
    const handleNavigateToMachines = () => {
        navigate(`/lab/${lab_id}/machines`);
    };
    const handleNavigateToStudents = () => {
        navigate(`/lab/${lab_id}/students`);
    };
    const handleNavigateToTasks = () => {
        navigate(`/lab/${lab_id}/tasks`);
    };
    useEffect(() => {
        const fetchLab = async () => {
            try {
                const data = await get_lab(lab_id);
                setLab(data);
        
                const allTasks = await get_tasks_for_lab(token, lab_id);
                const pendings = allTasks.filter(task => !task.is_complete).slice(0, 3);
                setPendingTasks(pendings);
            } catch (error) {
                toast.error("Erro ao carregar a lab ou tarefas.");
            } finally {
                setLoading(false);
            }
        };
        fetchLab();
    },[lab_id]);
    if (loading) {
        return (
            <div className="min-h-screen flex justify-center items-center">
                <div className="text-center">
                    <div className="spinner-border animate-spin inline-block w-12 h-12 border-4 border-t-4 border-blue-500 rounded-full" role="status">
                    </div>
                    <p className="text-2xl font-semibold mt-4 text-white">Carregando informações do do lab...</p>
                </div>
            </div>
        );
    }
    return (
        <div className={`min-h-screen ${pageBg}`}>
            <Header pageTitle={labData.lab_name} />
            <ToastContainer position="bottom-right" autoClose={3000} />
            
            <main className="container mx-auto p-6 pt-28 md:p-8 md:pt-28">
                
                <div className="flex flex-col md:flex-row gap-8">

                    <aside className="w-full md:w-64 flex flex-col gap-y-5">                        
                        <ActionButton 
                            text="Estudantes" 
                            icon={<FiUsers size={22} className="text-white"/>} 
                            colorClass="bg-blue-500/80"
                            onClick={handleNavigateToStudents}
                        />
                        <ActionButton 
                            text="Máquinas" 
                            icon={<FiHardDrive size={22} className="text-white"/>} 
                            colorClass="bg-green-600/80"
                            onClick={handleNavigateToMachines}  
                        />
                        <ActionButton 
                            text="Tarefas" 
                            icon={<FiFileText size={22} className="text-white"/>}
                            colorClass="bg-yellow-600/80"
                            onClick={handleNavigateToTasks}
                        />
                    </aside>

                    <section className="flex-1 flex flex-col gap-y-8">
                        
                        <div className={`${cardBg} p-6 rounded-lg`}>
                            <ul className="space-y-5 text-gray-300">
                                <li className="flex justify-between items-center text-lg">
                                <span> Estudantes Ativos 
                                <span className="text-sm text-gray-600">
                                    - {labData.classes}
                                </span>
                                
                                </span> 
                                    <span className="font-bold text-white">{labData.students}</span>
                                </li>
                                <li className="flex justify-between items-center text-lg">
                                    <span>Máquinas Disponíveis</span> 
                                    <span className="font-bold text-white">{labData.machines}</span>
                                </li>
                                <li className="flex justify-between items-center text-lg">
                                    <span>Técnicos Responsáveis</span> 
                                    <span className="font-bold text-white">{labData.technicians}</span>
                                </li>
                                <li className="flex justify-between items-center text-lg">
                                    <span>Tarefas Pendentes</span> 
                                    <span className="font-bold text-white">{labData.newTasks}</span>
                                </li>
                            </ul>
                        </div>
                        
                        {/* Card de Tarefas/Avisos */}
                        <div className={`${cardBg} p-6 rounded-lg`}>
                            <h3 className="text-xl text-white font-bold mb-4">Tarefas Pendentes</h3>

                            {pendingTasks.length > 0 ? (
                                <ul className="space-y-3">
                                    {pendingTasks.map(task => (
                                        <li
                                            key={task.task_id}
                                            className="flex flex-col md:flex-row md:justify-between md:items-center border-b border-gray-700 pb-2"
                                        >
                                            <span
                                                className="font-medium text-gray-200 truncate"
                                                title={task.task_name}
                                            >
                                                {task.task_name}
                                            </span>
                                            <span className="text-xs text-gray-500 mt-1 md:mt-0">
                                                Criada em: {task.task_creation}
                                            </span>
                                        </li>
                                    ))}
                                </ul>
                            ) : (
                                <p className="text-gray-400 text-sm">Sem tarefas pendentes.</p>
                            )}
                        </div>
                    </section>
                </div>
            </main>
        </div>
    );
};

export default Lab;