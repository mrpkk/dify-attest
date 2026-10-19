# attest — Dify tool plugin

Verify an AI agent artifact before you trust it or pay for it.

The plugin exposes one tool, **Verify artifact**, which posts the artifact to the
attest API and returns the verdict (`accept` / `review` / `reject`), the trust
score, violations/signals and an Ed25519-signed attestation that can be verified
without the service.

## Install

1. Build the package: `dify plugin package ./dify-attest`
2. In Dify: **Plugins → Install from local package** → pick `attest.difypkg`.
3. Configure the provider:
   - **API base URL** — defaults to `https://attest.rta.lat` (20 free checks/day).
   - **Entitlement token** — optional, for 30-day unlimited access
     (buy at https://attest.rta.lat/pricing).

## Tool parameters

| Parameter | Required | Meaning |
|---|---|---|
| `artifact` | yes | The artifact exactly as received, JSON-encoded (object, array or string) |
| `schema` | no | JSON Schema (JSON-encoded) the artifact must conform to |

## What it checks

- schema conformance (silent type/field changes);
- emptiness (placeholder or content-free output);
- prompt injection — positional: the same sentence in `description` and in
  `content` has different severity;
- provenance and authority (who signed the artifact, whether it is still valid).

## Honest limits

- The scanner recognises known classes; a clean result means "clean against these
  rules", not "safe".
- Free tier: 20 checks per day per IP on the hosted service; beyond that the API
  answers `402` with x402 payment instructions (USDC on Base).
- The checker decides; it never executes anything.

Links: https://attest.rta.lat · https://github.com/mrpkk/attest · MCP: https://attest.rta.lat/mcp
