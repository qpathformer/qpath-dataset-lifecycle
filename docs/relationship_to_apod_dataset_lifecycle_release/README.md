# Relationship Documents

This directory contains reference documents that describe the
governance and architectural context of this repository.

These documents are provided for informational purposes and do
not define the governance semantics of the repository itself.

## Included documents

### APOD-TR-007 — Governed Dataset Onboarding and Lifecycle Routing

Defines the governance framework for converting inspection
artifacts into machine-readable datasets while preserving
provenance, authorization scope, and lifecycle state.

This repository implements reference tooling compatible with
the dataset lifecycle model described in this document.

### QPATH-ARCH-001 — Q-Pathformer Multi-State Machine Learning Architecture

Describes the conceptual architecture of the Q-Pathformer
multi-state machine learning system.

This document is provided as an architectural reference and
does not define governance authority for dataset lifecycle
processing.

## Governance Boundary

The governance semantics for dataset lifecycle management are
defined exclusively by the Access-PoD publications.

Execution environments such as Q-Pathformer may consume
governed datasets but do not determine lifecycle state,
authorization scope, or governance authority.