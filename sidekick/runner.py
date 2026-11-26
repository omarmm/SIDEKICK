import subprocess, os, signal
from pathlib import Path

class OpenCodeRunner:
    def __init__(self, binary, timeout):
        self.binary, self.timeout = binary, timeout

    def execute(self, prompt, cwd):
        # Prompt passed as a single argv value, not interpolated into a shell command.
        p = subprocess.Popen([self.binary, "run", prompt], cwd=cwd,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
            start_new_session=True)
        try:
            out, _ = p.communicate(timeout=self.timeout)
        except subprocess.TimeoutExpired:
            try: os.killpg(p.pid, signal.SIGTERM)
            except ProcessLookupError: pass
            try: p.communicate(timeout=10)
            except subprocess.TimeoutExpired:
                try: os.killpg(p.pid, signal.SIGKILL)
                except ProcessLookupError: pass
            raise RuntimeError(f"OpenCode timed out after {self.timeout} seconds")
        return p.returncode, out
