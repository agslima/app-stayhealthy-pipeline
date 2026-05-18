# System Reproducibility Gates & Evidence

[//]: # (owner: Project Maintainers)
[//]: # (review_cadence: Quarterly)
[//]: # (last_reviewed: 2026-05-14)

This document defines the reproducibility enforcement gates and historical pilot evidence for the release path across core system services.

As of May 2026, the reproducibility checks have graduated from an observation pilot to a **hard blocking gate** for the backend, frontend, and worker services.

## Objective

Ensure byte-for-byte determinism of all production release images, mitigating supply chain poisoning by validating that our source code and build pipelines consistently produce identical OCI manifest digests under normalized inputs.

## Scope

- Workflow: `.github/workflows/ci-release-gate.yml`
- Job Strategy: Matrix execution across `backend`, `frontend`, and `worker`
- Comparison basis: OCI manifest digest extracted from two locally generated OCI archives per service.

## Gate Design

The release workflow enforces reproducibility by executing the following steps for each service:

1. Checks out the release commit with full Git history.
2. Calculates deterministic timestamps directly from the Git commit (`git log -1 --format=%ct`).
3. Builds the image twice with `docker buildx build` using normalized metadata.
   - `BUILD_DATE=<ISO 8601 Git Commit Timestamp>`
   - `SOURCE_DATE_EPOCH=<Git Commit Timestamp>`
   - `VCS_REF=<release sha>`
   - `VERSION=<release tag>`
   - `SOURCE=https://github.com/<repo>`
4. Disables provenance and SBOM emission for the local build so the comparison focuses strictly on the filesystem output.
5. Generates comparison reports using `scripts/supply-chain/report-reproducibility-pilot.py` without the mismatch allowance flag.

## Success, Failure, and Emergency Overrides

**Success Criteria:**

- Both verification builds complete successfully.
- The two OCI manifest digests match perfectly (`allow-mismatch: false`).
- The evidence artifacts (`report.json`, `summary.md`) are uploaded as workflow artifacts.

**Failure Criteria:**

- Either build fails.
- The OCI manifest digests differ.
- **Enforcement:** A digest mismatch immediately halts the release pipeline. No production images are published or tagged.

**Emergency "Break-Glass" Procedure:**
In the event of a critical security hotfix (P0) where transient build anomalies cause a reproducibility failure, a designated repository administrator may trigger the release workflow manually with a specific `OVERRIDE_REPRODUCIBILITY_GATE=true` input. This override execution will be logged, flagged in the release notes, and automatically trigger a high-priority security review ticket to remediate the broken determinism post-incident.

## Historical Pilot Evidence Record

The following records validate the successful remediation of non-deterministic build steps, justifying the transition to a hard gate.

### 2026-05-13 Release Run: Backend Success

- Status: `pass`
- Comparison basis: `oci_manifest_digest`
- Manifest digest: `sha256:f5fb9044ff7288c358b20a3364ae680557ef457eaaf61d203cb1775331e9525d`
- Config digest: `sha256:9674628727e420ca9bebad04f1f6be527aa4e4e52ba47c3d7213be70a113c279`
- Layer count: `8` layers on `linux/amd64`
- Detailed comparison: All layer digests and config JSON fields matched perfectly with zero differences.

### 2026-05-13 Release Run: Worker Success

- Status: `pass`
- Comparison basis: `oci_manifest_digest`
- Manifest digest: `sha256:41c57efce43e7b5dbfe5c31b1548b235fb4d8c7b783866578bcb515ee9bbb0ca`
- Config digest: `sha256:1f748bc95099fd23ef975cecf911e8e734d04868864d99b582e356663f255131`
- Layer count: `8` layers on `linux/amd64`
- Detailed comparison: All layer digests and config JSON fields matched perfectly with zero differences.

### 2026-05-13 Release Run: Frontend Success

- Status: `pass`
- Comparison basis: `oci_manifest_digest`
- Manifest digest: `sha256:921dfab05edd042b96989d73392e95e1ce6b789dc5cf4aab3dc18b4c34b5bf32`
- Config digest: `sha256:30c2a01c246793bc92ccc16ebfdc641f88b5e1187b19bbbf0dc3f6fcd19e405b`
- Layer count: `12` layers on `linux/amd64`
- Detailed comparison: All layer digests and config JSON fields matched perfectly with zero differences.
