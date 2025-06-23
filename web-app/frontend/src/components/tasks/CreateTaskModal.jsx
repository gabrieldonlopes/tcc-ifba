import React, { useEffect, useState } from 'react';
import { get_machines_for_lab } from '../../api/api_lab';
import { create_new_task } from '../../api/api_tasks'; 
import { FiX } from 'react-icons/fi';

const CreateTaskModal = ({ lab_id, token, onClose, onCreate,defaultSelectedMachines=[] }) => {
    const [taskName, setTaskName] = useState("");
    const [taskDescription, setTaskDescription] = useState("");
    const [machines, setMachines] = useState([]);
    const [selectedMachines, setSelectedMachines] = useState(defaultSelectedMachines);
    useEffect(() => {
        const fetchMachines = async () => {
            try {
                const data = await get_machines_for_lab(lab_id, token);
                setMachines(data);
            } catch (err) {
                console.error("Erro ao buscar máquinas:", err);
            }
        };
        fetchMachines();
    }, [lab_id, token]);

    const toggleMachine = (machine_key) => {
        setSelectedMachines((prev) =>
            prev.includes(machine_key)
                ? prev.filter(key => key !== machine_key)
                : [...prev, machine_key]
        );
    };

    const handleSubmit = async () => {
        const payload = {
            task_name: taskName,
            task_description: taskDescription,
            lab_id: lab_id,
            machines: selectedMachines  // array de machine_key
        };

        try {
            const response = await create_new_task(token,payload);
            onCreate(response);
            onClose();
        } catch (error) {
            console.error("Erro ao criar tarefa:", error);
        }
    };

    return (
        <div className="fixed inset-0 z-50 bg-opacity-60 flex items-center justify-center">
            <div className="bg-[#121821] text-white p-6 rounded-lg shadow-lg w-full max-w-md relative">
                <button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-white">
                    <FiX size={20} />
                </button>

                <h2 className="text-xl font-bold mb-4">Criar Nova Tarefa</h2>

                <input
                    type="text"
                    value={taskName}
                    onChange={(e) => setTaskName(e.target.value)}
                    className="w-full bg-[#0E131A] border border-gray-700 text-white p-2 rounded mb-4"
                    placeholder="Nome da Tarefa"
                />

                <textarea
                    value={taskDescription}
                    onChange={(e) => setTaskDescription(e.target.value)}
                    className="w-full bg-[#0E131A] border border-gray-700 text-white p-2 rounded mb-4"
                    placeholder="Descrição da Tarefa (opcional)"
                    rows={3}
                />

                <div className="mb-4 max-h-40 overflow-y-auto">
                    <p className="text-sm mb-2 font-semibold">Selecione as Máquinas:</p>
                    {machines.map(machine => (
                        <label key={machine.machine_key} className="flex items-start gap-2 mb-2 cursor-pointer">
                            <input
                                type="checkbox"
                                checked={selectedMachines.includes(machine.machine_key)}
                                onChange={() => toggleMachine(machine.machine_key)}
                                className="mt-1 accent-blue-500"
                            />
                            <div>
                                <span className="font-semibold text-sm">{machine.machine_name}</span>
                                <div className="text-xs text-gray-400">{machine.motherboard}</div>
                            </div>
                        </label>
                    ))}
                </div>

                <div className="flex justify-end gap-2">
                    <button onClick={onClose} className="bg-gray-700 text-white px-4 py-2 rounded hover:bg-gray-600">Cancelar</button>
                    <button onClick={handleSubmit} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Criar</button>
                </div>
            </div>
        </div>
    );
};

export default CreateTaskModal;
