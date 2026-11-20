#!/bin/bash
# The release machine's startup script: Google Cloud, Container-Optimized OS (W1134, FU-603).
#
# Compute Engine runs it as root at every boot. On this OS /etc is stateless, so what it sets up - the mount, the host
# firewall's rules, the registry sign-in - it sets up again at every boot. It holds no key: the registry sign-in uses
# the machine's own service account. The steps that start the machine are in docs/DEPLOYMENT.md, "The Google Cloud
# deploy, step by step", each with the page it was read at.
#
# THE RECORDS: the platform keeps them as files under DATA_DIR (/app/data in the image), so they live on a disk of
# their own, which the machine's deletion leaves in place. This script refuses, rather than guesses, at the one step
# that could destroy them: the data disk is formatted ONLY when it is blank (its first MiB all zeros, and no ext4
# file system on it). A disk that holds anything else is left exactly as it is, and the platform is not started.
#
# A RELEASE OR A ROLLBACK is a change to the machine's metadata key image-tag followed by a re-run of this script
# (docs/DEPLOYMENT.md, step 8): the tag names the image the platform is started from.
#
# HTTPS (W1140, FU-1284): with a domain in the machine's metadata (key domain, docs/DEPLOYMENT.md step 12), Caddy
# answers on ports 80 and 443 in front of the platform and obtains the domain's certificate itself. With none, the
# platform serves plain HTTP on port 80, and no person signs in until a domain is set.

set -u

DISK="${WORKSTATION_DISK:-/dev/disk/by-id/google-workstation-data}"
MNT="${WORKSTATION_MNT:-/mnt/disks/data}"
REGION="${WORKSTATION_REGION:-us-central1}"

log() { echo "workstation-startup: $*"; }

# The ext4 superblock begins 1024 bytes in; its magic number 0xEF53 sits 56 bytes into it, stored as 53 ef.
has_ext4() {
    [ "$(dd if="$1" bs=1 skip=1080 count=2 2>/dev/null | od -An -tx1 | tr -d ' \n')" = "53ef" ]
}

# A new persistent disk reads as zeros. Blank means the first MiB could be read whole and every byte of it is zero.
is_blank() {
    local n z
    n=$(head -c 1048576 "$1" 2>/dev/null | wc -c) || return 1
    [ "$n" -eq 1048576 ] || return 1
    z=$(head -c 1048576 "$1" 2>/dev/null | tr -d '\000' | wc -c) || return 1
    [ "$z" -eq 0 ]
}

# Leaves the disk ready to mount, or refuses: 0 when it holds ext4 (kept as it is) or was blank (formatted now).
prepare_disk() {
    local disk="$1"
    if [ ! -e "$disk" ]; then
        log "no data disk at $disk: the platform is not started"
        return 1
    fi
    if has_ext4 "$disk"; then
        log "the data disk holds its file system: kept as it is"
        return 0
    fi
    if is_blank "$disk"; then
        log "the data disk is blank: formatting it once"
        mkfs.ext4 -m 0 -E lazy_itable_init=0,lazy_journal_init=0,discard "$disk" </dev/null || return 1
        has_ext4 "$disk" || return 1
        return 0
    fi
    log "the data disk at $disk is neither blank nor ext4: NOT formatted, and the platform is not started"
    return 1
}

