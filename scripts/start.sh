#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$ROOT_DIR/logs"
TMP_DIR="$ROOT_DIR/tmp"
mkdir -p "$LOG_DIR" "$TMP_DIR"

API_PID_FILE="$TMP_DIR/ml-api.pid"
WEB_PID_FILE="$TMP_DIR/interface-demo.pid"

API_PORT=8000
WEB_PORT=5173

API_LOG="$LOG_DIR/ml-api.log"
WEB_LOG="$LOG_DIR/interface-demo.log"

c_green="\033[1;32m"
c_yellow="\033[1;33m"
c_red="\033[1;31m"
c_reset="\033[0m"

info()  { printf "${c_green}[start]${c_reset} %s\n" "$*"; }
warn()  { printf "${c_yellow}[start]${c_reset} %s\n" "$*"; }
fail()  { printf "${c_red}[start]${c_reset} %s\n" "$*" >&2; exit 1; }

port_in_use() {
  local port="$1"
  lsof -ti :"$port" >/dev/null 2>&1
}

is_running() {
  local pid_file="$1"
  [[ -f "$pid_file" ]] && kill -0 "$(cat "$pid_file")" 2>/dev/null
}

wait_for_port() {
  local port="$1"
  local log_file="$2"
  local label="$3"
  local tries=50
  while (( tries-- > 0 )); do
    if port_in_use "$port"; then
      info "$label is up on port $port"
      return 0
    fi
    sleep 0.2
  done
  warn "$label did not start on port $port. See $log_file"
  return 1
}

start_api() {
  if is_running "$API_PID_FILE"; then
    warn "ML API already running (pid $(cat "$API_PID_FILE"))"
    return 0
  fi
  if port_in_use "$API_PORT"; then
    fail "Port $API_PORT is busy. Run scripts/stop.sh first."
  fi

  local venv="$ROOT_DIR/ml-service/.venv"
  if [[ ! -x "$venv/bin/uvicorn" ]]; then
    fail "venv not found at $venv. Run: cd ml-service && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
  fi

  info "Starting ML API on port $API_PORT..."
  (
    cd "$ROOT_DIR/ml-service"
    nohup "$venv/bin/uvicorn" lead_qualify.api.main:app --host 127.0.0.1 --port "$API_PORT" \
      >"$API_LOG" 2>&1 &
    echo $! >"$API_PID_FILE"
  )
  wait_for_port "$API_PORT" "$API_LOG" "ML API"
}

start_web() {
  if is_running "$WEB_PID_FILE"; then
    warn "interface-demo already running (pid $(cat "$WEB_PID_FILE"))"
    return 0
  fi
  if port_in_use "$WEB_PORT"; then
    fail "Port $WEB_PORT is busy. Run scripts/stop.sh first."
  fi

  if [[ ! -d "$ROOT_DIR/interface-demo/node_modules" ]]; then
    fail "node_modules missing. Run: cd interface-demo && yarn install"
  fi

  local pm=()
  if command -v yarn >/dev/null 2>&1 && [[ -f "$ROOT_DIR/interface-demo/yarn.lock" ]]; then
    pm=(yarn)
  elif command -v npm >/dev/null 2>&1; then
    pm=(npm)
  else
    fail "Neither yarn nor npm is available"
  fi

  info "Starting interface-demo on port $WEB_PORT (using ${pm[0]})..."
  (
    cd "$ROOT_DIR/interface-demo"
    nohup "${pm[@]}" run dev -- --host 127.0.0.1 --port "$WEB_PORT" \
      >"$WEB_LOG" 2>&1 &
    echo $! >"$WEB_PID_FILE"
  )
  wait_for_port "$WEB_PORT" "$WEB_LOG" "interface-demo"
}

start_api
start_web

info "Done."
info "  ML API          -> http://127.0.0.1:$API_PORT/docs"
info "  interface-demo  -> http://127.0.0.1:$WEB_PORT"
info "  Logs            -> $LOG_DIR"
info "  Stop            -> scripts/stop.sh"