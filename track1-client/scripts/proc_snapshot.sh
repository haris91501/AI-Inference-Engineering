#!/usr/bin/env bash

set -Eeuo pipefail

usage() {
    echo "Usage: $0 <PID>" >&2
    exit 2
}

if [[ $# -ne 1 ]]; then
    usage
fi

PID="$1"

if [[ ! "$PID" =~ ^[1-9][0-9]*$ ]]; then
    echo "ERROR: PID must be a positive integer." >&2
    exit 2
fi

PROC_DIR="/proc/$PID"

if [[ ! -d "$PROC_DIR" ]]; then
    echo "ERROR: Process $PID does not exist or is not accessible." >&2
    exit 1
fi

echo "======================================"
echo "       LINUX PROCESS SNAPSHOT"
echo "======================================"
echo "Timestamp: $(date --iso-8601=seconds)"
echo "PID: $PID"
echo

echo "---- Process Identity & State ----"

if ! grep -E '^(Name|State|Pid|PPid|Threads):' "$PROC_DIR/status"; then
    echo "ERROR: Unable to read process identity." >&2
    exit 1
fi

echo
echo "---- Memory (status) ----"

grep -E '^(VmSize|VmRSS|VmPeak|VmSwap):' "$PROC_DIR/status" || true

echo
echo "---- Signal State ----"

grep -E '^(SigPnd|ShdPnd|SigBlk|SigIgn|SigCgt):' "$PROC_DIR/status" || true

echo
echo "---- Command Line ----"

if [[ -r "$PROC_DIR/cmdline" ]]; then
    tr '\0' ' ' < "$PROC_DIR/cmdline"
    echo
else
    echo "Command line unavailable."
fi

echo
echo "---- Memory Summary (smaps_rollup) ----"

if [[ -r "$PROC_DIR/smaps_rollup" ]]; then
    grep -E '^(Rss|Pss|Private_Clean|Private_Dirty|Shared_Clean|Shared_Dirty|Swap):' \
        "$PROC_DIR/smaps_rollup" || true
else
    echo "smaps_rollup unavailable (permissions or kernel support)."
fi

echo
echo "---- Open File Descriptors ----"

if [[ -d "$PROC_DIR/fd" ]]; then
    ls -l "$PROC_DIR/fd" 2>&1 || true
    echo "Open descriptor count: $(find "$PROC_DIR/fd" -mindepth 1 -maxdepth 1 2>/dev/null | wc -l)"
else
    echo "File descriptor directory unavailable."
fi

echo
echo "---- Snapshot Complete ----"
