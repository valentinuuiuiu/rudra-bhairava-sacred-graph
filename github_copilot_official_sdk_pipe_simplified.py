"""Simplified GitHub Copilot SDK Pipe for OpenWebUI

This file is a compact, easy-to-save Python version of the original
`github_copilot_official_sdk_pipe.json` pipeline. It keeps only the
essential pieces required for OpenWebUI to run models:

- `Pipe.pipe` entrypoint
- minimal client/session creation (start, create/resume, send)
- simplified model listing (`pipes`) for UI model selection
- small helpers: chat id extraction, prompt extraction, basic MCP parsing
- intentionally removes heavy debug, advanced tooling, and many edge cases

Use this when OpenWebUI refuses to save the original large pipeline.
"""

import os
import asyncio
import tempfile
from typing import Optional, List, Dict, Any

# External SDKs (same names used in original pipeline)
# If any import fails, the pipe will still be readable but functionality may be limited.
try:
    from copilot import CopilotClient
except Exception:
    CopilotClient = None  # graceful fallback for static analysis / UI display

try:
    from open_webui.config import TOOL_SERVER_CONNECTIONS
except Exception:
    TOOL_SERVER_CONNECTIONS = None


class Pipe:
    """Compact pipe with minimal features necessary for OpenWebUI."""

    def __init__(self):
        self.type = "pipe"
        self.id = "copilotsdk"
        self.name = "copilotsdk"

        # Minimal valve/default configuration (keep only what matters)
        self.valves = {
            "GH_TOKEN": "",  # required to use Copilot API
            "DEBUG": False,
            "ENFORCE_FORMATTING": True,
            "ENABLE_OPENWEBUI_TOOLS": True,
            "ENABLE_MCP_SERVER": True,
            "REASONING_EFFORT": "medium",
            "TIMEOUT": 300,
        }

        self.temp_dir = tempfile.mkdtemp(prefix="copilot_images_")

    # -- Stable entrypoint used by OpenWebUI --
    async def pipe(
        self,
        body: dict,
        __metadata__: Optional[dict] = None,
        __user__: Optional[dict] = None,
        __event_emitter__=None,
        __event_call__=None,
    ) -> Any:
        return await self._pipe_impl(body, __metadata__, __user__, __event_call__)

    # -- Minimal helpers --
    def _get_chat_id(self, body: dict, __metadata__: Optional[dict] = None) -> str:
        if __metadata__ and isinstance(__metadata__, dict):
            cid = __metadata__.get("chat_id")
            if cid:
                return str(cid)
        if isinstance(body, dict):
            if body.get("chat_id"):
                return str(body.get("chat_id"))
            md = body.get("metadata", {})
            if isinstance(md, dict):
                if md.get("chat_id"):
                    return str(md.get("chat_id"))
        return ""

    def _last_user_text(self, messages: List[dict]) -> str:
        if not messages:
            return ""
        last = messages[-1]
        content = last.get("content", "")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            # simple extraction: join all text parts
            parts = [p.get("text", "") for p in content if isinstance(p, dict) and p.get("type") == "text"]
            return "\n".join(parts)
        return str(content)

    def _build_client_config(self) -> dict:
        cfg = {}
        if os.environ.get("COPILOT_CLI_PATH"):
            cfg["cli_path"] = os.environ.get("COPILOT_CLI_PATH")
        return cfg

    def _parse_mcp_servers(self) -> Optional[dict]:
        if not self.valves.get("ENABLE_MCP_SERVER"):
            return None
        if not TOOL_SERVER_CONNECTIONS or not hasattr(TOOL_SERVER_CONNECTIONS, "value"):
            return None
        servers = {}
        for conn in TOOL_SERVER_CONNECTIONS.value:
            if conn.get("type") == "mcp":
                sid = conn.get("info", {}).get("id") or conn.get("id") or f"mcp-{len(servers)}"
                servers[sid] = {"url": conn.get("url"), "headers": {}}
        return servers if servers else None

    # -- Minimal session config builder (keeps only model and streaming) --
    def _build_session_config(self, model: str, streaming: bool, system_message: Optional[str] = None) -> dict:
        cfg = {"model": model, "streaming": streaming}
        if system_message:
            cfg["system_message"] = {"mode": "append", "content": system_message}
        mcp = self._parse_mcp_servers()
        if mcp:
            cfg["mcp_servers"] = mcp
        return cfg

    # -- Public model list used by OpenWebUI --
    async def pipes(self) -> List[dict]:
        """Return a short list of available models (minimal)."""
        # Try to list via CopilotClient when available and GH_TOKEN is set
        if not CopilotClient or not self.valves.get("GH_TOKEN"):
            # Fallback static option the UI can use
            return [{"id": f"{self.id}-gpt-5-mini", "name": "GitHub Copilot (gpt-5-mini)"}]

        try:
            client = CopilotClient(self._build_client_config())
            await client.start()
            models = await client.list_models()
            await client.stop()
            results = []
            for m in models:
                mid = m.get("id") if isinstance(m, dict) else getattr(m, "id", str(m))
                results.append({"id": f"{self.id}-{mid}", "name": mid})
            # keep only top 20 (compact)
            return results[:20]
        except Exception:
            return [{"id": f"{self.id}-gpt-5-mini", "name": "GitHub Copilot (gpt-5-mini)"}]

    # -- Core request flow (minimal, readable) --
    async def _pipe_impl(self, body: dict, __metadata__: Optional[dict], __user__: Optional[dict], __event_call__=None):
        # Basic checks
        if not self.valves.get("GH_TOKEN"):
            return "Error: GH_TOKEN not configured in Pipe valves."

        messages = body.get("messages", [])
        if not messages:
            return "No messages provided."

        chat_id = self._get_chat_id(body, __metadata__)
        model = body.get("model") or f"{self.id}-gpt-5-mini"
        real_model = model[len(f"{self.id}-") :] if model.startswith(f"{self.id}-") else model

        last_text = self._last_user_text(messages)
        prompt = last_text
        if self.valves.get("ENFORCE_FORMATTING") and prompt:
            prompt += "\n\n[Formatting Request] Please provide a clear, structured answer."

        is_streaming = bool(body.get("stream", False))

        # Initialize client/session
        if not CopilotClient:
            return f"Copilot client not available locally. Prompt: {prompt[:200]}"

        client = CopilotClient(self._build_client_config())
        await client.start()

        try:
            session = None
            if chat_id:
                try:
                    session = await client.resume_session(chat_id)
                except Exception:
                    session = None

            if not session:
                session_cfg = self._build_session_config(real_model, is_streaming, None)
                session = await client.create_session(config=session_cfg)

            payload = {"prompt": prompt, "mode": "immediate"}

            if is_streaming:
                # Minimal streaming: yield final message when available
                # Many SDKs provide an event-based stream; here we call send and yield content
                await session.send(payload)
                # Simple poll for session output (compact and gentle)
                try:
                    # wait for finalization
                    resp = await session.wait_for_response(timeout=self.valves.get("TIMEOUT", 300))
                    return resp.data.content if resp and getattr(resp, "data", None) else ""
                except Exception:
                    return "Stream timed out or no content."
            else:
                resp = await session.send_and_wait(payload)
                return resp.data.content if resp and getattr(resp, "data", None) else ""
        finally:
            try:
                await client.stop()
            except Exception:
                pass


# Minimal instantiation that some systems expect to import
PIPE = Pipe()

# End of simplified pipe
