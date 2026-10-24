# Day 13: Container Failure Triage Report

## Overview
This report documents 5 foundational container failure classes encountered in production AI inference systems, isolating root causes across host network, storage permissions, container runtimes, hardware passthrough, and application configuration.

---

### Failure 1: Missing Environment Variable (Image Startup Crash)
- **Layer:** Application Level
- **Symptom:** Container terminates immediately after launching with status `Exited (1)`.
- **Evidence:** 
  - `docker inspect` shows `ExitCode: 1`.
  - `docker logs` captures: `FATAL: MODEL_ENDPOINT or REQUIRED_CONFIG missing`.
- **Root Cause:** Application entrypoint validation halted execution because mandatory environment variables (`CONFIG_READY`) were not passed to the container runtime.
- **Fix:** Injected required environment variables at runtime (`docker run -e CONFIG_READY=true ...`).
- **Prevention:** Use strict configuration models (e.g., Pydantic `BaseSettings`) with fallback defaults or self-documenting startup logs.

---

### Failure 2: Port Collision (Address Already In Use)
- **Layer:** Host Network Stack
- **Symptom:** Secondary container remains in `Created` state and fails to start.
- **Evidence:** 
  - Docker daemon logs error: `bind: address already in use` / `port is already allocated`.
  - `docker ps` verifies existing container binding `0.0.0.0:8000->80/tcp`.
- **Root Cause:** Two independent containers attempted to bind simultaneously to the same host TCP port (`8000`).
- **Fix:** Remapped host port allocation (`-p 8001:80`) or terminated the lingering process occupying port `8000`.
- **Prevention:** Parameterize host bind ports via environment variables (`${INFERENCE_PORT:-8000}`) and route traffic through an API gateway/reverse proxy.

---

### Failure 3: Volume Mount & Read-Only Filesystem
- **Layer:** Storage / Linux Kernel VFS
- **Symptom:** Container process crashes when attempting to write model weights or telemetry to mounted storage.
- **Evidence:** 
  - Python traceback: `OSError: [Errno 30] Read-only file system: '/app/cache/new_weights.bin'`.
  - Volume inspection reveals `:ro` flag or non-root user UID mismatch.
- **Root Cause:** Volume mounted with read-only constraint (`:ro`) preventing write operations to cache paths.
- **Fix:** Updated volume mount flags to read-write (`-v host_path:/app/cache:rw`) and ensured write permissions match container execution UID.
- **Prevention:** Explicitly separate static configuration volumes (`:ro`) from dynamic caching volumes (`:rw`) in container specs.

---

### Failure 4: Missing GPU / Device Runtime Failure
- **Layer:** Container Runtime & NVIDIA Driver Passthrough
- **Symptom:** Container fails at creation/start with device selection failure.
- **Evidence:** 
  - Docker daemon error: `could not select device driver "" with capabilities: [[gpu]]`.
  - Container remains in `Created` state without launching PID 1.
- **Root Cause:** `--gpus all` requested on a host lacking physical NVIDIA hardware and the `nvidia-container-toolkit`.
- **Fix:** Switched to standard CPU container execution mode and verified graceful runtime device detection (`device = 'cuda' if torch.cuda.is_available() else 'cpu'`).
- **Prevention:** Decouple Compose files into CPU (`docker-compose.yml`) and GPU-accelerated (`docker-compose.gpu.yml`) profiles.

---

### Failure 5: Missing / Unmounted Model Cache
- **Layer:** State & Persistence Architecture
- **Symptom:** Significant startup latency, egress network spikes, or strict local cache policy violation (`ExitCode: 1`).
- **Evidence:** 
  - Container logs show: `WARNING: Model cache not mounted or empty!` followed by `FATAL: STRICT_LOCAL_CACHE_ONLY policy violated`.
- **Root Cause:** Ephemeral container storage without persistent volume mounting, causing loss of weights across container lifecycles.
- **Fix:** Attached host directory to container cache directory (`-v $(pwd)/artifacts/day13/model_cache:/app/cache:ro`).
- **Prevention:** Enforce volume declarations for model storage in production manifests (`VOLUME ["/app/cache"]`) and validate local artifact presence before accepting inference traffic.
