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

metadata() {
    curl -fsS "http://metadata.google.internal/computeMetadata/v1/$1" -H "Metadata-Flavor: Google"
}

main() {
    prepare_disk "$DISK" || exit 1
    mkdir -p "$MNT"
    grep -qs " $MNT " /proc/mounts || mount -o discard,defaults "$DISK" "$MNT" || exit 1
    chown 1000:1000 "$MNT"    # the image's user, app, is uid 1000 (measured W1134)

    # This OS refuses incoming traffic by default. The VPC firewall rule (step 6) is what admits port 80 alone.
    iptables -A INPUT -j ACCEPT
    iptables -A FORWARD -j ACCEPT

    local project tag image
    project=$(metadata project/project-id) || exit 1
    tag=$(metadata instance/attributes/image-tag) || { log "no image-tag in the machine's metadata: not started"; exit 1; }
    image="$REGION-docker.pkg.dev/$project/workstation/workstation:$tag"

    export HOME=/home/appuser    # where the registry sign-in is kept
    docker-credential-gcr configure-docker --registries "$REGION-docker.pkg.dev" || exit 1
    docker pull "$image" || { log "the image $image could not be pulled: the running platform is left as it was"; exit 1; }
    docker stop workstation || true
    docker rm workstation || true
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
