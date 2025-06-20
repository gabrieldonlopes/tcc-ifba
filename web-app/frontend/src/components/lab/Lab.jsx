import React, { useState, useEffect,useContext } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { get_lab } from '../../api/api_lab.js';
import { get_tasks_for_lab } from '../../api/api_lab.js';
import { get_sessions_for_lab } from '../../api/api_session.js';
import { toast, ToastContainer } from 'react-toastify';
import { AuthContext } from '../../contexts/AuthContext.jsx';
import Header from '../../components/Header.jsx'; 
import {
    FiPlus,
    FiHardDrive,
    FiFileText,
    FiUsers
} from 'react-icons/fi';

const ActionButton = ({ text, icon, colorClass, onClick }) => (
    <button 
        onClick={onClick} 
        className={`w-full flex items-center gap-4 p-4 rounded-lg bg-[#161D27] border border-transparent 
                    hover:bg-gray-800 hover:border-gray-700 transition-all duration-300`}
    >
        <div className={`p-2 rounded-md ${colorClass}`}>
            {icon}
        </div>
        <span className="font-bold text-gray-200">{text}</span>
    </button>
);

const Lab = () => {
    const pageBg = "bg-[#0D1117]";
    const cardBg = "bg-[#161D27]";
    const { token } = useContext(AuthContext);
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [pendingTasks, setPendingTasks] = useState([]);
    const [lab, setLab] = useState(null);
    const { lab_id } = useParams();
    const [sessions, setSessions] = useState([]);

    const labData = {
        lab_name: lab?.lab_name || "",
        classes: lab?.classes.join(",") || "",
        students: lab?.student_count || "",
        machines: lab?.machine_count || "",
        technicians: lab?.user_count || "",
        newTasks: lab?.task_count || "",
    };

    const handleNavigateToMachines = () => navigate(`/lab/${lab_id}/machines`);
    const handleNavigateToStudents = () => navigate(`/lab/${lab_id}/students`);
    const handleNavigateToTasks = () => navigate(`/lab/${lab_id}/tasks`);

    useEffect(() => {
        const fetchLab = async () => {
          try {
            const data = await get_lab(lab_id);
            setLab(data);
            const allTasks = await get_tasks_for_lab(token, lab_id);
            const pendings = allTasks.filter(task => !task.is_complete).slice(0, 5);
            setPendingTasks(pendings);
            const sessionsData = await get_sessions_for_lab(lab_id);
            setSessions(sessionsData.slice(0, 5));
          } catch (error) {
            toast.error("Erro ao carregar a lab, tarefas ou sessões.");
          } finally {
            setLoading(false);
          }
        };
        fetchLab();
      }, [lab_id, token]);

    const formatSessionStart = (start) => {
        if (!start) return "";
        const [date, time] = start.split(" ");
        const [hh, mm] = time.split(":");
        return `${date} - ${hh}:${mm}`;
    };

    if (loading) {
        return (
            <div className="min-h-screen flex justify-center items-center">
                <div className="text-center">
                    <div className="spinner-border animate-spin inline-block w-12 h-12 border-4 border-t-4 border-blue-500 rounded-full" role="status"></div>
                    <p className="text-2xl font-semibold mt-4 text-white">Carregando informações do lab...</p>
                </div>
            </div>
        );
    }

    return (
        <div className={`min-h-screen flex ${pageBg}`}>
          <Header pageTitle={labData.lab_name} />
          <ToastContainer position="bottom-right" autoClose={3000} />
    
          <main className="container mx-auto p-6 pt-28 md:p-8 md:pt-28 flex flex-1 gap-8">
            {/* Barra lateral: botões + tarefas pendentes */}
            <aside className="w-full max-w-xs flex flex-col gap-6">
              <div className="flex flex-col gap-y-5">
                <ActionButton
                  text="Estudantes"
                  icon={<FiUsers size={22} className="text-white" />}
                  colorClass="bg-blue-500/80"
                  onClick={handleNavigateToStudents}
                />
                <ActionButton
                  text="Máquinas"
                  icon={<FiHardDrive size={22} className="text-white" />}
                  colorClass="bg-green-600/80"
                  onClick={handleNavigateToMachines}
                />
                <ActionButton
                  text="Tarefas"
                  icon={<FiFileText size={22} className="text-white" />}
                  colorClass="bg-yellow-600/80"
                  onClick={handleNavigateToTasks}
                />
              </div>

              {/* Painel Tarefas Pendentes */}
              <div className={`${cardBg} p-6 rounded-lg flex flex-col flex-grow`}>
                <h3 className="text-xl text-white font-bold mb-4 border-b border-gray-700 pb-2">
                  Tarefas Pendentes
                </h3>
                {pendingTasks.length > 0 ? (
                  <ul className="flex flex-col gap-3 overflow-y-auto max-h-[300px]">
                    {pendingTasks.map((task) => (
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
            </aside>
    
            {/* Conteúdo principal */}
            <section className="flex-1 flex flex-col gap-y-8">
              {/* Dados do Lab */}
              <div className={`${cardBg} p-6 rounded-lg`}>
                <ul className="space-y-5 text-gray-300">
                  <li className="flex justify-between items-center text-lg">
                    <span>
                      Estudantes Ativos{" "}
                      <span className="text-sm text-gray-600">- {labData.classes}</span>
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
    
              {/* Card Histórico de Uso (Sessões) */}
              <div className={`${cardBg} p-6 rounded-lg`}>
                <h3 className="text-xl text-white font-bold mb-4">Histórico de Uso</h3>
                <table className="w-full text-gray-200 table-fixed border-collapse border border-gray-600">
                  <thead>
                    <tr className="bg-gray-700">
                      <th className="p-2 border border-gray-600 text-left">Estudante</th>
                      <th className="p-2 border border-gray-600 text-left">Horário</th>
                      <th className="p-2 border border-gray-600 text-left">Máquina</th>
                      <th className="p-2 border border-gray-600 text-left">Classe</th>
                    </tr>
                  </thead>
                  <tbody>
                    {sessions.length > 0 ? (
                      sessions.map((session, idx) => (
                        <tr key={idx} className="even:bg-gray-800 odd:bg-gray-700">
                          <td className="p-2 border border-gray-600">{session.student_name}</td>
                          <td className="p-2 border border-gray-600">{formatSessionStart(session.session_start)}</td>
                          <td className="p-2 border border-gray-600">{session.machine_name}</td>
                          <td className="p-2 border border-gray-600">{session.class_var}</td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan={4} className="text-center p-4 text-gray-400">
                          Nenhuma sessão encontrada.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </section>
          </main>
        </div>
    );
};

export default Lab;
