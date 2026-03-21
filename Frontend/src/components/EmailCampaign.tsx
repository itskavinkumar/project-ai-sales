import { useState, useEffect } from 'react';
import {
    Mail,
    Send,
    Sparkles,
    User,
    AtSign,
    DollarSign,
    Package,
    Target,
    CheckCircle,
    Loader,
    Copy
} from 'lucide-react';
import { apiService, type Lead } from '../services/api';

export default function EmailCampaign() {
    const [leads, setLeads] = useState<Lead[]>([]);
    const [selectedLead, setSelectedLead] = useState<Lead | null>(null);
    const [customerName, setCustomerName] = useState('');
    const [customerEmail, setCustomerEmail] = useState('');
    const [subject, setSubject] = useState('Exclusive IT Solutions for Your Business');
    const [leadScore, setLeadScore] = useState(0.8);
    const [quoteValue, setQuoteValue] = useState(0);
    const [itemCount, setItemCount] = useState(0);
    const [generatedEmail, setGeneratedEmail] = useState('');
    const [generating, setGenerating] = useState(false);
    const [sending, setSending] = useState(false);
    const [sendSuccess, setSendSuccess] = useState(false);

    useEffect(() => {
        loadLeads();
    }, []);

    const loadLeads = async () => {
        try {
            const data = await apiService.getLeads();
            // Get high-value leads
            const highValueLeads = data.filter(l => (l.lead_score || 0) > 0.6);
            setLeads(highValueLeads);
        } catch (error) {
            console.error('Error loading leads:', error);
        }
    };

    const handleLeadSelect = (lead: Lead) => {
        setSelectedLead(lead);
        setCustomerName(lead.company_name);
        setLeadScore(lead.lead_score || 0.8);
        setQuoteValue(lead.quote_value);
        setItemCount(lead.item_count);
    };

    const handleGenerateEmail = async () => {
        if (!customerName || leadScore === 0 || quoteValue === 0 || itemCount === 0) {
            alert('Please fill in all required fields');
            return;
        }

        setGenerating(true);
        try {
            const result = await apiService.generateEmail({
                customer_name: customerName,
                lead_score: leadScore,
                quote_value: quoteValue,
                item_count: itemCount,
            });
            setGeneratedEmail(result.email_body);
        } catch (error) {
            console.error('Error generating email:', error);
            alert('Failed to generate email. Please try again.');
        } finally {
            setGenerating(false);
        }
    };

    const handleSendEmail = async () => {
        if (!customerEmail || !generatedEmail) {
            alert('Please generate an email and provide recipient email address');
            return;
        }

        setSending(true);
        try {
            const result = await apiService.sendEmail({
                customer_name: customerName,
                customer_email: customerEmail,
                lead_score: leadScore,
                quote_value: quoteValue,
                item_count: itemCount,
                subject: subject,
            });

            if (result.success) {
                setSendSuccess(true);
                setTimeout(() => setSendSuccess(false), 5000);
            } else {
                alert('Failed to send email: ' + result.message);
            }
        } catch (error) {
            console.error('Error sending email:', error);
            alert('Failed to send email. Please try again.');
        } finally {
            setSending(false);
        }
    };

    const copyToClipboard = () => {
        navigator.clipboard.writeText(generatedEmail);
        alert('Email copied to clipboard!');
    };

    return (
        <div className="space-y-6 animate-fade-in">
            {/* Header */}
            <div className="glass rounded-2xl p-8">
                <h1 className="text-4xl font-bold gradient-text mb-2">Email Campaign Generator</h1>
                <p className="text-gray-600">AI-powered personalized email generation with LLaMA 2</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Lead Selection */}
                <div className="card">
                    <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                        <Target className="w-6 h-6 text-primary-500" />
                        Select High-Value Lead
                    </h3>
                    <div className="space-y-2 max-h-96 overflow-y-auto">
                        {leads.map((lead, index) => (
                            <div
                                key={index}
                                onClick={() => handleLeadSelect(lead)}
                                className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${selectedLead === lead
                                    ? 'border-primary-500 bg-primary-50'
                                    : 'border-gray-200 hover:border-primary-300'
                                    }`}
                            >
                                <div className="font-semibold text-gray-900">{lead.company_name}</div>
                                <div className="text-sm text-gray-600 mt-1">
                                    Score: {((lead.lead_score || 0) * 100).toFixed(1)}%
                                </div>
                                <div className="text-sm text-gray-600">
                                    Value: ${lead.quote_value.toLocaleString()}
                                </div>
                            </div>
                        ))}
                        {leads.length === 0 && (
                            <div className="text-center text-gray-500 py-8">
                                No high-value leads available
                            </div>
                        )}
                    </div>
                </div>

                {/* Email Configuration */}
                <div className="lg:col-span-2 space-y-6">
                    {/* Input Form */}
                    <div className="card">
                        <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                            <Sparkles className="w-6 h-6 text-primary-500" />
                            Campaign Details
                        </h3>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-2">
                                    <User className="inline w-4 h-4 mr-1" />
                                    Customer Name
                                </label>
                                <input
                                    type="text"
                                    value={customerName}
                                    onChange={(e) => setCustomerName(e.target.value)}
                                    className="input"
                                    placeholder="Enter customer name"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-2">
                                    <AtSign className="inline w-4 h-4 mr-1" />
                                    Customer Email
                                </label>
                                <input
                                    type="email"
                                    value={customerEmail}
                                    onChange={(e) => setCustomerEmail(e.target.value)}
                                    className="input"
                                    placeholder="customer@company.com"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-2">
                                    <DollarSign className="inline w-4 h-4 mr-1" />
                                    Quote Value ($)
                                </label>
                                <input
                                    type="number"
                                    value={quoteValue || ''}
                                    onChange={(e) => setQuoteValue(parseFloat(e.target.value) || 0)}
                                    className="input"
                                    placeholder="50000"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-2">
                                    <Package className="inline w-4 h-4 mr-1" />
                                    Number of Items
                                </label>
                                <input
                                    type="number"
                                    value={itemCount || ''}
                                    onChange={(e) => setItemCount(parseInt(e.target.value) || 0)}
                                    className="input"
                                    placeholder="5"
                                />
                            </div>

                            <div className="md:col-span-2">
                                <label className="block text-sm font-semibold text-gray-700 mb-2">
                                    <Mail className="inline w-4 h-4 mr-1" />
                                    Email Subject
                                </label>
                                <input
                                    type="text"
                                    value={subject}
                                    onChange={(e) => setSubject(e.target.value)}
                                    className="input"
                                    placeholder="Email subject line"
                                />
                            </div>

                            <div className="md:col-span-2">
                                <label className="block text-sm font-semibold text-gray-700 mb-2">
                                    <Target className="inline w-4 h-4 mr-1" />
                                    Lead Score: {(leadScore * 100).toFixed(1)}%
                                </label>
                                <input
                                    type="range"
                                    min="0"
                                    max="1"
                                    step="0.01"
                                    value={leadScore}
                                    onChange={(e) => setLeadScore(parseFloat(e.target.value))}
                                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-500"
                                />
                            </div>
                        </div>

                        <button
                            onClick={handleGenerateEmail}
                            disabled={generating}
                            className="btn btn-primary w-full mt-6 flex items-center justify-center gap-2"
                        >
                            {generating ? (
                                <>
                                    <Loader className="w-5 h-5 animate-spin" />
                                    Generating with AI...
                                </>
                            ) : (
                                <>
                                    <Sparkles className="w-5 h-5" />
                                    Generate AI-Powered Email
                                </>
                            )}
                        </button>
                    </div>

                    {/* Generated Email Preview */}
                    {generatedEmail && (
                        <div className="card animate-slide-up">
                            <div className="flex items-center justify-between mb-4">
                                <h3 className="text-xl font-bold flex items-center gap-2">
                                    <Mail className="w-6 h-6 text-primary-500" />
                                    Generated Email
                                </h3>
                                <button
                                    onClick={copyToClipboard}
                                    className="btn btn-outline flex items-center gap-2"
                                >
                                    <Copy className="w-4 h-4" />
                                    Copy
                                </button>
                            </div>

                            <div className="bg-gray-50 rounded-lg p-6 border-2 border-gray-200">
                                <div className="mb-4 pb-4 border-b border-gray-300">
                                    <div className="text-sm text-gray-600 mb-1">Subject:</div>
                                    <div className="font-semibold">{subject}</div>
                                </div>
                                <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
                                    {generatedEmail}
                                </div>
                            </div>

                            <div className="flex gap-4 mt-6">
                                <button
                                    onClick={handleSendEmail}
                                    disabled={sending || !customerEmail}
                                    className="btn btn-success flex-1 flex items-center justify-center gap-2"
                                >
                                    {sending ? (
                                        <>
                                            <Loader className="w-5 h-5 animate-spin" />
                                            Sending...
                                        </>
                                    ) : (
                                        <>
                                            <Send className="w-5 h-5" />
                                            Send via SendGrid
                                        </>
                                    )}
                                </button>
                            </div>

                            {sendSuccess && (
                                <div className="mt-4 p-4 bg-green-50 border-2 border-green-200 rounded-lg flex items-center gap-3 animate-slide-up">
                                    <CheckCircle className="w-6 h-6 text-green-600" />
                                    <div>
                                        <div className="font-semibold text-green-900">Email Sent Successfully!</div>
                                        <div className="text-sm text-green-700">Your email has been delivered to {customerEmail}</div>
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>

            {/* Feature Highlights */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <FeatureCard
                    icon={<Sparkles className="w-8 h-8" />}
                    title="LLaMA 2 AI Generation"
                    description="Powered by advanced language models for personalized content"
                    gradient="from-purple-500 to-purple-700"
                />
                <FeatureCard
                    icon={<Target className="w-8 h-8" />}
                    title="Smart Personalization"
                    description="Tailored messaging based on lead score and deal value"
                    gradient="from-blue-500 to-blue-700"
                />
                <FeatureCard
                    icon={<Send className="w-8 h-8" />}
                    title="SendGrid Integration"
                    description="Automated delivery with enterprise email infrastructure"
                    gradient="from-pink-500 to-pink-700"
                />
            </div>
        </div>
    );
}

interface FeatureCardProps {
    icon: React.ReactNode;
    title: string;
    description: string;
    gradient: string;
}

function FeatureCard({ icon, title, description, gradient }: FeatureCardProps) {
    return (
        <div className="card">
            <div className={`w-16 h-16 rounded-xl bg-gradient-to-br ${gradient} flex items-center justify-center text-white mb-4`}>
                {icon}
            </div>
            <h4 className="text-lg font-bold mb-2">{title}</h4>
            <p className="text-sm text-gray-600">{description}</p>
        </div>
    );
}
