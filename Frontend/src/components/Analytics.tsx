import { useState, useEffect } from 'react';
import {
    TrendingUp,
    DollarSign,
    Users,
    Mail,
    Target,
    Activity,
    BarChart3
} from 'lucide-react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { apiService, type Lead } from '../services/api';

export default function Analytics() {
    const [leads, setLeads] = useState<Lead[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const data = await apiService.getLeads();
            setLeads(data);
        } catch (error) {
            console.error('Error loading data:', error);
        } finally {
            setLoading(false);
        }
    };

    // Performance metrics
    const performanceData = [
        { month: 'Jan', leads: 45, converted: 12, revenue: 245 },
        { month: 'Feb', leads: 52, converted: 18, revenue: 320 },
        { month: 'Mar', leads: 48, converted: 15, revenue: 280 },
        { month: 'Apr', leads: 61, converted: 22, revenue: 410 },
        { month: 'May', leads: 55, converted: 19, revenue: 350 },
        { month: 'Jun', leads: 67, converted: 28, revenue: 520 },
    ];

    // Lead quality radar
    const qualityMetrics = [
        { metric: 'Response Rate', value: 85 },
        { metric: 'Engagement', value: 72 },
        { metric: 'Deal Size', value: 68 },
        { metric: 'Close Rate', value: 45 },
        { metric: 'Speed to Close', value: 58 },
    ];

    // Conversion funnel
    const funnelData = [
        { stage: 'Total Leads', count: leads.length, percentage: 100 },
        { stage: 'Qualified', count: Math.floor(leads.length * 0.7), percentage: 70 },
        { stage: 'Engaged', count: Math.floor(leads.length * 0.45), percentage: 45 },
        { stage: 'Proposal', count: Math.floor(leads.length * 0.25), percentage: 25 },
        { stage: 'Closed', count: Math.floor(leads.length * 0.12), percentage: 12 },
    ];

    // Score distribution
    const scoreRanges = [
        { range: '0-20%', count: leads.filter(l => (l.lead_score || 0) < 0.2).length },
        { range: '20-40%', count: leads.filter(l => (l.lead_score || 0) >= 0.2 && (l.lead_score || 0) < 0.4).length },
        { range: '40-60%', count: leads.filter(l => (l.lead_score || 0) >= 0.4 && (l.lead_score || 0) < 0.6).length },
        { range: '60-80%', count: leads.filter(l => (l.lead_score || 0) >= 0.6 && (l.lead_score || 0) < 0.8).length },
        { range: '80-100%', count: leads.filter(l => (l.lead_score || 0) >= 0.8).length },
    ];

    const stats = [
        {
            title: 'Total Pipeline Value',
            value: `$${(leads.reduce((acc, l) => acc + l.quote_value, 0) / 1000).toFixed(0)}K`,
            change: '+12.5%',
            trend: 'up',
            icon: DollarSign,
            gradient: 'from-green-500 to-green-700',
        },
        {
            title: 'Average Deal Size',
            value: `$${(leads.reduce((acc, l) => acc + l.quote_value, 0) / leads.length / 1000).toFixed(1)}K`,
            change: '+8.3%',
            trend: 'up',
            icon: TrendingUp,
            gradient: 'from-blue-500 to-blue-700',
        },
        {
            title: 'Conversion Rate',
            value: '28.4%',
            change: '+5.2%',
            trend: 'up',
            icon: Target,
            gradient: 'from-purple-500 to-purple-700',
        },
        {
            title: 'Email Response Rate',
            value: '45.6%',
            change: '+3.1%',
            trend: 'up',
            icon: Mail,
            gradient: 'from-pink-500 to-pink-700',
        },
    ];

    if (loading) {
        return (
            <div className="flex items-center justify-center h-screen">
                <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-primary-500"></div>
            </div>
        );
    }

    return (
        <div className="space-y-6 animate-fade-in">
            {/* Header */}
            <div className="glass rounded-2xl p-8">
                <h1 className="text-4xl font-bold gradient-text mb-2">Analytics & Performance</h1>
                <p className="text-gray-600">Real-time insights and predictive metrics</p>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {stats.map((stat, index) => (
                    <div key={index} className="card group hover:scale-105">
                        <div className="flex items-start justify-between mb-4">
                            <div className={`p-3 rounded-xl bg-gradient-to-br ${stat.gradient} text-white group-hover:scale-110 transition-transform`}>
                                <stat.icon className="w-6 h-6" />
                            </div>
                            <span className={`text-sm font-semibold ${stat.trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
                                {stat.change}
                            </span>
                        </div>
                        <p className="text-sm font-medium text-gray-600 mb-1">{stat.title}</p>
                        <p className="text-3xl font-bold text-gray-900">{stat.value}</p>
                    </div>
                ))}
            </div>

            {/* Performance Trends */}
            <div className="card">
                <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                    <TrendingUp className="w-6 h-6 text-primary-500" />
                    6-Month Performance Trends
                </h3>
                <ResponsiveContainer width="100%" height={350}>
                    <LineChart data={performanceData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="month" />
                        <YAxis yAxisId="left" />
                        <YAxis yAxisId="right" orientation="right" />
                        <Tooltip />
                        <Legend />
                        <Line yAxisId="left" type="monotone" dataKey="leads" stroke="#6366f1" strokeWidth={3} name="Total Leads" />
                        <Line yAxisId="left" type="monotone" dataKey="converted" stroke="#10b981" strokeWidth={3} name="Converted" />
                        <Line yAxisId="right" type="monotone" dataKey="revenue" stroke="#ec4899" strokeWidth={3} name="Revenue ($K)" />
                    </LineChart>
                </ResponsiveContainer>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Lead Score Distribution */}
                <div className="card">
                    <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                        <BarChart3 className="w-6 h-6 text-primary-500" />
                        Lead Score Distribution
                    </h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={scoreRanges}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="range" />
                            <YAxis />
                            <Tooltip />
                            <Bar dataKey="count" fill="#6366f1" radius={[8, 8, 0, 0]} />
                        </BarChart>
                    </ResponsiveContainer>
                </div>

                {/* Lead Quality Radar */}
                <div className="card">
                    <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                        <Activity className="w-6 h-6 text-primary-500" />
                        Lead Quality Metrics
                    </h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <RadarChart data={qualityMetrics}>
                            <PolarGrid />
                            <PolarAngleAxis dataKey="metric" />
                            <PolarRadiusAxis angle={90} domain={[0, 100]} />
                            <Radar name="Performance" dataKey="value" stroke="#6366f1" fill="#6366f1" fillOpacity={0.6} />
                            <Tooltip />
                        </RadarChart>
                    </ResponsiveContainer>
                </div>
            </div>

            {/* Conversion Funnel */}
            <div className="card">
                <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                    <Target className="w-6 h-6 text-primary-500" />
                    Sales Conversion Funnel
                </h3>
                <div className="space-y-4">
                    {funnelData.map((stage, index) => (
                        <div key={index} className="relative">
                            <div className="flex items-center justify-between mb-2">
                                <span className="font-semibold text-gray-700">{stage.stage}</span>
                                <span className="text-sm text-gray-600">{stage.count} leads ({stage.percentage}%)</span>
                            </div>
                            <div className="relative h-12 bg-gray-100 rounded-lg overflow-hidden">
                                <div
                                    className="absolute inset-y-0 left-0 bg-gradient-to-r from-primary-500 to-primary-700 transition-all duration-500 flex items-center justify-center text-white font-semibold"
                                    style={{ width: `${stage.percentage}%` }}
                                >
                                    {stage.percentage > 20 && `${stage.percentage}%`}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Key Insights */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <InsightCard
                    icon={<TrendingUp className="w-8 h-8" />}
                    title="Top Insight"
                    description="High-value leads (>$50K) have 2.3x higher conversion rate"
                    gradient="from-green-500 to-green-700"
                />
                <InsightCard
                    icon={<Users className="w-8 h-8" />}
                    title="Customer Segment"
                    description="Enterprise IT companies show 45% faster decision-making"
                    gradient="from-blue-500 to-blue-700"
                />
                <InsightCard
                    icon={<Mail className="w-8 h-8" />}
                    title="AI Email Impact"
                    description="AI-generated emails achieve 38% better response rates"
                    gradient="from-purple-500 to-purple-700"
                />
            </div>
        </div>
    );
}

interface InsightCardProps {
    icon: React.ReactNode;
    title: string;
    description: string;
    gradient: string;
}

function InsightCard({ icon, title, description, gradient }: InsightCardProps) {
    return (
        <div className="card group hover:scale-105">
            <div className={`w-16 h-16 rounded-xl bg-gradient-to-br ${gradient} flex items-center justify-center text-white mb-4 group-hover:scale-110 transition-transform`}>
                {icon}
            </div>
            <h4 className="text-lg font-bold mb-2">{title}</h4>
            <p className="text-sm text-gray-600">{description}</p>
        </div>
    );
}
