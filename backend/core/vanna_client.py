"""
vanna_client.py — Thin wrapper. All Vanna logic lives in vanna_bridge.py.
This file kept for backward compatibility with any existing imports.
"""
from core.vanna_bridge import get_vanna, train_if_needed, generate_sql

__all__ = ["get_vanna", "train_if_needed", "generate_sql"]
