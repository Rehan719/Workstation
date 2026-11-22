#!/bin/bash
# FU-1284's drill (W1140), on a machine with Docker: nothing is deployed and no account is touched.
# Usage: deploy/https_drill.sh IMAGE   (an image built from this tree's Dockerfile)
# The startup script's own HTTPS front (start_front in deploy/gcp/startup.sh) is started for workstation.localhost, a
# name Caddy serves with a certificate from its own local authority: a public authority certifies only a domain, which
# is the Owner's to buy. Ports 80 and 443 of this machine are used, as the release machine uses them.
#   HTTPS: the platform answers through Caddy, HTTP is redirected to HTTPS, and the platform has no port of its own.
#   THE CLIENT'S ADDRESS: the platform logs the address Caddy saw a request come from, and does not believe a forwarded
#            address the caller wrote itself; started without the setting, it logs Caddy's own address instead.
# Prints one KEY=VALUE line per measurement.
set -u
IMG=${1:?platform image}
DOM=workstation.localhost
HERE=$(cd "$(dirname "$0")" && pwd)
for c in caddy workstation; do
  docker inspect "$c" >/dev/null 2>&1 && { echo "REFUSED: a container named $c is already on this machine"; exit 1; }
done
docker network inspect workstation-front >/dev/null 2>&1 && { echo "REFUSED: a network named workstation-front is already on this machine"; exit 1; }
M=$(mktemp -d); chown 1000:1000 "$M"
cleanup() { docker rm -f caddy workstation >/dev/null 2>&1; docker network rm workstation-front >/dev/null 2>&1
            docker volume rm -f caddy-data caddy-config >/dev/null 2>&1; rm -rf "$M"; }
trap cleanup EXIT

#  the startup script's own steps, sourced: only its functions are defined, and its records' folder is the drill's
export WORKSTATION_STARTUP_SOURCED=1 WORKSTATION_MNT="$M"
. "$HERE/gcp/startup.sh"
valid_domain "$DOM" || { echo "REFUSED: the startup script would refuse $DOM"; exit 1; }

get() { curl -sk --noproxy '*' --resolve "$DOM:443:127.0.0.1" "$@"; }
healthy() {
  for _ in $(seq 1 120); do
    [ "$(get -o /dev/null -w '%{http_code}' "https://$DOM/health")" = "200" ] && return 0; sleep 1
  done
  return 1
}
seen() {    # the address the platform's access log gives for the request marked $1
  docker logs workstation 2>&1 | grep "GET /health?drill=$1 " | tail -1 | awk '{print $2}' | sed 's/:[0-9]*$//'
}

t0=$(date +%s.%N)
#  the front starts only with sign-in on, its fourth argument (W1191); /health answers with sign-in on
start_front "$IMG" drill "$DOM" true >/dev/null || { echo "FRONT_START_FAILED"; exit 1; }
healthy || { echo "FRONT_NOT_HEALTHY"; docker logs --tail 20 caddy; exit 1; }
echo "FRONT_TO_HEALTH_SECONDS=$(python3 -c "import time; print(round(time.time() - $t0, 1))")"
echo "IMAGE=$IMG"
echo "CADDY_IMAGE=$CADDY_IMAGE"
echo "HTTPS_HEALTH=$(get -o /dev/null -w '%{http_code}' "https://$DOM/health")"
echo "HTTP_ANSWER=$(curl -s --noproxy '*' --resolve "$DOM:80:127.0.0.1" -o /dev/null -w '%{http_code} %{redirect_url}' "http://$DOM/health")"
echo "PLATFORM_PORTS_PUBLISHED=$(docker port workstation | grep -c .)"
echo "CERT_ISSUER=$(echo | openssl s_client -connect 127.0.0.1:443 -servername "$DOM" 2>/dev/null | openssl x509 -noout -issuer 2>/dev/null | sed 's/^issuer= *//')"
echo "CADDY_ADDRESS=$(docker inspect caddy --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')"
echo "PLATFORM_ADDRESS=$(docker inspect workstation --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')"
echo "GATEWAY=$(docker network inspect workstation-front --format '{{range .IPAM.Config}}{{.Gateway}}{{end}}')"
get -o /dev/null "https://$DOM/health?drill=plain"
get -o /dev/null -H 'X-Forwarded-For: 203.0.113.7' "https://$DOM/health?drill=forged"
sleep 1
echo "PLATFORM_SAW=$(seen plain)"
echo "PLATFORM_SAW_WITH_A_FORGED_HEADER=$(seen forged)"

#  the control: the same platform on the same network, started without the setting
docker rm -f workstation >/dev/null
docker run --name=workstation --detach --network=workstation-front --volume="$M":/app/data "$IMG" >/dev/null || {
  echo "CONTROL_START_FAILED"; exit 1; }
healthy || { echo "CONTROL_NOT_HEALTHY"; exit 1; }
get -o /dev/null "https://$DOM/health?drill=control"
sleep 1
echo "WITHOUT_THE_SETTING_PLATFORM_SAW=$(seen control)"
echo "DRILL_DONE=yes"
