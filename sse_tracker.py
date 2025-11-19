# sse_tracker.py
"""
SSE (Server-Sent Events) tracker for monitoring streaming events from SonarQube compute engine.
Captures timing and correlates events with tool executions.
"""
import time
import asyncio
from typing import AsyncIterator, Optional
import httpx
from mcp_helpers import log, CORRELATION_CHAIN

# SSE event storage
SSE_EVENTS: list[dict] = []


async def track_sse_events(
    url: str,
    auth: tuple,
    correlation_id: str,
    timeout: float = 60.0
) -> AsyncIterator[dict]:
    """
    Track SSE events from a URL, correlating them with a correlation ID.
    
    Args:
        url: SSE endpoint URL
        auth: Authentication tuple
        correlation_id: Parent correlation ID to link events to
        timeout: Maximum time to listen
    
    Yields:
        Parsed SSE events with timing metadata
    """
    start_time = time.time()
    event_count = 0
    
    log("[cid={}] SSE: Starting stream from {}", correlation_id, url)
    
    try:
        async with httpx.AsyncClient(auth=auth, timeout=timeout) as client:
            async with client.stream('GET', url) as response:
                if response.status_code != 200:
                    log("[cid={}] SSE: Failed to connect, status={}", correlation_id, response.status_code)
                    return
                
                buffer = ""
                async for chunk in response.aiter_text():
                    buffer += chunk
                    
                    # Process complete events (separated by double newline)
                    while '\n\n' in buffer:
                        event_text, buffer = buffer.split('\n\n', 1)
                        
                        # Parse SSE event
                        event_data = {}
                        for line in event_text.split('\n'):
                            if line.startswith('data: '):
                                try:
                                    import json
                                    event_data = json.loads(line[6:])
                                except:
                                    event_data = {'raw': line[6:]}
                        
                        if event_data:
                            event_count += 1
                            event_record = {
                                "correlation_id": correlation_id,
                                "event_number": event_count,
                                "timestamp": time.time(),
                                "offset_ms": (time.time() - start_time) * 1000,
                                "data": event_data
                            }
                            
                            SSE_EVENTS.append(event_record)
                            log("[cid={}] SSE: Event #{} at {:.1f}ms: {}", 
                                correlation_id, event_count, event_record["offset_ms"], 
                                str(event_data)[:100])
                            
                            yield event_record
                    
                    # Check timeout
                    if time.time() - start_time > timeout:
                        log("[cid={}] SSE: Timeout after {:.1f}s", correlation_id, timeout)
                        break
    
    except Exception as e:
        log("[cid={}] SSE: Error - {}", correlation_id, repr(e))
    
    finally:
        elapsed = (time.time() - start_time) * 1000
        log("[cid={}] SSE: Stream ended after {:.1f}ms, {} events received", 
            correlation_id, elapsed, event_count)
        
        # Update correlation chain
        if correlation_id in CORRELATION_CHAIN:
            CORRELATION_CHAIN[correlation_id]["sse_events"] = event_count
            CORRELATION_CHAIN[correlation_id]["sse_duration_ms"] = elapsed


async def monitor_sonar_ce_task_sse(task_id: str, base_url: str, auth: tuple, correlation_id: str) -> None:
    """
    Monitor a SonarQube Compute Engine task via SSE (if supported).
    Note: SonarQube doesn't natively support SSE for CE tasks, but this demonstrates the pattern.
    """
    sse_url = f"{base_url}/api/ce/task?id={task_id}&stream=true"
    
    async for event in track_sse_events(sse_url, auth, correlation_id):
        # Process specific event types
        status = event.get("data", {}).get("status")
        if status in ("SUCCESS", "FAILED", "CANCELED"):
            log("[cid={}] SSE: Task completed with status={}", correlation_id, status)
            break


def get_sse_stats() -> dict:
    """Get SSE statistics."""
    if not SSE_EVENTS:
        return {"total_events": 0, "streams": 0}
    
    streams = set(e["correlation_id"] for e in SSE_EVENTS)
    
    return {
        "total_events": len(SSE_EVENTS),
        "streams": len(streams),
        "events_by_stream": {
            cid: len([e for e in SSE_EVENTS if e["correlation_id"] == cid])
            for cid in streams
        }
    }
