# Toolchain Baseline (Baseline)

## Purpose
Define the baseline toolchain assumptions used by documentation, validation, and future implementation planning.

## Current toolchain selections
These are the current baseline settings reflected in `docs/baseline/baseline_manifest.json`:
- Kubernetes: not in scope (baseline default)
- Terraform: not in scope (baseline default)
- AWS CDK: not in scope (baseline default)

## Implications
- Documentation and gates must not assume Kubernetes primitives unless an ADR updates the baseline.
- Implementation strategy should express tasks in provider-native terms first (AWS, per ADR), and only introduce IaC tooling via ADR + toolchain update.

