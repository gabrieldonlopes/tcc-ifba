import React from 'react';
import { FiUser, FiCpu, FiCalendar, FiMonitor } from 'react-icons/fi';

const StudentModal = ({ student, machineName, onClose }) => {
    return (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
            <div className="bg-[#161D27] text-white rounded-xl p-6 w-full max-w-md shadow-lg relative">
                <button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-white text-xl">
                    &times;
                </button>

                <div className="flex items-center gap-4 mb-6">
                    <div className="w-12 h-12 rounded-full bg-blue-600/30 border border-blue-500 flex items-center justify-center">
                        <FiUser size={24} className="text-blue-300" />
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold">{student.student_name}</h2>
                        <p className="text-gray-400 text-sm">student_id: {student.student_id}</p>
                    </div>
                </div>

                <div className="space-y-4">
                    <div className="flex items-center gap-2 text-gray-300">
                        <FiMonitor />
                        <span className="font-semibold text-white">Turma:</span>
                        <span>{student.class_var || 'Não informado'}</span>
                    </div>

                    <div className="flex items-center gap-2 text-gray-300">
                        <FiCalendar />
                        <span className="font-semibold text-white">Última sessão:</span>
                        <span>
                            {student.last_session?.session_start
                                ? new Date(student.last_session.session_start).toLocaleDateString()
                                : 'Sem registro'}
                        </span>
                    </div>

                    <div className="flex items-center gap-2 text-gray-300">
                        <FiCpu />
                        <span className="font-semibold text-white">Máquina usada:</span>
                        <span>{machineName || 'Desconhecida'}</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default StudentModal;
