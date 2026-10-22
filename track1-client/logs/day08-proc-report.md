
# Day 8 — Environment & Process Report

## Step 1: Docker Checks

- Docker version: `29.8.2`
- `docker ps`: PASS
- Docker daemon: ACCESSIBLE
- Docker context: `default`
- Docker Desktop with WSL 2: Detected

## Step 2: NVIDIA GPU Checks

- `nvidia-smi`: FAIL — command not found in Ubuntu WSL
- `/dev/nvidia*` devices: NOT VISIBLE

## Step 3: Docker GPU Runtime Test

- Test: `docker run --rm --gpus all ubuntu:22.04 nvidia-smi`
- Result: SKIPPED
- Reason: NVIDIA GPU access was not verified in Ubuntu WSL.
- Note: The GPU test was not run.

## Diagnosis

- Docker CLI and daemon are working.
- NVIDIA GPU access is not currently verified in WSL.
- No additional NVIDIA packages were installed during these checks.

## Step 5: Invalid PID Failure Test

- Command: `./scripts/proc_snapshot.sh 99999999`
- Result: PASS
- Error message: Process does not exist or is not accessible.
- Exit code: `1`
- Conclusion: The script correctly handles an invalid or inaccessible PID.
