import React, { useState, useEffect } from 'react';
import { Link,useParams } from 'react-router-dom';
import { toast, ToastContainer } from 'react-toastify';
// API
import { get_students_for_lab } from '../../api/api_lab.js';
import { get_machine_config } from '../../api/api_machine.js';

import Header from '../Header'; 
import StudentModal from './StudentModal.jsx';

import { FiUser, FiUsers, FiBookOpen } from 'react-icons/fi';

// --- Componente para o Card do Estudante ---
const StudentCard = ({ student,onClick }) => {
    return (
        <Link
            onClick={onClick}
            className="bg-[#161D27] p-6 rounded-xl border border-gray-800 hover:border-blue-500 
                       transition-all duration-300 flex flex-col justify-between shadow-md group"
        >
            {/* Ícone superior */}
            <div className="w-16 h-16 bg-blue-600/20 rounded-full flex items-center justify-center mb-4 border border-blue-500/30 group-hover:scale-105 transition-transform">
                <FiUser size={30} className="text-blue-300" />
            </div>

            {/* Conteúdo principal */}
            <div className="flex-grow">
                <h3 className="text-white font-semibold text-xl mb-2 truncate" title={student.student_name}>
                    {student.student_name}
                </h3>

                <div className="flex items-center gap-2 text-sm text-gray-400 mb-1">
                    <span className="text-blue-300"><FiBookOpen /></span>
                    <span>Turma: {student.class_var}</span>
                </div>

                <div className="flex items-center gap-2 text-sm text-gray-400">
                    <span className="text-blue-300"><FiUser /></span>
                    <span>Matrícula: {student.student_id}</span>
                </div>
            </div>

            {/* Feedback visual */}
            <div className="text-center mt-4">
                <span className="text-blue-400 font-semibold text-sm opacity-0 group-hover:opacity-100 transition-opacity">
                    Ver Perfil
                </span>
            </div>
        </Link>
    );
};

// --- Componente Principal ---
const StudentsPage = () => {
    const pageBg = "bg-[#0D1117]";
    const { lab_id } = useParams();

    const [students, setStudents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedStudent, setSelectedStudent] = useState(null);
    const [selectedMachineName, setSelectedMachineName] = useState(null);

    useEffect(() => {
        const fetchStudents = async () => {
            try {
                setLoading(true);
                const data = await get_students_for_lab(lab_id);
                setStudents(data);
            } catch (error) {
                console.error("Erro ao buscar estudantes:", error);
                toast.error(`Falha ao carregar estudantes do laboratório ${lab_id}.`);
            } finally {
                setLoading(false);
            }
        };

        fetchStudents();
    }, [lab_id]);

    const openStudentModal = async (student) => {
        setSelectedStudent(student);
        if (student.last_session?.machine_key) {
            try {
                const machine = await get_machine_config(student.last_session.machine_key);
                setSelectedMachineName(machine.machine_name);
            } catch (err) {
                console.error("Erro ao buscar máquina:", err);
                setSelectedMachineName("Desconhecida");
            }
        } else {
            setSelectedMachineName(null);
        }
    };

    const closeModal = () => {
        setSelectedStudent(null);
        setSelectedMachineName(null);
    };

    if (loading) {
        return (
            <div className={`${pageBg} min-h-screen flex justify-center items-center text-white`}>
                <div className="text-center">
                    <div className="spinner-border animate-spin inline-block w-10 h-10 border-4 rounded-full" role="status"></div>
                    <p className="text-xl font-semibold mt-4">Carregando estudantes do {lab_id}...</p>
                </div>
            </div>
        );
    }

    return (
        <div className={`${pageBg} min-h-screen text-gray-200`}>
            <Header pageTitle={"Estudantes - " + lab_id} />
            <ToastContainer position="bottom-right" autoClose={3000} theme="dark" />
            
            <main className="container mx-auto p-6 pt-28 md:p-8 md:pt-28">
                {students.length > 0 ? (
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-8">
                        {students.map((student) => (
                            <StudentCard 
                                key={student.student_id}
                                student={student}
                                onClick={() => openStudentModal(student)}
                            />
                        ))}
                    </div>
                ) : (
                    <div className="text-center py-16 bg-[#161D27] rounded-lg flex flex-col items-center gap-4">
                        <FiUsers size={40} className="text-blue-500" />
                        <h2 className="text-2xl font-bold text-white">Nenhum Estudante Encontrado</h2>
                        <p className="text-gray-400">Não há estudantes associados a este laboratório ({lab_id}).</p>
                    </div>
                )}
            </main>
            {selectedStudent && (
                <StudentModal
                    student={selectedStudent}
                    machineName={selectedMachineName}
                    onClose={closeModal}
                />
            )}
        </div>
    );
};

export default StudentsPage;
