import asyncio
import sys
import tempfile
import os
import logging
try:
    import resource
except ImportError:
    resource = None
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

class ReplicationEngine:
    """
    Layer 4: Empirical Validation (v53 Hardened).
    Executes a python script and verifies its output with strict resource limits.
    """
    def __init__(self, timeout: int = 30, memory_limit_mb: int = 256):
        self.timeout = timeout
        self.memory_limit = memory_limit_mb * 1024 * 1024

    def _set_resource_limits(self):
        """Sets memory and CPU limits for the child process."""
        if not resource:
            return
        # Limit address space
        resource.setrlimit(resource.RLIMIT_AS, (self.memory_limit, self.memory_limit))
        # Limit CPU time
        resource.setrlimit(resource.RLIMIT_CPU, (self.timeout, self.timeout))
        # Disable core dumps
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))

    async def replicate_script(self, code_content: str, expected_output: str) -> Dict[str, Any]:
        """
        Executes code in a hardened subprocess with resource constraints.
        """
        logger.info(f"ReplicationEngine: Executing script with {self.timeout}s timeout and {self.memory_limit/1e6}MB RAM limit.")

        # Security: Basic static analysis to block obvious dangerous calls
        dangerous_calls = ["os.system", "subprocess.call", "shutil.rmtree", "socket.", "requests."]
        for call in dangerous_calls:
            if call in code_content:
                 return {"status": "SECURITY_VIOLATION", "reason": f"Dangerous call '{call}' detected."}

        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
            tmp.write(code_content.encode())
            tmp_path = tmp.name

        try:
            # Execute in a subprocess with resource limits via preexec_fn
            # Note: preexec_fn is not supported on Windows
            preexec = self._set_resource_limits if os.name != 'nt' else None
            process = await asyncio.create_subprocess_exec(
                sys.executable, tmp_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                preexec_fn=preexec,
                env={"PYTHONPATH": os.getcwd(), "JULES_AI_VERSION": "99.0.0"} # Restricted env
            )

            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=self.timeout + 2)

                output = stdout.decode().strip()
                success = output == expected_output.strip()

                return {
                    "status": "REPRODUCED" if success else "FAILED",
                    "actual_output": output,
                    "error": stderr.decode(),
                    "reproducibility_score": 1.0 if success else 0.0
                }
            except asyncio.TimeoutError:
                process.kill()
                return {
                    "status": "TIMEOUT",
                    "reason": f"Execution exceeded {self.timeout}s limit."
                }
        except Exception as e:
            return {"status": "ERROR", "reason": str(e)}
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
