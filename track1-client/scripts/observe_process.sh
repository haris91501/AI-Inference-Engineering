```bash
#!/usr/bin/env bash

set -u

# Save the report to the requested log file.
LOG_FILE="logs/day05-process.txt"

mkdir -p logs artifacts/day05

# Start a new report.
{
    echo "========================================"
    echo "DAY 05 - PROCESS OBSERVATION REPORT"
    echo "========================================"
    echo "Date: $(date)"
    echo "Working directory: $(pwd)"
    echo

    echo "----- Python Version -----"
    python --version 2>&1
    echo "Python version command exit status: $?"
    echo

    echo "----- File Details -----"
    ls -l
    echo "File listing exit status: $?"
    echo

    echo "----- Process List -----"
    ps -ef
    echo "Process listing exit status: $?"
    echo

    echo "----- Current Shell Process -----"
    ps -p "$$" -o pid,ppid,stat,args
    echo

    echo "----- Process Tree -----"
    if command -v pstree >/dev/null 2>&1; then
        pstree -p "$$"
    else
        echo "pstree is not installed; using ps instead."
        ps -ef
    fi
    echo

    echo "----- Selected Environment Variables -----"
    printf 'USER=%s\n' "${USER:-unknown}"
    printf 'HOME=%s\n' "${HOME:-unknown}"
    printf 'PWD=%s\n' "${PWD:-unknown}"
    echo

    echo "----- Report Finished -----"
    echo "Observation script completed."
} > "$LOG_FILE" 2>&1

# Save the script's exit status before running another command.
SCRIPT_STATUS=$?

echo "Report saved to: $LOG_FILE"
echo "Observation script exit status: $SCRIPT_STATUS"

exit "$SCRIPT_STATUS"
```

