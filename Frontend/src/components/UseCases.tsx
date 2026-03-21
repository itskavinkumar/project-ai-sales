import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import type { UseCase } from '../services/api';
import { BookOpen, Target, CheckCircle, ArrowRight, Loader } from 'lucide-react';

const UseCases: React.FC = () => {
    const [useCases, setUseCases] = useState<UseCase[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedIndustry, setSelectedIndustry] = useState<string>('All');

    useEffect(() => {
        loadUseCases();
    }, []);

    const loadUseCases = async () => {
        try {
            const data = await apiService.getUseCases();
            setUseCases(data);
        } catch (error) {
            console.error("Error loading use cases:", error);
        } finally {
            setLoading(false);
        }
    };

    const industries = ['All', ...Array.from(new Set(useCases.map(uc => uc.industry)))];

    const filteredUseCases = selectedIndustry === 'All'
        ? useCases
        : useCases.filter(uc => uc.industry === selectedIndustry);

    if (loading) {
        return (
            <div className="flex justify-center items-center h-64">
                <Loader className="w-8 h-8 text-blue-500 animate-spin" />
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                        Success Stories & Use Cases
                    </h2>
                    <p className="text-gray-500 mt-1">
                        Internal repository of solutions mapped to customer segments
                    </p>
                </div>

                <div className="flex items-center space-x-2">
                    <span className="text-sm font-medium text-gray-600">Filter by Industry:</span>
                    <select
                        value={selectedIndustry}
                        onChange={(e) => setSelectedIndustry(e.target.value)}
                        className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                    >
                        {industries.map(ind => (
                            <option key={ind} value={ind}>{ind}</option>
                        ))}
                    </select>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredUseCases.map((useCase) => (
                    <div key={useCase.id} className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 overflow-hidden group">
                        <div className="h-2 bg-gradient-to-r from-blue-500 to-purple-600 w-full" />
                        <div className="p-6">
                            <div className="flex justify-between items-start mb-4">
                                <span className={`px-3 py-1 rounded-full text-xs font-semibold 
                                    ${useCase.industry === 'Technology' ? 'bg-blue-100 text-blue-700' :
                                        useCase.industry === 'Healthcare' ? 'bg-green-100 text-green-700' :
                                            useCase.industry === 'Finance' ? 'bg-yellow-100 text-yellow-700' :
                                                'bg-gray-100 text-gray-700'}`}>
                                    {useCase.industry}
                                </span>
                                <BookOpen className="w-5 h-5 text-gray-400 group-hover:text-blue-500 transition-colors" />
                            </div>

                            <h3 className="text-lg font-bold text-gray-800 mb-2 group-hover:text-blue-600 transition-colors">
                                {useCase.title}
                            </h3>
                            <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                                {useCase.description}
                            </p>

                            <div className="space-y-3 mb-6">
                                <div>
                                    <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2 flex items-center">
                                        <Target className="w-3 h-3 mr-1" /> Pain Points
                                    </h4>
                                    <div className="flex flex-wrap gap-2">
                                        {useCase.pain_points.map((point, i) => (
                                            <span key={i} className="text-xs bg-red-50 text-red-600 px-2 py-1 rounded">
                                                {point}
                                            </span>
                                        ))}
                                    </div>
                                </div>

                                <div>
                                    <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1 flex items-center">
                                        <CheckCircle className="w-3 h-3 mr-1" /> Solution
                                    </h4>
                                    <p className="text-sm text-gray-700 bg-gray-50 p-2 rounded-lg border border-gray-100">
                                        {useCase.solution_summary}
                                    </p>
                                </div>

                                {useCase.success_metrics && (
                                    <div className="bg-green-50 rounded-lg p-2 border border-green-100">
                                        <p className="text-xs font-medium text-green-700 text-center">
                                            🚀 {useCase.success_metrics}
                                        </p>
                                    </div>
                                )}
                            </div>

                            <div className="pt-4 border-t border-gray-100 flex justify-between items-center">
                                <span className="text-xs text-gray-500">
                                    Map: {useCase.relevant_segments.slice(0, 2).join(", ")}
                                </span>
                                <button className="text-blue-600 hover:text-blue-800 text-sm font-medium flex items-center transition-colors">
                                    View Details <ArrowRight className="w-3 h-3 ml-1" />
                                </button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {filteredUseCases.length === 0 && (
                <div className="text-center py-12 bg-gray-50 rounded-xl border border-dashed border-gray-300">
                    <BookOpen className="mx-auto h-12 w-12 text-gray-400" />
                    <h3 className="mt-2 text-sm font-medium text-gray-900">No use cases found</h3>
                    <p className="mt-1 text-sm text-gray-500">Try selecting a different industry filter.</p>
                </div>
            )}
        </div>
    );
};

export default UseCases;
