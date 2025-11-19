# mcp_helpers.py
import time
import sys
import os
import uuid
import asyncio
import re
from typing import Any, Callable, Coroutine
from functools import wraps

# simple in-memory cache: {key: (ts, value)}
_CACHE: dict[str, tuple[float, Any]] = {}
CACHE_TTL = float(os.getenv("MCP_CACHE_TTL", "60"))  # seconds

# simple per-tool stats
TOOL_STATS: dict[str, dict[str, Any]] = {}

# rate limiting per-tool using semaphores (conservative)
_RATE_LIMITS: dict[str, asyncio.Semaphore] = {}

# correlation tracking: {correlation_id: {"tool": str, "start_time": float, "jsonrpc_id": str, ...}}
CORRELATION_CHAIN: dict[str, dict[str, Any]] = {}

# Secret patterns to redact from logs
SECRET_PATTERNS = [
    re.compile(r'(token|auth|password|secret|key|credential|bearer)[\'\"]?\s*[:=]\s*[\'\"]?([^\s\'"]+)', re.IGNORECASE),
    re.compile(r'(ghp_[a-zA-Z0-9]{36})', re.IGNORECASE),  # GitHub PAT
    re.compile(r'(gho_[a-zA-Z0-9]{36})', re.IGNORECASE),  # GitHub OAuth
    re.compile(r'(Bearer\s+[^\s]+)', re.IGNORECASE),
]

def redact_secrets(text: str) -> str:
    """Redact secrets from text using pattern matching."""
    for pattern in SECRET_PATTERNS:
        text = pattern.sub(r'\1=<REDACTED>', text)
    return text

def log(msg: str, *args, **kwargs) -> None:
    """Log to stderr only (never print secrets)."""
    formatted = msg.format(*args, **kwargs)
    safe_msg = redact_secrets(formatted)
    print(safe_msg, file=sys.stderr)

def cache_get(key: str):
    now = time.time()
    v = _CACHE.get(key)
    if v:
        ts, val = v
        if now - ts < CACHE_TTL:
            return val
        del _CACHE[key]
    return None

def cache_set(key: str, value: Any):
    _CACHE[key] = (time.time(), value)

def ensure_rate_limit(tool_name: str, max_parallel: int = 4):
    if tool_name not in _RATE_LIMITS:
        _RATE_LIMITS[tool_name] = asyncio.Semaphore(max_parallel)
    return _RATE_LIMITS[tool_name]

def instrument(tool_name: str):
    """Decorator to measure latency, assign correlation id, and record stats."""
    def deco(func: Callable[..., Coroutine[Any, Any, Any]]):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cid = str(uuid.uuid4())[:8]
            start = time.time()
            
            # Extract JSON-RPC ID if present in kwargs
            jsonrpc_id = kwargs.pop('_jsonrpc_id', None)
            parent_cid = kwargs.pop('_parent_cid', None)
            
            # Store correlation info
            CORRELATION_CHAIN[cid] = {
                "tool": tool_name,
                "start_time": start,
                "jsonrpc_id": jsonrpc_id,
                "parent_cid": parent_cid,
                "args": str(args)[:100],  # Truncate for safety
            }
            
            log("[cid={}] START tool={} jsonrpc_id={} parent={}", cid, tool_name, jsonrpc_id or "N/A", parent_cid or "N/A")
            sem = ensure_rate_limit(tool_name)
            async with sem:
                try:
                    result = await func(*args, **kwargs)
                    elapsed = (time.time() - start) * 1000.0
                    rec = TOOL_STATS.setdefault(tool_name, {"count":0, "total_ms":0.0})
                    rec["count"] += 1
                    rec["total_ms"] += elapsed
                    log("[cid={}] END tool={} elapsed_ms={:.1f}", cid, tool_name, elapsed)
                    
                    # Update correlation chain
                    CORRELATION_CHAIN[cid]["end_time"] = time.time()
                    CORRELATION_CHAIN[cid]["elapsed_ms"] = elapsed
                    CORRELATION_CHAIN[cid]["status"] = "success"
                    
                    # attach correlation id + latency metadata if result is a dict
                    if isinstance(result, dict):
                        result.setdefault("_mcp_meta", {})["correlation_id"] = cid
                        result["_mcp_meta"]["latency_ms"] = round(elapsed,1)
                        if jsonrpc_id:
                            result["_mcp_meta"]["jsonrpc_id"] = jsonrpc_id
                    return result
                except Exception as e:
                    elapsed = (time.time() - start) * 1000.0
                    log("[cid={}] ERROR tool={} elapsed_ms={:.1f} error={}", cid, tool_name, elapsed, repr(e))
                    
                    # Update correlation chain
                    CORRELATION_CHAIN[cid]["end_time"] = time.time()
                    CORRELATION_CHAIN[cid]["elapsed_ms"] = elapsed
                    CORRELATION_CHAIN[cid]["status"] = "error"
                    CORRELATION_CHAIN[cid]["error"] = str(e)
                    raise
        return wrapper
    return deco
