import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { get_lab } from '../../api/api_lab.js';
import { toast, ToastContainer } from 'react-toastify';
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
const ActionButton = ({ text, icon, colorClass }) => (
    <button 
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
const Lab = () => {
    // Estilo de Fundo da Página (mais escuro como na imagem)
    const pageBg = "bg-[#0D1117]";
    // Estilo do Fundo dos Cards (tom azulado escuro)
    const cardBg = "bg-[#161D27]";

    const navigate = useNavigate();

    const [lab, setLab] = useState(null);
    const { lab_id } = useParams();
    const labData = {
        lab_name: lab?.lab_name,
        classes: lab?.classes,
        students: lab?.student_count,
        machines: lab?.machine_count,
        technicians: lab?.user_count,
        newTasks: 2,
    };

    useEffect(() => {
        const fetchLab = async () => {
            try {
                const data = await get_lab(lab_id);
                setLab(data);
            } catch (error) {
                toast.error("Erro ao carregar a lab:", error);
            }
        };
        fetchLab();
    },[lab_id]);

    return (
        <div className={`min-h-screen `}>
            <Header pageTitle={labData.lab_name} />
            <ToastContainer position="bottom-right" autoClose={3000} />
            

            {/* Container principal com padding para o header fixo */}
            <main className="container mx-auto p-6 pt-28 md:p-8 md:pt-28">
                
                {/* Layout de duas colunas */}
                <div className="flex flex-col md:flex-row gap-8">

                    {/* Coluna da Esquerda (Ações) */}
                    <aside className="w-full md:w-64 flex flex-col gap-y-5">
                        <button className="w-full flex items-center gap-3 bg-blue-600 text-white p-4 rounded-lg font-bold text-lg hover:bg-blue-700 transition-colors">
                            <FiPlus size={22} />
                            Nova Tarefa
                        </button>
                        <ActionButton 
                            text="Estudantes" 
                            icon={<FiUsers size={22} className="text-white"/>} 
                            colorClass="bg-blue-500/80" 
                        />
                        <ActionButton 
                            text="Máquinas" 
                            icon={<FiHardDrive size={22} className="text-white"/>} 
                            colorClass="bg-green-600/80" 
                        />
                        <ActionButton 
                            text="Tarefas" 
                            icon={<FiFileText size={22} className="text-white"/>}
                            colorClass="bg-yellow-600/80"
                        />
                    </aside>

                    {/* Coluna da Direita (Informações) */}
                    <section className="flex-1 flex flex-col gap-y-8">
                        
                        {/* Card de Dados do Laboratório */}
                        <div className={`${cardBg} p-6 rounded-lg`}>
                            <ul className="space-y-5 text-gray-300">
                                <li className="flex justify-between items-center text-lg">
                                    <span>Estudantes Ativos</span> 
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
                            <h3 className="text-xl text-white font-bold mb-4">Tarefas</h3>
                            <button className="w-full bg-yellow-600/20 border border-yellow-500/30 text-yellow-300 p-4 rounded-lg flex items-center justify-center gap-x-3 hover:bg-yellow-600/30 transition-all duration-300">
                                <FiAlertTriangle size={24} />
                                <span className="font-bold text-lg">Atualizar Licenças</span>
                            </button>
                        </div>
                    </section>
                </div>
            </main>
        </div>
    );
};

export default Lab;