---
title: 'LLMs Are Not Just an Inference Layer: What We Learned While Building Observability in Microservices'
description: 'A concise, production-focused set of lessons learned while adding observability to LLMs across microservices.'
pubDate: '2026-06-05'
heroImage: '../../assets/images/blog/Blog Header LLM.png'
---

The first time we added an LLM call to a microservice, the architecture looked simple and elegant:
call the model → get a response → return it.

That was enough to prove the feature. The first demo worked, and the users were happy with the output.
We shipped it the normal way, then went back and analyzed what production behavior exposed.
That retrospective view showed the model call was only one part of the problem; the rest of the system had to be treated as part of the same workflow.

## 1. Where We Started

Like many teams, our initial integration was straightforward:
- call the model — send the user prompt and assembled context to the LLM and wait for the result.
- capture the response — collect the generated output so the service could continue processing.
- return the output from the microservice — deliver an answer back to the caller with minimal latency.

This was not a greenfield platform design. It was a feature built into an existing microservice landscape, and we learned from real production usage.

Then we built a few basic capabilities around it:
- capturing token consumption for every LLM request, so we could later attribute cost to specific features and understand how prompt changes impacted spend.
- storing responses in an indexed trace store (OpenSearch) for audits, searchable history, and postmortem investigation.
- implementing prompt versioning so prompts could be selected dynamically by version without redeploying code or changing service logic.

At that stage, the setup felt effective. It gave us enough control and visibility to iterate, and it allowed us to validate the first generation of the feature in production.

## 2. The Problems Started Emerging

As usage grew across multiple services, the missing pieces began to show.

###  Problem 1: Lack of End-to-End Traceability

We could track token usage.
We could store individual responses.

But we could not reliably answer:
- which user request triggered which LLM call? — we lacked the linkage between incoming API requests and downstream model invocations.
- what data or context was used for that call? — we could not tell whether the model saw the same retrieval document or prompt state each time.
- which service path produced that output? — there was no clear trace across microservices to show where the request traveled.

That meant when a business user complained that the assistant returned stale information, we had to manually reconstruct the flow from logs and guess which version of the prompt and context had been used.
Observability existed, but only in fragments. It was not a unified trace.

###  Problem 2: Tight Coupling Across Microservices

Each microservice implemented:
- its own prompt selection logic, often using slightly different rules for the same use case.
- its own tracking mechanisms, meaning the telemetry was inconsistent across services.

That led to:
- duplicated implementation, with the same feature repeated in many repositories.
- inconsistent behavior, since each service could decide differently under load or failure.
- higher maintenance overhead, because changes had to be propagated through many code paths.

In practice, that meant one team would update their prompt strategy and another would still be using the old semantics. The result was confusing behavior for the product and longer incident response times.

###  Problem 3: Prompt Management Didn’t Scale

Prompt versioning worked at first, but it lacked a platform:
- no centralized prompt registry, so teams managed versions in different places.
- no structured experimentation, making it difficult to compare prompt changes objectively.
- no clean rollback or A/B testing, so mistakes were harder to reverse safely.

This was the first time we understood that prompts are not just code strings. They are product assets that need lifecycle management, audit history, and quality controls.

###  Problem 4: Observability Was Partial

We had:
- cost visibility  — we knew how many tokens were being spent.
- response storage  — we kept the outputs for later review.

But we were missing:
- request-level correlation — we could not link the model call to the originating business request.
- latency insights — we lacked metrics for where time was spent in the LLM path.
- failure tracking — errors were often visible only as generic failures.
- feedback loops — there was no formal way to close the loop on bad model outputs.

Without those signals, production debugging was still difficult. A single bad response could trigger a lengthy investigation because the team had to trace across multiple services and storage systems to reconstruct what happened.

###  The Key Realization

At this point, we needed a fundamental shift in thinking.

LLMs are not just another API dependency.
They introduce:
- probabilistic behavior
- cost sensitivity
- dependency on evolving context
- operational complexity

###  Additional production issues we observed

- **Prompt sensitivity:** small prompt tweaks produced large deviations in output. Mitigation: treat prompts as experimental assets, run small controlled canaries, and roll changes out gradually.
- **Intermittent correctness:** the same prompt sometimes worked and sometimes failed. Mitigation: add validation checks and guardrails, and record confidence/diagnostics for each call.
- **Stale or wrong outputs:** occasionally the system returned an older result for the same input. Mitigation: include freshness metadata in context and add strict cache invalidation rules.
- **Hard to test generated output:** judging correctness required human review and fuzzy criteria. Mitigation: create golden datasets, automated semantic tests (embedding similarity, unit prompts), and acceptance checks.
- **Redundant model calls:** we hit the LLM repeatedly for identical inputs and wasted tokens. Mitigation: caching responses keyed by prompt+context fingerprint and deduplicating requests.
- **High latency:** some model calls took too long for synchronous UX. Mitigation: use faster/smaller models for low-cost paths, or serve async responses and notify callers.
- **JSON token overhead:** posting huge JSON payloads (with double quotes) inflated token consumption. Mitigation: send compact text templates, avoid serializing large JSON into prompt bodies, or use shorter encodings.
- **Missing model attribution:** we did not log which model/version produced the output. Mitigation: record model name, version, and endpoint per trace.
- **Prompt templates managed in code:** templates lived in source rather than a registry. Mitigation: move prompts to a central versioned registry with audit history.