#  A domain is lower-case labels of letters, digits and hyphens joined by dots, the last beginning with a letter: never
#  an IP address, a bare name, or anything with a character a host name cannot hold (W1140)
valid_domain() {
    [ ${#1} -le 253 ] || return 1
    [[ "$1" =~ ^([a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]([a-z0-9-]{0,61}[a-z0-9])?$ ]]
}

#  THE HTTPS FRONT (W1140, FU-1284). Caddy's one-command reverse proxy answers on ports 80 and 443 for the domain,
#  obtains its certificate from a public authority, keeps it renewed and redirects HTTP to HTTPS. The platform is on a
#  private network with no port of its own, and believes a forwarded client address only from Caddy's fixed address;
#  Docker gives its own addresses from the network's top half, so Caddy's is never taken. Caddy's certificates are
#  kept in a Docker volume: /var/lib/docker is stateful on this OS, for the life of the boot disk.
CADDY_IMAGE="caddy:2.11.9@sha256:4851e54a46b206517c574821bb5cc67f170d2156041e9fbc4c9193b45e84a75b"
FRONT_NET=workstation-front
FRONT_IP=172.30.0.2

start_front() {    # IMAGE TAG DOMAIN
    docker network inspect "$FRONT_NET" >/dev/null 2>&1 \
        || docker network create --subnet=172.30.0.0/24 --ip-range=172.30.0.128/25 --gateway=172.30.0.1 "$FRONT_NET" \
        || return 1
    docker run --name=workstation --restart=always --detach --network="$FRONT_NET" \
        --env=FORWARDED_ALLOW_IPS="$FRONT_IP" --volume="$MNT":/app/data \
        --log-opt max-size=10m --log-opt max-file=3 \
        --label=app=workstation --label=image-tag="$2" \
        "$1" || return 1
    docker run --name=caddy --restart=always --detach --network="$FRONT_NET" --ip="$FRONT_IP" \
        --publish=80:80 --publish=443:443 --volume=caddy-data:/data --volume=caddy-config:/config \
        --log-opt max-size=10m --log-opt max-file=3 --label=app=workstation \
        "$CADDY_IMAGE" caddy reverse-proxy --from "$3" --to workstation:8000
}

metadata() {
    curl -fsS "http://metadata.google.internal/computeMetadata/v1/$1" -H "Metadata-Flavor: Google"
}

main() {
    prepare_disk "$DISK" || exit 1
    mkdir -p "$MNT"
    grep -qs " $MNT " /proc/mounts || mount -o discard,defaults "$DISK" "$MNT" || exit 1
    chown 1000:1000 "$MNT"    # the image's user, app, is uid 1000 (measured W1134)

    # This OS refuses incoming traffic by default. The VPC firewall rule (step 6) is what admits ports 80 and 443
    # alone; 443 is answered once the machine has a domain (step 12).
    iptables -A INPUT -j ACCEPT
    iptables -A FORWARD -j ACCEPT

    local project tag image domain
    project=$(metadata project/project-id) || exit 1
    tag=$(metadata instance/attributes/image-tag) || { log "no image-tag in the machine's metadata: not started"; exit 1; }
    image="$REGION-docker.pkg.dev/$project/workstation/workstation:$tag"
    domain=$(metadata instance/attributes/domain 2>/dev/null | tr 'A-Z' 'a-z')    # none: plain HTTP (W1140)
    if [ -n "$domain" ] && ! valid_domain "$domain"; then
        log "the machine's domain is not a host name: not started, and the running platform is left as it was"
        exit 1
    fi

    export HOME=/home/appuser    # where the registry sign-in is kept
    docker-credential-gcr configure-docker --registries "$REGION-docker.pkg.dev" || exit 1
    docker pull "$image" || { log "the image $image could not be pulled: the running platform is left as it was"; exit 1; }
    if [ -n "$domain" ]; then
        docker image inspect "$CADDY_IMAGE" >/dev/null 2>&1 || docker pull "$CADDY_IMAGE" \
            || { log "the front's image could not be pulled: the running platform is left as it was"; exit 1; }
    fi
    docker stop caddy workstation || true
    docker rm caddy workstation || true
    if [ -n "$domain" ]; then
        start_front "$image" "$tag" "$domain"
        return
    fi
    docker run --name=workstation --restart=always --detach \
        --publish=80:8000 --volume="$MNT":/app/data \
        --log-opt max-size=10m --log-opt max-file=3 \
        --label=app=workstation --label=image-tag="$tag" \
        "$image"
}

# Run, it starts the platform. Sourced (as test_w1134 does, with WORKSTATION_STARTUP_SOURCED=1), it only defines
# the steps above, so the disk step can be driven on its own against disk images.
if [ "${WORKSTATION_STARTUP_SOURCED:-}" != "1" ] && [ "${BASH_SOURCE[0]}" = "$0" ]; then
    main "$@"
fi
