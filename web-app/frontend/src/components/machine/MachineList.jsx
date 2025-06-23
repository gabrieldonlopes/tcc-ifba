import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { toast, ToastContainer } from 'react-toastify'; // Recomendo para mostrar erros

// API
import { get_machines_for_lab } from '../../api/api_lab.js'; // Ajuste o caminho para sua API

// Componentes
import Header from '../Header.jsx'; 

// Ícones
import { FiCpu, FiCalendar, FiWind, FiServer, FiAlertCircle } from 'react-icons/fi';

// O componente MachineCard não precisa de alterações, pois vamos adaptar os dados antes de passá-los.
const MachineCard = ({ machine }) => {
    const cardBg = "bg-[#161D27]";
    return (
        <Link 
            // A chave única da máquina será usada como ID na rota
            to={`/maquina/${machine.key}`} 
            className={`${cardBg} p-5 rounded-lg border border-gray-800 hover:border-blue-600 
                        transition-all duration-300 flex flex-col justify-between group`}
        >
            <div>
                <div className="flex justify-between items-start mb-4">
                    <h3 className="text-white font-bold text-xl">{machine.name}</h3>
                </div>
                
                <ul className="space-y-3 text-gray-300">
                    {/* Opcional: Adicionar um ícone para placa-mãe mesmo sem o dado */}
                    <li className="flex items-center gap-3">
                        <FiCpu size={20} className="text-gray-500" />
                        <span>{machine.motherboard || 'Não especificado'}</span>
                    </li>
                    <li className="flex items-center gap-3">
                        <FiCalendar size={20} className="text-gray-500" />
                        <span>Última Vistoria: {machine.lastInspection}</span>
                    </li>
                    <li className="flex items-center gap-3">
                        <FiWind size={20} className="text-gray-500" />
                        <span>Limpeza: {machine.cleaningStatus}</span>
                    </li>
                </ul>
            </div>
            <div className="text-center mt-5">
                <span className="text-blue-500 font-semibold text-sm opacity-0 group-hover:opacity-100 transition-opacity">
                    Ver Detalhes
                </span>
            </div>
        </Link>
    );
};

// --- Componente Principal da Página (Refatorado) ---
const MachineList = () => {
    const pageBg = "bg-[#0D1117]";
    const { lab_id } = useParams();

    // Estados para os dados, carregamento e erros
    const [machines, setMachines] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Função para buscar os dados
        const fetchMachines = async () => {
            try {
                setLoading(true);
                const data = await get_machines_for_lab(lab_id);
                setMachines(data);
            } catch (error) {
                console.error("Erro ao buscar máquinas:", error);
                toast.error(`Falha ao carregar máquinas do laboratório ${lab_id}.`);
            } finally {
                setLoading(false);
            }
        };

        fetchMachines();

    // A busca será refeita se o lab_id mudar
    }, [lab_id]);

    // Renderiza o estado de Carregamento
    if (loading) {
        return (
            <div className={`${pageBg} min-h-screen flex justify-center items-center text-white`}>
                <div className="text-center">
                     <div className="spinner-border animate-spin inline-block w-10 h-10 border-4 rounded-full" role="status"></div>
                    <p className="text-xl font-semibold mt-4">Carregando máquinas do {lab_id}...</p>
                </div>
            </div>
        );
    }

    return (
        <div className={`${pageBg} min-h-screen text-gray-200`}>
            <Header pageTitle={"Máquinas - " + lab_id} />
            
            
            <main className="container mx-auto p-6 pt-28 md:p-8 md:pt-28">
                {/* Verifica se há máquinas para exibir */}
                {machines.length > 0 ? (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                        {machines.map(apiMachine => (
                            // Mapeamos os dados da API para as props que o MachineCard espera
                            <MachineCard 
                                key={apiMachine.machine_key} 
                                machine={{
                                    key: apiMachine.machine_key,
                                    name: apiMachine.machine_name,
                                    lastInspection: apiMachine.last_checked,
                                    cleaningStatus: apiMachine.state_cleanliness,
                                    motherboard: apiMachine.motherboard // Se a API não envia, será 'undefined'
                                }}
                            />
                        ))}
                    </div>
                ) : (
                    // Mensagem para quando não há máquinas
                    <div className="text-center py-16 bg-[#161D27] rounded-lg flex flex-col items-center gap-4">
                        <FiServer size={40} className="text-blue-500" />
                        <h2 className="text-2xl font-bold text-white">Nenhuma Máquina Encontrada</h2>
                        <p className="text-gray-400">Não há máquinas cadastradas para o laboratório {lab_id}.</p>
                    </div>
                )}
            </main>
        </div>
    );
};

export default MachineList;