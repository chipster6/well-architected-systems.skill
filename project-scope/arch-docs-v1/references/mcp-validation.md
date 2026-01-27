# MCP Validation Matrix (CloudRail Arch Docs v2)

This file mandates exactly which MCP tools to call and when.

## Tool Catalog (exact names)
- aws-docs: `search_documentation`, `read_documentation`, `recommend`
- context7: `resolve-library-id`, `get-library-docs`
- terraform-awslabs (AWS Terraform MCP): `ExecuteTerraformCommand`, `ExecuteTerragruntCommand`, `RunCheckovScan`, `SearchAwsProviderDocs`, `SearchAwsccProviderDocs`, `SearchSpecificAwsIaModules`, `SearchUserProvidedModule`
- terraform-hashicorp: `search_providers`, `get_provider_details`, `get_provider_capabilities`, `get_latest_provider_version`, `search_modules`, `get_module_details`, `get_latest_module_version`, `search_policies`, `get_policy_details`
- cdk: `CDKGeneralGuidance`, `CheckCDKNagSuppressions`, `ExplainCDKNagRule`, `GetAwsSolutionsConstructPattern`, `LambdaLayerDocumentationProvider`, `SearchGenAICDKConstructs`

## PRE-FLIGHT (before drafting)
- ADRs (service selection / orchestration / datastore):
  - aws-docs: service semantics, limits/quotas, regional availability, security guidance.
  - terraform-hashicorp + terraform-awslabs: confirm provider/module capability if Terraform is mentioned.
  - cdk: `CDKGeneralGuidance` + construct pattern if CDK path is mentioned.
- Workflows (Step Functions + runners): aws-docs for Step Functions semantics/limits, retries/timeouts, integrations used.
- Datastores: aws-docs for Object Lock/KMS/encryption/retention/residency for chosen services.
- Dependencies/libraries: context7 `resolve-library-id` + `get-library-docs` for mandated SDK/CLI/library.

## POST-FLIGHT (after drafting)
- Terraform claims: terraform-hashicorp to confirm latest versions/capabilities for pinned providers/modules; terraform-awslabs `RunCheckovScan` if Terraform examples/modules are present and can be scanned.
- CDK claims: cdk `ExplainCDKNagRule` for any cdk-nag references; `CheckCDKNagSuppressions` guidance if suppressions discussed.
- AWS feasibility: aws-docs to re-check limits/quotas if document asserts scaling/throughput boundaries.

## Doc-Type Mapping (authoritative)
- ADR / ARC / SERVICE / WORKFLOW:
  - Preflight: aws-docs service semantics/limits; add terraform-hashicorp + terraform-awslabs if Terraform is mentioned; add cdk guidance if CDK is mentioned; context7 for SDK/library calls.
  - Postflight: aws-docs limits recheck; terraform-hashicorp version/capability confirmation; terraform-awslabs `RunCheckovScan` when Terraform snippets exist; cdk nag rule validation if referenced.
- DM / DCON / API:
  - Preflight: aws-docs for datastore/service limits; terraform-hashicorp + terraform-awslabs if IaC is referenced; context7 for SDK/library docs.
  - Postflight: aws-docs limits recheck; terraform-hashicorp latest versions/capabilities for providers/modules referenced.
- SEC / OBS / DR / RUN:
  - Preflight: aws-docs for IAM/STS/KMS/Object Lock/monitoring/service limits relevant to the document.
  - Postflight: aws-docs to confirm any asserted quotas or performance claims.
- GOV / REF:
  - Preflight: aws-docs when cloud behaviors are asserted; context7 for library/SDK references.
  - Postflight: aws-docs to confirm any normative claims about limits or behaviors.

## Normative Claim Rules
- Every normative AWS/Terraform/CDK/library claim must map to an `MCP_EVIDENCE_LOG.md` entry.
- Each entry must use `evidence_id` format `MCP-YYYYMMDD-NNNN` and be cited in References.
- If required MCP tools are unavailable: mark affected sections `UNVERIFIED EXTERNALLY` and block acceptance until validated.

## Timing Enforcement
- Do not begin drafting normative sections until PRE-FLIGHT calls are logged.
- Do not mark a document complete until POST-FLIGHT validations are logged and mapped to claims.
