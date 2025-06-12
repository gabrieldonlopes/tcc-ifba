import React, { useState, useEffect } from 'react';
// Importe o Link para ser usado no Card
import { Link, useParams } from 'react-router-dom';
import { toast, ToastContainer } from 'react-toastify';

// API
import { get_students_for_lab } from '../../api/api_lab.js'; 

// Componentes
import Header from '../Header'; 

// Ícones
import { FiUser, FiUsers, FiBookOpen } from 'react-icons/fi';

// --- Componente para o Card do Estudante (agora é um Link) ---
const StudentCard = ({ student }) => {
    const cardBg = "bg-[#161D27]";
    return (
        // O card inteiro agora é um Link que leva para a página do aluno
        <Link 
            to={`/aluno/${student.student_id}`}
            className={`${cardBg} p-5 rounded-lg border border-gray-800 hover:border-blue-600 
                        transition-all duration-300 flex flex-col group`}
        >
            <div className="w-16 h-16 bg-blue-600/30 rounded-full flex items-center justify-center mb-4 border-2 border-blue-500/50 group-hover:scale-105 transition-transform">
                <FiUser size={32} className="text-blue-300" />
            </div>
            
            <div className='flex-grow'>
                <h3 className="text-white font-bold text-xl truncate" title={student.student_name}>
                    {student.student_name}
                </h3>
                
                <div className="flex items-center gap-2 mt-2 text-gray-400">
                    <FiBookOpen size={16} />
                    <span>Turma: {student.class_var}</span>
                </div>
            </div>

            {/* Adiciona um feedback visual de "Ver Perfil" no hover */}
            <div className="text-center mt-4">
                <span className="text-blue-500 font-semibold text-sm opacity-0 group-hover:opacity-100 transition-opacity">
                    Ver Perfil
                </span>
            </div>
        </Link>
    );
};

// --- Componente Principal da Página (com a key corrigida) ---
const StudentsPage = () => {
    const pageBg = "bg-[#0D1117]";
    const { lab_id } = useParams();

    const [students, setStudents] = useState([]);
    const [loading, setLoading] = useState(true);

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

    // Renderiza o estado de Carregamento (sem alterações)
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
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
                        {students.map((student) => (
                            <StudentCard 
                                // ✅ CORREÇÃO: Usando o ID único do estudante como chave (key)
                                key={student.student_id} 
                                student={student}
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
        </div>
    );
};

export default StudentsPage;