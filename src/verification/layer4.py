import asyncio
import sys
import tempfile
import os
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

class ReplicationEngine:
    """
    Layer 4: Empirical Validation.
    Executes a python script and verifies its output.
    v52.0 Security Hardening: Added execution timeout and logging.
    """
    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    async def replicate_script(self, code_content: str, expected_output: str) -> Dict[str, Any]:
        """
        Executes the given python code in a temporary file and checks stdout.
        WARNING: This executes arbitrary code. Ensure input is trusted or
        run within a sandboxed environment (e.g., Docker).
        """
        logger.warning("ReplicationEngine: Executing arbitrary code. Ensure sandbox safety.")

        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
            tmp.write(code_content.encode())
            tmp_path = tmp.name

        try:
            # Execute in a subprocess with timeout
            process = await asyncio.create_subprocess_exec(
                sys.executable, tmp_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=self.timeout)

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
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
