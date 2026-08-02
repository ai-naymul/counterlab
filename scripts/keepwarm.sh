#!/usr/bin/env bash
# Keep the free Render instance awake across the judging window only.
#
# WHY A WINDOW AND NOT ALWAYS:
# Render grants 750 free instance-hours per MONTH per WORKSPACE, shared by every
# free web service in it. Exceeding it suspends ALL of them until the 1st. This
# workspace has 9 free web services, so pinging one 24/7 (~690 h for the rest of
# the month) risks taking the others down too.
#
# Judging is 16:00-19:30 PDT on 2 Aug = 05:00-08:30 GMT+6 on 3 Aug.
# This covers 04:30-09:00 GMT+6, which costs about 4.5 instance-hours.
#
#   ./scripts/keepwarm.sh                  # default window
#   START=04:30 END=09:00 ./scripts/keepwarm.sh
#   ./scripts/keepwarm.sh --now            # ping immediately until END

set -uo pipefail

URL="${URL:-https://counterlab.onrender.com/healthz}"
START="${START:-04:30}"
END="${END:-09:00}"
INTERVAL="${INTERVAL:-600}"   # 10 min - comfortably inside Render's 15 min idle timeout

log() { printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S %Z')" "$*"; }

start_ts=$(date -d "today $START" +%s 2>/dev/null) || { echo "bad START"; exit 1; }
end_ts=$(date -d "today $END" +%s 2>/dev/null) || { echo "bad END"; exit 1; }
now=$(date +%s)
# If the window already passed today, aim at tomorrow.
if [ "$end_ts" -lt "$now" ]; then
  start_ts=$((start_ts + 86400)); end_ts=$((end_ts + 86400))
fi

if [ "${1:-}" = "--now" ]; then
  log "pinging immediately until $(date -d "@$end_ts" '+%H:%M')"
else
  wait_s=$((start_ts - now))
  if [ "$wait_s" -gt 0 ]; then
    log "sleeping ${wait_s}s until $(date -d "@$start_ts" '+%Y-%m-%d %H:%M %Z')"
    sleep "$wait_s"
  fi
fi

log "keep-warm started -> $URL (every ${INTERVAL}s until $(date -d "@$end_ts" '+%H:%M'))"
hits=0; fails=0
while [ "$(date +%s)" -lt "$end_ts" ]; do
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 90 "$URL" || echo 000)
  if [ "$code" = "200" ]; then hits=$((hits+1)); else fails=$((fails+1)); log "WARN http=$code"; fi
  sleep "$INTERVAL"
done
log "keep-warm finished: $hits ok, $fails failed, ~$(( (end_ts - start_ts) / 3600 )) instance-hours used"
