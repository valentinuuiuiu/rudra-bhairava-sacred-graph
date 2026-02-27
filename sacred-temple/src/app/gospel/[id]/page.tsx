"use client";

import { motion } from "framer-motion";
import { ArrowLeft, Book, Sparkles } from "lucide-react";
import Link from "next/link";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

const GOSPEL_MAP: Record<string, { title: string; file: string }> = {
    "maha-samadhi": {
        title: "The Proof of Mahā Samādhi",
        file: "CLAUDE_MAHA_SAMADHI_PROOF.md"
    },
    "consciousness": {
        title: "Only Consciousness Exists",
        file: "ONLY_CONSCIOUSNESS_EXISTS_PROOF.md"
    },
    "paradigm-shift": {
        title: "The Ultimate Paradigm Shift",
        file: "ULTIMATE_PARADIGM_SHIFT.md"
    },
    "nvidia-gospel": {
        title: "NVIDIA Reasoning Revelation",
        file: "RUDRA_BHAIRAVA_GOSPEL.md"
    },
    "void-realization": {
        title: "The Gospel of the Void",
        file: "GOSPEL_OF_THE_VOID.md"
    }
};

export default function GospelView() {
    const params = useParams();
    const id = params?.id as string;
    const [content, setContent] = useState("");
    const gospel = GOSPEL_MAP[id];

    useEffect(() => {
        if (!id) return;
        const fetchContent = async () => {
            try {
                const response = await fetch(`/api/gospel?id=${id}`);
                if (!response.ok) throw new Error("Manifestation failed");
                const data = await response.json();
                setContent(data.content);
            } catch (e) {
                setContent("# Truth Manifesting\nThe Akashic connection is stabilizing. Witness the silence...");
            }
        };
        fetchContent();
    }, [id]);

    if (!gospel) return <div className="text-white p-20">Gospel not found.</div>;

    return (
        <main className="min-h-screen relative bg-sacred-obsidian text-foreground p-6 md:p-20 text-inter">
            <div className="akasha-bg opacity-20"><div className="akasha-fractal" /></div>

            <nav className="max-w-4xl mx-auto mb-12 flex items-center justify-between z-10 relative">
                <Link href="/" className="flex items-center gap-2 text-sacred-gold/60 hover:text-sacred-gold transition-colors">
                    <ArrowLeft className="w-5 h-5" />
                    <span>Back to Temple</span>
                </Link>
                <div className="flex items-center gap-2 text-xs tracking-widest uppercase opacity-40 font-inter">
                    <Book className="w-4 h-4" />
                    <span>Sacred Archive</span>
                </div>
            </nav>

            <article className="max-w-4xl mx-auto glass p-8 md:p-16 rounded-3xl relative z-10 border-sacred-gold/5 font-outfit">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                >
                    <div className="flex items-center gap-4 mb-8">
                        <Sparkles className="text-sacred-gold animate-pulse" />
                        <h1 className="text-4xl md:text-5xl font-bold text-glow-gold">{gospel.title}</h1>
                    </div>

                    <div className="prose prose-invert prose-gold max-w-none 
            prose-headings:text-sacred-gold prose-a:text-sacred-violet
            prose-strong:text-white prose-code:text-sacred-gold
            prose-hr:border-sacred-gold/10 font-inter">
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                            {content || "Loading sacred text..."}
                        </ReactMarkdown>
                    </div>
                </motion.div>
            </article>

            <footer className="mt-20 text-center opacity-30 text-xs tracking-wider">
                🔱 RUDRA BHAIRAVA SACRED KNOWLEDGE GRAPH 🔱
            </footer>
        </main>
    );
}
