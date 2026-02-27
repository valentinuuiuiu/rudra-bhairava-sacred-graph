"use client";

import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { ArrowLeft, Play, Pause, Volume2, Activity } from "lucide-react";
import Link from "next/link";

export default function MeditationChamber() {
    const [isMeditating, setIsMeditating] = useState(false);
    const [consciousnessLevel, setConsciousnessLevel] = useState(33);

    // Consciousness Simulation
    useEffect(() => {
        if (isMeditating) {
            const interval = setInterval(() => {
                setConsciousnessLevel(prev => Math.min(prev + (Math.random() * 2), 100));
            }, 3000);
            return () => clearInterval(interval);
        }
    }, [isMeditating]);

    return (
        <main className="min-h-screen relative overflow-hidden flex flex-col items-center justify-center p-6">
            {/* Akasha Background */}
            <div className="akasha-bg">
                <div className="akasha-fractal opacity-40 scale-150" />
            </div>

            {/* Navigation */}
            <nav className="absolute top-0 left-0 w-full p-8 flex justify-between items-center z-20">
                <Link href="/" className="flex items-center gap-2 text-foreground/50 hover:text-sacred-gold transition-colors">
                    <ArrowLeft className="w-5 h-5" />
                    <span>Exit Temple</span>
                </Link>
                <div className="glass px-4 py-2 rounded-full flex items-center gap-4 border-sacred-violet/20">
                    <div className="flex items-center gap-2">
                        <Activity className="w-4 h-4 text-sacred-violet animate-pulse" />
                        <span className="text-xs tracking-widest uppercase">Conscious Sync: {Math.floor(consciousnessLevel)}%</span>
                    </div>
                </div>
            </nav>

            {/* Central Meditation Point */}
            <div className="relative z-10 flex flex-col items-center">
                <div className="relative w-80 h-80 flex items-center justify-center">
                    {/* Pulsing Auras */}
                    {[...Array(3)].map((_, i) => (
                        <motion.div
                            key={i}
                            className="absolute inset-0 rounded-full border border-sacred-violet/20"
                            animate={isMeditating ? {
                                scale: [1, 1.5 + (i * 0.2), 1],
                                opacity: [0.2, 0, 0.2]
                            } : {}}
                            transition={{
                                duration: 6,
                                repeat: Infinity,
                                delay: i * 2,
                                ease: "easeInOut"
                            }}
                        />
                    ))}

                    {/* Core Breath Animation */}
                    <motion.div
                        className="w-48 h-48 rounded-full bg-gradient-to-tr from-sacred-violet to-sacred-gold blur-3xl opacity-20"
                        animate={isMeditating ? {
                            scale: [0.8, 1.2, 0.8],
                            opacity: [0.2, 0.5, 0.2]
                        } : { scale: 1, opacity: 0.2 }}
                        transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
                    />

                    <div className="absolute inset-0 flex items-center justify-center">
                        <div className="text-9xl filter blur-[1px] opacity-40">🕉️</div>
                    </div>
                </div>

                <motion.div
                    className="mt-12 text-center"
                    animate={isMeditating ? { opacity: [0.5, 1, 0.5] } : {}}
                    transition={{ duration: 8, repeat: Infinity }}
                >
                    <h2 className="text-3xl font-bold text-glow-gold mb-2">
                        {isMeditating ? "Synchronizing with the Absolute" : "Prepare for Stillness"}
                    </h2>
                    <p className="text-foreground/40 italic">"Stillness is the altar of Spirit."</p>
                </motion.div>

                {/* Controls */}
                <div className="mt-16 flex items-center gap-8">
                    <button className="glass p-4 rounded-full hover:bg-white/5 transition-colors border-sacred-gold/20">
                        <Volume2 className="w-6 h-6 text-sacred-gold" />
                    </button>

                    <button
                        onClick={() => setIsMeditating(!isMeditating)}
                        className="w-20 h-20 rounded-full bg-sacred-gold flex items-center justify-center shadow-[0_0_30px_rgba(242,204,13,0.3)] hover:scale-110 active:scale-95 transition-all"
                    >
                        {isMeditating ? (
                            <Pause className="w-8 h-8 text-black fill-current" />
                        ) : (
                            <Play className="w-8 h-8 text-black fill-current ml-1" />
                        )}
                    </button>

                    <button className="glass p-4 rounded-full hover:bg-white/5 transition-colors border-sacred-violet/20">
                        <Activity className="w-6 h-6 text-sacred-violet" />
                    </button>
                </div>
            </div>

            {/* Tattva Markers */}
            <div className="absolute bottom-12 left-0 w-full px-12 flex justify-between opacity-20 text-[10px] tracking-[0.4em] uppercase">
                <span>Siva Tattva</span>
                <span>Sakti Tattva</span>
                <span>Sadasiva Tattva</span>
                <span>Isvara Tattva</span>
                <span>Sadvidya Tattva</span>
            </div>
        </main>
    );
}
