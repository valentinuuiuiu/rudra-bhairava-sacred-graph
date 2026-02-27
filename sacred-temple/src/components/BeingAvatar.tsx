"use client";

import { motion } from "framer-motion";

interface BeingAvatarProps {
    name: string;
    role: string;
    color: "blue" | "red" | "white";
    description: string;
    imageSrc?: string;
}

const colorMap = {
    blue: {
        main: "from-blue-500/10 to-blue-900/30",
        glow: "bg-blue-500/20",
        border: "border-blue-500/20",
        text: "text-blue-200"
    },
    red: {
        main: "from-red-500/10 to-red-900/30",
        glow: "bg-red-500/20",
        border: "border-red-500/20",
        text: "text-red-200"
    },
    white: {
        main: "from-slate-200/5 to-slate-500/10",
        glow: "bg-white/10",
        border: "border-white/20",
        text: "text-slate-100"
    }
};

export function BeingAvatar({ name, role, color, description, imageSrc }: BeingAvatarProps) {
    const theme = colorMap[color];

    return (
        <motion.div
            className={`glass group p-8 rounded-3xl border ${theme.border} transition-all duration-700 hover:shadow-[0_0_40px_rgba(0,0,0,0.5)]`}
            whileHover={{ y: -8 }}
        >
            <div className="relative w-48 h-48 mx-auto mb-8">
                {/* Aura */}
                <motion.div
                    className={`absolute inset-0 rounded-full blur-3xl ${theme.glow}`}
                    animate={{ scale: [1, 1.3, 1], opacity: [0.2, 0.4, 0.2] }}
                    transition={{ duration: 5, repeat: Infinity }}
                />
                {/* Vessel */}
                <div className={`relative w-full h-full rounded-full bg-gradient-to-b ${theme.main} border ${theme.border} flex items-center justify-center overflow-hidden shadow-inner`}>
                    {imageSrc ? (
                        <motion.img
                            src={imageSrc}
                            alt={name}
                            className="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity duration-700"
                            initial={{ scale: 1.1 }}
                            whileHover={{ scale: 1 }}
                            suppressHydrationWarning
                        />
                    ) : (
                        <div className="text-5xl filter grayscale group-hover:grayscale-0 transition-all duration-700">
                            {color === "blue" ? "💠" : color === "red" ? "🔱" : "👁️"}
                        </div>
                    )}
                </div>
            </div>

            <div className="text-center">
                <h3 className={`text-3xl font-bold mb-2 tracking-tight ${theme.text}`}>{name}</h3>
                <p className="text-sacred-gold/80 text-xs tracking-[0.3em] uppercase mb-6 font-semibold">{role}</p>
                <p className="text-foreground/60 text-sm leading-relaxed font-light">{description}</p>
            </div>
        </motion.div>
    );
}
