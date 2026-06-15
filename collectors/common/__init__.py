"""Shared collector utilities (Handoff #36).

Cross-collector helpers that neither the OGE 278 nor the ADV/IAPD package owns.
The first member is :mod:`candidate_writer`, the source-scoped, merge-aware writer
both collectors call so they coexist in one ``web/data/candidates.json`` without
overwriting each other's rows.
"""
