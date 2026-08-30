# ReviewSignal

> Experimental AI code-review system investigating whether developer-process telemetry can improve review prioritization.

## Status

🚧 V0 — Experimental validation

This project is currently testing a hypothesis:

> Can development-process signals provide useful information for AI-assisted code review that cannot be derived from the final code diff alone?

## Current experiment

ReviewSignal compares two approaches:

1. **Baseline** — repository + pull request + code diff
2. **Process-aware** — baseline context + developer-process telemetry

The goal is to determine whether the additional process signal improves review prioritization.

## Important

This is a research experiment, not a production code-review tool yet.