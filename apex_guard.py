# -*- coding: utf-8 -*-
import math
import json
import hashlib
import numpy as np
from datetime import datetime, timezone

class CoreManifesto:
    @staticmethod
    def get_details():
        return {
            "toolkit": "FirstPrinciplesAI (ApexGuard)",
            "philosophy": [
                "Explainability by Design: Outputs are verifiable and interpretable without reverse engineering.",
                "First Principles: Solutions derived from fundamental mathematical laws rather than opaque heuristics.",
                "Cross-Domain Agnostic: Universal mathematics applied to secure and structure software pipelines."
            ]
        }

# 1. EntropyGuard (API Rate Limiting & Bot Anomaly Shield)
class EntropyGuard:
    @staticmethod
    def calculate_shannon_entropy(payload):
        if not payload:
            return 0.0
        payload_bytes = payload.encode('utf-8') if isinstance(payload, str) else payload
        length = len(payload_bytes)
        frequencies = {}
        for b in payload_bytes:
            frequencies[b] = frequencies.get(b, 0) + 1
        
        entropy = 0.0
        for count in frequencies.values():
            p = count / length
            entropy -= p * math.log2(p)
        return round(entropy, 4)

    @classmethod
    def audit_request(cls, payload_string, request_velocity_hz, threshold=4.5):
        entropy = cls.calculate_shannon_entropy(payload_string)
        is_bot = (entropy > threshold) or (request_velocity_hz > 15.0 and entropy < 1.5)

        return {
            "module": "EntropyGuard",
            "payload_size": len(payload_string.encode('utf-8')),
            "shannon_entropy": entropy,
            "velocity_hz": request_velocity_hz,
            "status": "QUARANTINED_BOT_ANOMALY" if is_bot else "FLUID_PASSTHROUGH",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

# 2. CodeDrift (B-STA Architectural Entropy & Siphon Auditor)
class CodeDriftAuditor:
    def __init__(self, lambda_core, v_overhead):
        self.lambda_core = np.array(lambda_core, dtype=float)
        self.v_overhead = np.array(v_overhead, dtype=float)

    def audit_architecture(self):
        m_baseline = np.diag(self.lambda_core)
        m_inflected = m_baseline @ self.v_overhead
        commutator = m_inflected - (self.v_overhead @ m_baseline)
        
        vortex_energy = float(np.linalg.norm(commutator))
        vortex_energy = round(vortex_energy, 4)

        baseline_potential = float(np.prod(np.abs(self.lambda_core)))
        if baseline_potential == 0.0:
            baseline_potential = 1e-9

        sigma = round(vortex_energy / baseline_potential, 4)

        return {
            "module": "CodeDrift",
            "siphon_metric_sigma": sigma,
            "internal_vortex_energy": vortex_energy,
            "architectural_state": "HEALTHY_DECOUPLING" if sigma < 1.0 else "CRITICAL_STRUCTURAL_TRAP"
        }

# 3. SchemaSync (Deterministic OpenAPI/Protobuf Diff Engine)
class SchemaSyncEngine:
    @staticmethod
    def generate_fingerprint(schema_hash):
        sorted_canonical = json.dumps(schema_hash, sort_keys=True)
        return hashlib.sha256(sorted_canonical.encode('utf-8')).hexdigest().upper()

    @classmethod
    def compare_specs(cls, old_spec, new_spec):
        old_fp = cls.generate_fingerprint(old_spec)
        new_fp = cls.generate_fingerprint(new_spec)

        breaking_changes = []
        for key, old_val in old_spec.items():
            if key in new_spec and new_spec[key] != old_val:
                breaking_changes.append(f"Field type/contract modified for '{key}': '{old_val}' -> '{new_spec[key]}'")
            elif key not in new_spec:
                breaking_changes.append(f"Required field deleted: '{key}'")

        return {
            "module": "SchemaSync",
            "old_fingerprint": old_fp[:16],
            "new_fingerprint": new_fp[:16],
            "status": "COMPATIBLE_TRANSITION" if not breaking_changes else "BREAKING_SCHEMA_DRIFT",
            "breaking_changes": breaking_changes
        }