## 3. Rethinking the Architecture

Instead of treating the LLM as an inference layer, it is more accurate to treat it as an intelligence layer integrated across microservices.

This means the model is not just a dependency that gets called from the nearest service. It becomes a platform capability with its own orchestration, prompt lifecycle, and observability contract.

## 4. A More Mature Architecture

A more scalable architecture looks like this:

![AI observability architecture](../../assets/images/blog/Architeture.png)

The first time we added an LLM call to a microservice, it behaved like any other dependency: call the model, return the response. The demo worked, we shipped, and then we reviewed what production revealed.

This post is a concise, production-focused summary of the lessons we learned while instrumenting LLMs across a microservice architecture. Below are the pragmatic takeaways that guided our redesign and the concrete changes we'd make if we started again.

## Lessons Learned — Executive Summary

- Treat prompts as product assets, not inline strings. They need versioning, tests, and rollout controls.
- Observe the whole request path: from API request → orchestrator → model → response — nothing short of end-to-end traces will do.
- Make model attribution and token accounting first-class telemetry so behavior, cost, and model changes can be correlated.
- Cache and deduplicate identical calls to reduce unnecessary token spend.
- Design for latency: use staged fallbacks, async flows, or smaller models where UX requires responsiveness.

## 1. What We Shipped and Why It Felt Right

We integrated an LLM into an existing service to solve a clear product need. Initial controls were pragmatic:
- token accounting to understand cost
- indexed response storage (OpenSearch) for audits
- prompt version flags to change behavior without full deploys

These steps were necessary and useful, but insufficient at scale.

## 2. Where It Broke in Production

- Lack of end-to-end traceability: we could not link user requests to model calls reliably, which slowed incident response.
- Tight coupling: each service managed prompts and telemetry differently, creating duplication and drift.
- Prompt fragility: small prompt edits caused disproportionate output changes, and intermittent failures were hard to reproduce.
- Testing and regression: validating generated outputs required human judgment; we lacked automated semantic tests.
- Cost and performance: repeated identical calls, large JSON payloads, and slow model responses increased cost and worsened UX.

## 3. Concrete Changes We Implemented (and Recommend)

- Centralize orchestration: introduce an AI Orchestrator that decides model selection, retries, and routing, and emits structured traces.
- Centralize prompt management: move templates to a versioned registry with metadata, tests, and a rollout mechanism.
- Add model attribution: every trace records model name, version, and endpoint.
- Instrument full traces: use OpenTelemetry-compatible traces and export key fields to Langfuse or your trace store.
- Cache/dedupe: fingerprint prompt+context to avoid redundant model calls; use short TTLs for cached responses.
- Reduce token overhead: avoid embedding large JSON; use compact templates or pass context via retrieval (RAG).
- Automated validation: maintain golden datasets and use embedding-based similarity checks for regression detection.
- Staged rollouts and canaries: release prompt changes to a small percentage of traffic and monitor correctness and cost.

## 4. Architecture (Practical View)

API Gateway → Services → AI Orchestrator → [Prompt Registry, RAG, Guardrails] → LLM → Observability (traces + metrics)

The orchestrator is the single decision point; prompt templates and retrieval live outside business services so they can be audited, versioned, and tested independently.

## 5. Tools We Used

- Orchestration: [LangChain](https://python.langchain.com/en/latest/), [LlamaIndex](https://www.llamaindex.ai/docs/)
- Observability: [Langfuse](https://www.langfuse.io/), [OpenTelemetry](https://opentelemetry.io/)
- Prompt management & experiments: [MLflow](https://mlflow.org/docs/latest/index.html), Langfuse prompt tracking
- Retrieval: [OpenSearch](https://opensearch.org/), [FAISS](https://faiss.ai/), [Pinecone](https://www.pinecone.io/)

## 6. AWS Deployment Notes

- Bedrock for managed model endpoints and simplified scaling ([Amazon Bedrock](https://aws.amazon.com/bedrock/)).
- SageMaker for fine-tuning and custom hosting when domain accuracy required it ([Amazon SageMaker](https://aws.amazon.com/sagemaker/)).

## 7. Practical Checklist (If You Ship This Tomorrow)

- Start with end-to-end traces and model attribution.
- Move prompts out of service code into a registry and add tests.
- Add caching for identical requests and avoid large JSON in prompts.
- Automate semantic regression tests and run them pre-rollout.
- Deploy changes as canaries and monitor token & correctness metrics.

## Final Thought

Shipping an LLM-based feature is easy; operating it reliably at scale is the hard part. The pragmatic changes above convert an ad-hoc feature into an operable platform capability: measurable, auditable, and safe.

