# Provider Safety Matrix

## Rule

Real student data must not be sent to Gemini free tier or any provider not explicitly approved for pilot use.

## Providers

| Provider | Recommended Use | Real Student Data | Notes |
|---|---|---:|---|
| Gemini Flash free tier | synthetic dev only | No | Free-tier data policy is not suitable for real student pilot data. |
| Groq free tier | synthetic dev only | No | Good for speed tests, not for sensitive pilot data. |
| OpenAI / Claude cloud | possible paid eval only | Not by default | Requires explicit policy/legal review before real data. |
| Ollama local | pilot candidate | Yes, if local machine is controlled | Preferred for GIIS micro-pilot. |
| DeepSeek | future Jieni/China evaluation | TBD | Must review PIPL/data residency before use. |

## v0.7 Exit Criteria

- Local/private provider path documented.
- `.env` clearly warns against real data in dev cloud providers.
- Default tests do not require external API keys.
- End-to-end smoke path can run without exposing real student data to a cloud provider.

