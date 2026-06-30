#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$ROOT_DIR/tmp"
API_PID_FILE="$TMP_DIR/ml-api.pid"
WEB_PID_FILE="$TMP_DIR/interface-demo.pid"

API_PORT=8000
WEB_PORT=5173

c_green="\033[1;32m"
c_yellow="\033[1;33m"
c_red="\033[1;31m"
c_reset="\033[0m"

info()  { printf "${c_green}[stop]${c_reset} %s\n" "$*"; }
warn()  { printf "${c_yellow}[stop]${c_reset} %s\n" "$*"; }

kill_pid() {
  local pid_file="$1"
  local label="$2"
  local port="$3"

  local pid=""
  if [[ -f "$pid_file" ]]; then
    pid="$(cat "$pid_file" 2>/dev/null || true)"
  fi

  if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
    info "Stopping $label (pid $pid)..."
    kill "$pid" 2>/dev/null || true
    local tries=40
    while (( tries-- > 0 )) && kill -0 "$pid" 2>/dev/null; do
      sleep 0.2
    done
    if kill -0 "$pid" 2>/dev/null; then
      warn "$label did not stop gracefully, sending SIGKILL"
      kill -9 "$pid" 2>/dev/null || true
    fi
    info "$label stopped"
  else
    warn "$label pid not found, scanning port $port"
    local leftover
    leftover="$(lsof -ti :"$port" 2>/dev/null || true)"
    if [[ -n "$leftover" ]]; then
      warn "Killing stray process(es) on port $port: $leftover"
      kill $leftover 2>/dev/null || true
      sleep 0.5
      kill -9 $leftover 2>/dev/null || true
    else
      warn "$label was not running"
    fi
  fi

  rm -f "$pid_file"
}

# Stop in reverse order: web first (it depends on the API).
kill_pid "$WEB_PID_FILE" "interface-demo" "$WEB_PORT"
kill_pid "$API_PID_FILE" "ML API"        "$API_PORT"

info "Done."