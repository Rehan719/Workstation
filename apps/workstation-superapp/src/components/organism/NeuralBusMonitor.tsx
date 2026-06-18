import React, { useState, useEffect } from 'react';

interface NeuralEvent {
    id: string;
    type: string;
    source: string;
    timestamp: number;
    priority: number;
}

const priorityDot = (priority: number) => {
    if (priority === 1) return 'bg-red-500';
    if (priority <= 3) return 'bg-yellow-400';
    return 'bg-green-400';
};

const NeuralBusMonitor: React.FC = () => {
    const [events, setEvents] = useState<NeuralEvent[]>([]);
    const [isConnected, setIsConnected] = useState(false);

    useEffect(() => {
        const interval = setInterval(() => {
            const newEvent: NeuralEvent = {
                id: Math.random().toString(36).substr(2, 9),
                type: ['IntentGenerated', 'GovernanceValidated', 'ActionExecuted', 'HomeostasisEvent'][Math.floor(Math.random() * 4)],
                source: ['nematron', 'nemoclaw', 'openclaw', 'system'][Math.floor(Math.random() * 4)],
                timestamp: Date.now(),
                priority: Math.floor(Math.random() * 5) + 1
            };
            setEvents(prev => [newEvent, ...prev].slice(0, 50));
            setIsConnected(true);
        }, 2000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="p-5 bg-[#0a0a0a] text-white rounded-xl border border-[#333]">
            <div className="flex justify-between items-center mb-5">
                <h2 className="m-0 border-l-4 border-[#00d4ff] pl-4 text-lg font-bold">Neural Bus Monitor</h2>
                <div className="flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400 shadow-[0_0_8px_#4ade80]' : 'bg-red-500'}`} />
                    <span className="text-[10px] font-bold uppercase text-[#888]">
                        {isConnected ? 'libp2p Mesh Active' : 'Connecting...'}
                    </span>
                </div>
            </div>

            <div className="max-h-[400px] overflow-y-auto pr-2">
                <table className="w-full border-collapse text-xs">
                    <thead>
                        <tr className="text-left border-b border-[#333] text-[#888]">
                            <th className="p-2.5">ID</th>
                            <th className="p-2.5">TYPE</th>
                            <th className="p-2.5">SOURCE</th>
                            <th className="p-2.5">TIME</th>
                            <th className="p-2.5">P</th>
                        </tr>
                    </thead>
                    <tbody>
                        {events.map(event => (
                            <tr key={event.id} className="border-b border-[#222] transition-colors duration-200 hover:bg-white/5">
                                <td className="p-2.5 font-mono text-[#aaa]">{event.id}</td>
                                <td className="p-2.5 font-bold text-[#00d4ff]">{event.type}</td>
                                <td className="p-2.5 text-fuchsia-400">{event.source}</td>
                                <td className="p-2.5 text-[#888]">{new Date(event.timestamp).toLocaleTimeString()}</td>
                                <td className="p-2.5">
                                    <div className={`w-1.5 h-1.5 rounded-full ${priorityDot(event.priority)}`} />
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                {events.length === 0 && (
                    <p className="text-center py-10 text-[#555] italic">Awaiting neural signals...</p>
                )}
            </div>
        </div>
    );
};

export default NeuralBusMonitor;
