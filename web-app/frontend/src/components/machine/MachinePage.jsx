import React, { useState, useEffect, useContext } from 'react';
import { useParams } from 'react-router-dom';
import { toast, ToastContainer } from 'react-toastify';
import { get_sessions_for_machine } from '../../api/api_session.js';
import {
  get_machine_config,
  update_last_check,
  update_state_cleanliness,
  get_tasks_for_machine,
} from '../../api/api_machine.js';
import { complete_task } from '../../api/api_tasks.js'; // importe essa função
import Header from '../../components/Header.jsx';
import { AuthContext } from '../../contexts/AuthContext.jsx';
import { FiPlus } from 'react-icons/fi';
import CreateTaskModal from '../tasks/CreateTaskModal.jsx';

const MachinePage = () => {
  const { machine_key } = useParams();
  const { token } = useContext(AuthContext);
  const [machineConfig, setMachineConfig] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newCheckDate, setNewCheckDate] = useState('');
  const [cleanlinessState, setCleanlinessState] = useState('');
  const [isUpdating, setIsUpdating] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
    
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;   
  const pageBg = "bg-[#0D1117]";
  const cardBg = "bg-[#161D27]";

  useEffect(() => {
    const fetchData = async () => {
      try {
        const config = await get_machine_config(machine_key);
        setMachineConfig(config);

        const sessionData = await get_sessions_for_machine(machine_key);
        setSessions(sessionData);

        const taskData = await get_tasks_for_machine(token, machine_key);
        setTasks(taskData);
      } catch (error) {
        toast.error("Erro ao carregar informações da máquina, sessões ou tarefas.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [machine_key, token]);

  // Função para recarregar tarefas (útil após criar ou completar)
  const reloadTasks = async () => {
    try {
      const taskData = await get_tasks_for_machine(token, machine_key);
      setTasks(taskData);
    } catch {
      toast.error("Erro ao recarregar tarefas.");
    }
  };

  // Função para lidar com criação de tarefa (passada para o modal)
  const handleCreateTask = (newTask) => {
    // Pode recarregar todas as tarefas, ou inserir a nova na lista local
    reloadTasks();
    setModalOpen(false);
    toast.success("Tarefa criada com sucesso!");
  };

  // Função para completar tarefa
  const handleCompleteTask = async (task_id) => {
    try {
      await complete_task(token, task_id);
      toast.success("Tarefa marcada como completa!");
      reloadTasks();
    } catch {
      toast.error("Erro ao completar tarefa.");
    }
  };

  const formatSessionStart = (start) => {
    if (!start) return "";
    const [date, time] = start.split(" ");
    const [hh, mm] = time.split(":");
    return `${date} - ${hh}:${mm}`;
  };

  const isValidDate = (dateStr) => {
    return /^\d{2}\/\d{2}\/\d{4}$/.test(dateStr);
  };

  const handleUpdateLastCheck = async () => {
    if (!isValidDate(newCheckDate)) {
      toast.error('Formato de data inválido. Use dd/mm/aaaa.');
      return;
    }

    setIsUpdating(true);
    try {
      await update_last_check(token, machine_key, { new_check: newCheckDate });
      toast.success('Data da última verificação atualizada.');
      setMachineConfig(prev => ({ ...prev, last_checked: newCheckDate }));
    } catch (err) {
      toast.error('Erro ao atualizar a data.');
    } finally {
      setIsUpdating(false);
    }
  };

  const handleUpdateCleanliness = async () => {
    setIsUpdating(true);
    try {
      await update_state_cleanliness(token, machine_key, { new_state: cleanlinessState });
      toast.success('Estado de limpeza atualizado.');
      setMachineConfig(prev => ({ ...prev, state_cleanliness: cleanlinessState }));
    } catch (err) {
      toast.error('Erro ao atualizar o estado de limpeza.');
    } finally {
      setIsUpdating(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex justify-center items-center">
        <div className="text-center">
          <div
            className="spinner-border animate-spin inline-block w-12 h-12 border-4 border-t-4 border-blue-500 rounded-full"
            role="status"
          ></div>
          <p className="text-2xl font-semibold mt-4 text-white">Carregando informações da máquina...</p>
        </div>
      </div>
    );
  }

  // Espera machineConfig antes de abrir modal para garantir lab_id
  const lab_id = machineConfig?.lab_id;

  return (
    <div className={`min-h-screen flex ${pageBg}`}>
      <Header pageTitle={machineConfig?.machine_name || "Máquina"} />
      <ToastContainer position="bottom-right" autoClose={3000} />

      <main className="container mx-auto p-6 pt-28 md:p-8 md:pt-28 flex flex-col gap-8">
        {/* Linha com Informações e Atualizações */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* Informações da máquina */}
          <section className={`${cardBg} p-6 rounded-lg`}>
            <h3 className="text-xl text-white font-bold mb-4">Informações da Máquina</h3>
            <div className="grid grid-cols-1 gap-3 text-gray-300">
              <div><span className="text-white font-semibold">Nome:</span> {machineConfig.machine_name}</div>
              <div><span className="text-white font-semibold">Placa-mãe:</span> {machineConfig.motherboard}</div>
              <div><span className="text-white font-semibold">Memória:</span> {machineConfig.memory}</div>
              <div><span className="text-white font-semibold">Armazenamento:</span> {machineConfig.storage}</div>
              <div><span className="text-white font-semibold">Estado de Limpeza:</span> {machineConfig.state_cleanliness}</div>
              <div><span className="text-white font-semibold">Última Verificação:</span> {machineConfig.last_checked}</div>
            </div>
          </section>

          {/* Atualizações Técnicas */}
          <section className={`${cardBg} p-6 rounded-lg`}>
            <h3 className="text-xl text-white font-bold mb-4">Atualizações Técnicas</h3>

            {/* Atualizar data da última verificação */}
            <div className="mb-4">
              <label className="block text-sm text-gray-300 mb-1">Nova data da verificação (dd/mm/aaaa):</label>
              <input
                type="text"
                className="w-full bg-gray-800 text-white p-2 rounded border border-gray-600"
                value={newCheckDate}
                onChange={e => setNewCheckDate(e.target.value)}
                placeholder="28/06/2025"
              />
              <button
                onClick={handleUpdateLastCheck}
                disabled={isUpdating}
                className="mt-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
              >
                Atualizar Verificação
              </button>
            </div>

            {/* Atualizar estado de limpeza */}
            <div>
              <label className="block text-sm text-gray-300 mb-1">Estado de Limpeza:</label>
              <select
                className="w-full bg-gray-800 text-white p-2 rounded border border-gray-600"
                value={cleanlinessState}
                onChange={e => setCleanlinessState(e.target.value)}
              >
                <option value="">Selecione</option>
                <option value="BOM">BOM</option>
                <option value="REGULAR">REGULAR</option>
                <option value="URGENTE">URGENTE</option>
              </select>
              <button
                onClick={handleUpdateCleanliness}
                disabled={isUpdating}
                className="mt-2 bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded"
              >
                Atualizar Estado
              </button>
            </div>
          </section>
        </div>

        <section className={`${cardBg} p-6 rounded-lg`}>
  <h3 className="text-xl text-white font-bold mb-4">Histórico de Sessões</h3>

  <table className="w-full text-gray-200 table-fixed border-collapse border border-gray-600">
    <thead>
      <tr className="bg-gray-700">
        <th className="p-2 border border-gray-600 text-left">Estudante</th>
        <th className="p-2 border border-gray-600 text-left">Horário</th>
        <th className="p-2 border border-gray-600 text-left">Classe</th>
        <th className="p-2 border border-gray-600 text-left">Uso CPU (%)</th>
        <th className="p-2 border border-gray-600 text-left">Uso RAM (%)</th>
        <th className="p-2 border border-gray-600 text-left">Temp. CPU (°C)</th>
      </tr>
    </thead>
    <tbody>
      {sessions.length > 0 ? (
        // calcula o índice inicial e final para a página atual
        sessions
          .slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage)
          .map((session, idx) => (
            <tr key={idx} className="even:bg-gray-800 odd:bg-gray-700">
              <td className="p-2 border border-gray-600">{session.student_name}</td>
              <td className="p-2 border border-gray-600">{formatSessionStart(session.session_start)}</td>
              <td className="p-2 border border-gray-600">{session.class_var}</td>
              <td className="p-2 border border-gray-600">{session.cpu_usage}%</td>
              <td className="p-2 border border-gray-600">{session.ram_usage}%</td>
              <td className="p-2 border border-gray-600">{session.cpu_temp}°C</td>
            </tr>
          ))
      ) : (
        <tr>
          <td colSpan={6} className="text-center p-4 text-gray-400">
            Nenhuma sessão encontrada.
          </td>
        </tr>
      )}
    </tbody>
    </table>

    {/* Paginação */}
    {sessions.length > itemsPerPage && (
    <div className="flex justify-center gap-2 mt-4">
      {/* Botão Página Anterior */}
      <button
        onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}
        disabled={currentPage === 1}
        className="px-3 py-1 bg-gray-700 rounded disabled:opacity-50"
      >
        Anterior
      </button>

      {/* Botões de página */}
      {[...Array(Math.ceil(sessions.length / itemsPerPage))].map((_, i) => {
        const pageNum = i + 1;
        return (
          <button
            key={pageNum}
            onClick={() => setCurrentPage(pageNum)}
            className={`px-3 py-1 rounded ${currentPage === pageNum ? "bg-blue-600" : "bg-gray-700"}`}
          >
            {pageNum}
          </button>
        );
      })}

      {/* Botão Próxima Página */}
      <button
        onClick={() => setCurrentPage((p) => Math.min(p + 1, Math.ceil(sessions.length / itemsPerPage)))}
        disabled={currentPage === Math.ceil(sessions.length / itemsPerPage)}
        className="px-3 py-1 bg-gray-700 rounded disabled:opacity-50"
      >
        Próxima
      </button>
    </div>
    )}
    </section>

        {/* Tarefas da máquina */}
        <section className={`${cardBg} p-6 rounded-lg`}>
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-gray-100">Tarefas da Máquina</h2>
            <button
              onClick={() => setModalOpen(true)}
              className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg shadow hover:bg-green-700 transition duration-200"
            >
              <FiPlus size={18} /> Nova Tarefa
            </button>
          </div>
          <ul className="space-y-3 text-gray-300 mt-4">
            {tasks.filter(task => !task.is_complete).length > 0 ? (
              tasks
                .filter(task => !task.is_complete)
                .map((task, index) => (
                  <li key={index} className="p-3 border border-gray-700 rounded bg-gray-800">
                    <div className="flex justify-between items-center">
                      <div>
                        <p className="text-white font-semibold">{task.task_name}</p>
                        {task.task_description && (
                          <p className="text-sm text-gray-400">{task.task_description}</p>
                        )}
                      </div>
                      <button
                        onClick={() => handleCompleteTask(task.task_id)}
                        className="ml-4 px-3 py-1 text-sm bg-green-600 hover:bg-green-700 text-white rounded"
                      >
                        Completar
                      </button>
                    </div>
                  </li>
                ))
            ) : (
              <p className="text-gray-400">Nenhuma tarefa associada a esta máquina.</p>
            )}
          </ul>
        </section>
      </main>

      {modalOpen && lab_id && (
        <CreateTaskModal
          lab_id={lab_id}
          token={token}
          defaultSelectedMachines={[machine_key]} 
          onClose={() => setModalOpen(false)}
          onCreate={handleCreateTask}
        />
      )}
    </div>
  );
};

export default MachinePage;
