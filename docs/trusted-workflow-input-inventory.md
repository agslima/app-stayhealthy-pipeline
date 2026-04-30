# Trusted Workflow Input Inventory

[//]: # (owner: Project Maintainers)
[//]: # (review_cadence: Quarterly)
[//]: # (last_reviewed: 2026-04-30)

This inventory records mutable external inputs in the repository's highest-trust workflows and the current control posture for each.

For this repository, the trusted workflow set is:

- `.github/workflows/ci-release-gate.yml`
- `.github/workflows/release-build-push-dual-registry.yml`
- `.github/workflows/release-trivy.yml`
- `.github/workflows/release-dast.yml`
- `.github/workflows/gitops-enforce.yml`

The goal is not to eliminate every external dependency immediately. The goal is to make each remaining mutable input explicit, minimize it where feasible, and give maintainers a documented next action.

## Immediate Reductions Applied

- GitHub Actions in trusted workflows are pinned by full commit SHA and checked by `scripts/check-workflow-input-provenance.py`.
- The GitOps workflow now fixes the Go toolchain lookup to `1.23.2` with `check-latest: false`, removing automatic drift to newer patch releases during trusted promotion runs.
- The ZAP runtime image in `release-dast.yml` is digest-pinned.
- Release and promotion image references use immutable digests rather than mutable tags.

## Inventory

| Workflow | Input | Source | Current control | Mutable risk | Current disposition | Recommended next action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `gitops-enforce.yml` | Go toolchain download for `actions/setup-go` | GitHub-hosted toolcache / upstream Go distribution | Action pinned by SHA; requested version pinned to `1.23.2`; `check-latest` disabled | Medium | Reduced and accepted for now | Revisit only if builder hardening work requires a mirrored toolchain source. |
| `gitops-enforce.yml` | `yq` binary download | GitHub release asset `mikefarah/yq` | Version pinned to `v4.44.3`; workflow now verifies the downloaded binary against the official release `checksums` asset before installation | Low to Medium | Reduced and accepted for now | Consider a mirrored/internal distribution path before any L3 claim if release-asset availability becomes a recurring operational risk. |
| `gitops-enforce.yml` | Release metadata lookup | GitHub Actions REST API | Source repository, workflow name, event, ref, and run conclusion are all validated before promotion proceeds | Low | Accepted and required | Keep fail-closed validation logic; no reduction planned unless metadata is exported as a signed release artifact later. |
| `release-build-push-dual-registry.yml` | Docker Buildx action and registry clients | GitHub Marketplace action + Docker/GHCR registries | Actions pinned by SHA; target images built from digest-pinned base images | Medium | Accepted and partially reduced | Keep base-image digests pinned; future hermeticity work should reduce live registry dependence for builds. |
| `release-build-push-dual-registry.yml` | `npm ci` during image build | npm registry via lockfile-resolved packages | `package-lock.json` constrains dependency graph; builds use `npm ci` | High | Accepted exception | Evaluate mirrored package source or prefetch strategy as part of hermeticity work. |
| `release-trivy.yml` | Trivy installer and vulnerability database | `aquasecurity/setup-trivy` and live vulnerability DB | Installer action pinned by SHA; version pinned to `v0.70.0`; scan output required and gate is fail-closed | Medium | Accepted exception | Consider Trivy DB mirroring if scanner availability becomes a repeated governance issue. |
| `release-dast.yml` | ZAP container image | GHCR image pull | Digest-pinned `ghcr.io/zaproxy/zaproxy@sha256:...` | Low | Reduced and accepted | Maintain periodic digest review cadence. |
| `ci-release-gate.yml` | SLSA generator reusable workflow | `slsa-framework/slsa-github-generator` | Pinned to tag `v2.1.0`, not full commit SHA | Medium | Accepted exception | Migrate to a commit-SHA-pinned reusable workflow ref if the generator release process supports it cleanly. |
| All trusted workflows | GitHub-hosted runner image | `ubuntu-latest` | Workflow logic assumes hosted CI trust boundary; `step-security/harden-runner` egress audit is enabled in release, scan, reproducibility-pilot, and GitOps promotion jobs; current non-claims are documented in `docs/builder-isolation-assumptions.md` | Medium | Accepted exception | Address in builder isolation/hardening phase rather than per-workflow patching. |

## Exception Review Notes

Inputs retained as accepted exceptions should be reviewed with these questions:

- Is the input version-pinned or digest-pinned?
- Is the upstream source authenticated or otherwise constrained?
- Does the workflow fail closed if the input is unavailable or malformed?
- Is there a practical mirrored or pre-fetched alternative that would reduce drift without harming delivery integrity?

## Next Reductions To Target

Priority order:

1. evaluate SHA-pinned or otherwise stronger immutability for the SLSA generator reusable workflow reference
2. design a mirrored package-source approach for `npm ci` in trusted release builds
3. consider a Trivy DB mirror only if scanner outages become an operational trend
4. consider a mirrored/internal distribution path for `yq` only if GitHub release-asset availability becomes a recurring problem
