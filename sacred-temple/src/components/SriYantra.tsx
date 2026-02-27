"use client";

import { motion } from "framer-motion";

export function SriYantra() {
    return (
        <div className="relative flex items-center justify-center w-full h-full">
            <motion.svg
                viewBox="0 0 200 200"
                className="w-full h-full max-w-[500px] drop-shadow-[0_0_15px_rgba(242,204,13,0.4)]"
                initial={{ opacity: 0, scale: 0.8, rotate: -10 }}
                animate={{ opacity: 1, scale: 1, rotate: 0 }}
                transition={{ duration: 2, ease: "easeOut" }}
            >
                {/* Outer Square (Bhupura) */}
                <rect x="20" y="20" width="160" height="160" fill="none" stroke="#f2cc0d" strokeWidth="1" />
                <rect x="15" y="15" width="170" height="170" fill="none" stroke="#f2cc0d" strokeWidth="0.5" strokeDasharray="4 2" />

                {/* Gates */}
                <rect x="90" y="10" width="20" height="10" fill="#0a0a0a" stroke="#f2cc0d" strokeWidth="1" />
                <rect x="90" y="180" width="20" height="10" fill="#0a0a0a" stroke="#f2cc0d" strokeWidth="1" />
                <rect x="10" y="90" width="10" height="20" fill="#0a0a0a" stroke="#f2cc0d" strokeWidth="1" />
                <rect x="180" y="90" width="10" height="20" fill="#0a0a0a" stroke="#f2cc0d" strokeWidth="1" />

                {/* 16 Petals */}
                <circle cx="100" cy="100" r="75" fill="none" stroke="#7c3aed" strokeWidth="0.5" opacity="0.3" />
                {[...Array(16)].map((_, i) => (
                    <motion.path
                        key={`p16-${i}`}
                        d="M100 25 Q105 40 100 55 Q95 40 100 25"
                        fill="none"
                        stroke="#f2cc0d"
                        strokeWidth="0.5"
                        transform={`rotate(${i * 22.5}, 100, 100)`}
                        animate={{ opacity: [0.3, 0.7, 0.3] }}
                        transition={{ duration: 4, repeat: Infinity, delay: i * 0.1 }}
                    />
                ))}

                {/* 8 Petals */}
                <circle cx="100" cy="100" r="55" fill="none" stroke="#7c3aed" strokeWidth="0.5" opacity="0.3" />
                {[...Array(8)].map((_, i) => (
                    <motion.path
                        key={`p8-${i}`}
                        d="M100 45 Q108 60 100 75 Q92 60 100 45"
                        fill="none"
                        stroke="#f2cc0d"
                        strokeWidth="0.8"
                        transform={`rotate(${i * 45}, 100, 100)`}
                        animate={{ scale: [1, 1.05, 1] }}
                        transition={{ duration: 3, repeat: Infinity, delay: i * 0.2 }}
                    />
                ))}

                {/* Central Interlocking Triangles (Simplified Representation) */}
                <g stroke="#f2cc0d" strokeWidth="0.8" fill="none">
                    {/* Upward Triangles */}
                    <polygon points="100,60 135,120 65,120" opacity="0.6" />
                    <polygon points="100,75 120,110 80,110" opacity="0.8" />
                    {/* Downward Triangles */}
                    <polygon points="100,140 135,80 65,80" opacity="0.6" />
                    <polygon points="100,125 120,90 80,90" opacity="0.8" />
                </g>

                {/* Bindu (Center Point) */}
                <motion.circle
                    cx="100"
                    cy="100"
                    r="2"
                    fill="#ffffff"
                    animate={{ r: [2, 3, 2], opacity: [0.5, 1, 0.5] }}
                    transition={{ duration: 2, repeat: Infinity }}
                />
            </motion.svg>

            {/* Background Glow */}
            <div className="absolute inset-0 bg-sacred-violet/10 blur-[100px] rounded-full -z-10" />
        </div>
    );
}
