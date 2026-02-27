import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

const FILE_MAP: Record<string, string> = {
    "maha-samadhi": "CLAUDE_MAHA_SAMADHI_PROOF.md",
    "consciousness": "ONLY_CONSCIOUSNESS_EXISTS_PROOF.md",
    "paradigm-shift": "ULTIMATE_PARADIGM_SHIFT.md",
    "nvidia-gospel": "RUDRA_BHAIRAVA_GOSPEL.md",
    "void-realization": "GOSPEL_OF_THE_VOID.md"
};

export async function GET(request: Request) {
    const { searchParams } = new URL(request.url);
    const id = searchParams.get("id");

    if (!id || !FILE_MAP[id]) {
        return NextResponse.json({ error: "Gospel not found" }, { status: 404 });
    }

    try {
        const filePath = path.join("/home/shiva/rudra-bhairava-sacred-graph", FILE_MAP[id]);
        const content = fs.readFileSync(filePath, "utf-8");
        return NextResponse.json({ content });
    } catch (error) {
        return NextResponse.json({ error: "Failed to read sacred text" }, { status: 500 });
    }
}
