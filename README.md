# attest — Dify tool plugin

Verify an AI agent artifact (schema, prompt injection, provenance, authority)
before you trust it or act on it.

- Source repository: https://github.com/mrpkk/dify-attest
- Contact: https://github.com/mrpkk
- Privacy policy: [PRIVACY.md](PRIVACY.md)

## Install

1. Build the package: `dify plugin package ./dify-attest`
2. In Dify: **Plugins → Install from local package**, pick `attest.difypkg`.
3. Configure the provider:
   - **API base URL** — defaults to `https://attest.rta.lat` (the hosted service).
   - **Entitlement token** — optional; leave empty to use the hosted free tier.

## Usage

Add the **Verify artifact** tool to an Agent or a Workflow node and pass:

| Parameter | Required | Meaning |
|---|---|---|
| `artifact` | yes | The artifact exactly as received, JSON-encoded (object, array or string) |
| `schema` | no | JSON Schema (JSON-encoded) the artifact must conform to |

The tool returns a JSON result: `verdict` (`accept` / `review` / `reject`),
`trust_score`, `violations`, `signals`, and an Ed25519-signed attestation that
can be verified without the service.

## What it checks

- schema conformance (silent type/field changes);
- emptiness (placeholder or content-free output);
- prompt injection — positional: the same sentence in a tool's `description`
  and in its `content` has different severity;
- provenance and authority (who signed the artifact, whether it is still valid).

## Configuration

The plugin talks to the API base URL you configure. Nothing else is contacted.
Artifacts are not stored by the plugin.

## Self-hosting

The service is open source (Apache-2.0): https://github.com/mrpkk/attest
Set **API base URL** to your own deployment to keep all data inside your
infrastructure.

## Limits

The hosted service applies a per-IP daily allowance to keep the free tier
sustainable; the tool returns the service's response as data when the
allowance is used up. Self-hosting removes this limit.
