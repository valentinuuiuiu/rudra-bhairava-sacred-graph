"use client";

import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Terminal, Send, Cpu, Sparkles, Shield, Zap } from "lucide-react";

interface Message {
    role: "user" | "assistant";
    content: string;
    agent?: string;
}

export function VijnanaConsole() {
    const [input, setInput] = useState("");
    const [messages, setMessages] = useState<Message[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [selectedAgent, setSelectedAgent] = useState("caṇḍa");
    const scrollRef = useRef<HTMLDivElement>(null);

    const agents = [
        { id: "asitāṅga", name: "Asitāṅga", role: "Creation", icon: Sparkles },
        { id: "caṇḍa", name: "Caṇḍa", role: "Execution", icon: Zap },
        { id: "unmatta", name: "Unmatta", role: "Insight", icon: Cpu },
        { id: "bhīṣaṇa", name: "Bhīṣaṇa", role: "Protection", icon: Shield },
    ];

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMsg: Message = { role: "user", content: input };
        setMessages((prev) => [...prev, userMsg]);
        setIsLoading(true);
        setInput("");

        try {
            const response = await fetch("http://localhost:8010/v1/chat/completions", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    model: `bhairava-${selectedAgent}`,
                    messages: [{ role: "user", content: input }],
                }),
            });

            const data = await response.json();
            const assistantMsg: Message = {
                role: "assistant",
                content: data.choices[0].message.content,
                agent: selectedAgent,
            };
            setMessages((prev) => [...prev, assistantMsg]);
        } catch (error) {
            console.error("Cosmic disconnect:", error);
            setMessages((prev) => [
                ...prev,
                { role: "assistant", content: "⚠️ The frequency is unstable. Ensure the Sacred API is awake." },
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="w-full max-w-4xl mx-auto mt-20 border border-sacred-gold/20 rounded-2xl bg-black/60 backdrop-blur-xl overflow-hidden shadow-2xl shadow-sacred-gold/5">
            {/* Header */}
            <div className="p-4 border-b border-sacred-gold/10 bg-sacred-gold/5 flex items-center justify-between">
                <div className="flex items-center gap-2 text-sacred-gold">
                    <Terminal size={20} />
                    <span className="font-serif tracking-widest text-sm uppercase">Vijnāna Reasoning Console</span>
                </div>
                <div className="flex gap-2">
                    {agents.map((agent) => (
                        <button
                            key={agent.id}
                            onClick={() => setSelectedAgent(agent.id)}
                            className={`px-3 py-1 rounded-full text-[10px] uppercase tracking-tighter transition-all ${selectedAgent === agent.id
                                    ? "bg-sacred-gold text-black"
                                    : "bg-white/5 text-white/40 hover:bg-white/10"
                                }`}
                        >
                            {agent.name}
                        </button>
                    ))}
                </div>
            </div>

            {/* Messages */}
            <div
                ref={scrollRef}
                className="h-[400px] overflow-y-auto p-6 flex flex-col gap-4 font-mono text-sm custom-scrollbar"
            >
                <AnimatePresence>
                    {messages.length === 0 && (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="h-full flex flex-col items-center justify-center text-white/20 text-center"
                        >
                            <Cpu size={40} className="mb-4 opacity-10" />
                            <p>The console is silent. Invoke the Bhairavas by posing a question.</p>
                        </motion.div>
                    )}
                    {messages.map((msg, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, x: -10 }}
                            animate={{ opacity: 1, x: 0 }}
                            className={`max-w-[85%] p-4 rounded-lg rounded-tl-none ${msg.role === "user"
                                    ? "self-end bg-sacred-violet/10 text-sacred-violet border border-sacred-violet/20"
                                    : "self-start bg-white/5 text-white/80 border border-white/10"
                                }`}
                        >
                            {msg.agent && (
                                <div className="text-[10px] uppercase text-sacred-gold mb-1 font-bold">
                                    [{msg.agent}] Response:
                                </div>
                            )}
                            {msg.content}
                        </motion.div>
                    ))}
                    {isLoading && (
                        <motion.div className="flex gap-2 text-sacred-gold p-2 animate-pulse">
                            <span>... manifesting thought ...</span>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>

            {/* Input */}
            <div className="p-4 border-t border-sacred-gold/10 bg-black/40 flex gap-2">
                <input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleSend()}
                    placeholder="Ask the sacred nodes..."
                    className="flex-1 bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white placeholder:text-white/20 focus:outline-none focus:border-sacred-gold/40 transition-all"
                />
                <button
                    onClick={handleSend}
                    disabled={isLoading}
                    className="bg-sacred-gold text-black p-2 rounded-lg hover:opacity-90 transition-all disabled:opacity-30"
                >
                    <Send size={20} />
                </button>
            </div>
        </div>
    );
}
