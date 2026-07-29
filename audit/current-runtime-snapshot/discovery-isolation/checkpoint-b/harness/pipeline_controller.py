#!/usr/bin/env python3
"""Variant-blind downstream request builders and deterministic contract checks."""

from __future__ import annotations

import hashlib
import json
import secrets
from pathlib import Path
from typing import Any, Callable

import jsonschema


ROOT = Path("/private/tmp/readerlab-new-route-20260726/discovery-isolation/checkpoint-b")
SCHEMAS = ROOT / "protocol/schemas"
PROMPTS = ROOT / "protocol/prompts"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def load_schema(name: str) -> dict[str, Any]:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def validate_schema(instance: Any, schema_name: str) -> None:
    jsonschema.validate(instance, load_schema(schema_name))


def count_display_codepoints(text: str) -> int:
    return sum(1 for character in text if not character.isspace())


def random_blind_id(prefix: str, byte_count: int = 8) -> str:
    return f"{prefix}-{secrets.token_hex(byte_count).upper()}"


def build_normalizer_input(
    source_text_en: str,
    seed_batch: dict[str, Any],
    set_blind_id: str,
    material_blind_id: str,
) -> dict[str, Any]:
    sanitized_batch = {
        "schema_version": "seed-batch.v0.1",
        "run_id": set_blind_id,
        "seeds": seed_batch["seeds"],
    }
    payload = {
        "schema_version": "normalizer-input.v0.1",
        "set_blind_id": set_blind_id,
        "material_blind_id": material_blind_id,
        "source_text_en": source_text_en,
        "seed_batch": sanitized_batch,
    }
    validate_schema(payload, "normalizer-input.schema.json")
    return payload


def validate_normalizer_output(
    output: dict[str, Any], input_seed_ids: list[str], set_blind_id: str
) -> None:
    validate_schema(output, "normalizer-output.schema.json")
    if output["set_blind_id"] != set_blind_id:
        raise ValueError("Normalizer set_blind_id mismatch")
    output_ids = [card["source_seed_id"] for card in output["cards"]]
    if output_ids != input_seed_ids:
        raise ValueError("Normalizer must preserve exact seed order and cardinality")
    for card in output["cards"]:
        if card["status"] == "VALID":
            actual = count_display_codepoints(card["display_card_zh"])
            if not 240 <= actual <= 280:
                raise ValueError("VALID display card is outside 240–280 code points")
            if card["display_char_count"] != actual:
                raise ValueError("Normalizer display_char_count mismatch")


def build_judge_input(
    source_text_en: str,
    normalizer_output: dict[str, Any],
    set_blind_id: str,
    material_blind_id: str,
    id_factory: Callable[[str], str] = random_blind_id,
) -> tuple[dict[str, Any], dict[str, str]]:
    cards = []
    sealed_mapping = {}
    for card in normalizer_output["cards"]:
        if card["status"] != "VALID":
            continue
        blind_card_id = id_factory("J")
        cards.append(
            {
                "blind_card_id": blind_card_id,
                "display_card_zh": card["display_card_zh"],
            }
        )
        sealed_mapping[blind_card_id] = card["source_seed_id"]
    payload = {
        "schema_version": "judge-input.v0.1",
        "set_blind_id": set_blind_id,
        "material_blind_id": material_blind_id,
        "source_text_en": source_text_en,
        "cards": cards,
    }
    validate_schema(payload, "judge-input.schema.json")
    return payload, sealed_mapping


def validate_judge_output(
    output: dict[str, Any], judge_input: dict[str, Any]
) -> None:
    validate_schema(output, "judge-output.schema.json")
    if output["set_blind_id"] != judge_input["set_blind_id"]:
        raise ValueError("Judge set_blind_id mismatch")
    expected = [card["blind_card_id"] for card in judge_input["cards"]]
    actual = [judgment["blind_card_id"] for judgment in output["judgments"]]
    if actual != expected:
        raise ValueError("Judge must preserve exact card order and cardinality")
    for judgment in output["judgments"]:
        should_pass = (
            judgment["hard_kill"] == "NONE"
            and all(judgment["rubric"].values())
        )
        if (judgment["decision"] == "PASS") != should_pass:
            raise ValueError("Judge PASS is inconsistent with frozen hard-kill/rubric")


def build_cluster_input(
    material_blind_id: str,
    passed_cards: list[dict[str, str]],
) -> dict[str, Any]:
    payload = {
        "schema_version": "cluster-input.v0.1",
        "material_blind_id": material_blind_id,
        "cards": passed_cards,
    }
    validate_schema(payload, "cluster-input.schema.json")
    return payload


def validate_cluster_output(
    output: dict[str, Any], cluster_input: dict[str, Any]
) -> None:
    validate_schema(output, "cluster-output.schema.json")
    if output["material_blind_id"] != cluster_input["material_blind_id"]:
        raise ValueError("Cluster material_blind_id mismatch")
    expected = sorted(card["blind_card_id"] for card in cluster_input["cards"])
    actual = sorted(
        member
        for cluster in output["clusters"]
        for member in cluster["member_card_ids"]
    )
    if actual != expected:
        raise ValueError("Clusters must be a strict partition of input card IDs")


def select_representatives(
    clusters: list[dict[str, Any]],
    sealed_candidates: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Select one representative independently for each cluster and internal cohort."""
    selected = []
    for cluster in clusters:
        by_cohort: dict[str, list[dict[str, Any]]] = {}
        for blind_id in cluster["member_card_ids"]:
            candidate = sealed_candidates[blind_id]
            by_cohort.setdefault(candidate["cohort"], []).append(candidate)
        for cohort, candidates in sorted(by_cohort.items()):
            chosen = min(
                candidates,
                key=lambda candidate: (
                    -len(candidate["raw_seed"]["source_leads"]),
                    candidate["run_sequence"],
                    int(candidate["raw_seed"]["seed_id"][1:]),
                    canonical_sha256(candidate["raw_seed"]),
                ),
            )
            selected.append(
                {
                    "cluster_id": cluster["cluster_id"],
                    "cohort": cohort,
                    "candidate": chosen,
                }
            )
    return selected


def build_verifier_input(
    verification_id: str,
    material_blind_id: str,
    source_text_en: str,
    blind_card_id: str,
    raw_seed: dict[str, Any],
    display_card_zh: str,
) -> dict[str, Any]:
    payload = {
        "schema_version": "verifier-input.v0.1",
        "verification_id": verification_id,
        "material_blind_id": material_blind_id,
        "source_text_en": source_text_en,
        "representative": {
            "blind_card_id": blind_card_id,
            "source_anchor_quote_en": raw_seed["source_anchor_quote_en"],
            "external_lens_identity": raw_seed["external_lens_identity"],
            "mechanism_claim_zh": raw_seed["mechanism_claim_zh"],
            "reread_delta_zh": raw_seed["reread_delta_zh"],
            "source_leads": raw_seed["source_leads"],
            "display_card_zh": display_card_zh,
        },
    }
    validate_schema(payload, "verifier-input.schema.json")
    return payload


def validate_verifier_output(output: dict[str, Any], verification_id: str) -> None:
    validate_schema(output, "verifier-output.schema.json")
    if output["verification_id"] != verification_id:
        raise ValueError("Verifier verification_id mismatch")
    should_be_eligible = (
        output["status"] == "VERIFIED"
        and output["anchor_status"] == "SUPPORTED"
        and output["mechanism_status"] == "SUPPORTED"
        and output["attribution_status"] == "ACCURATE"
        and any(
            source["retrieval_status"] in {"OPENED_PRIMARY", "OPENED_AUTHORITATIVE"}
            and source["supports_claim"] is True
            for source in output["source_checks"]
        )
    )
    if output["technical_eligible"] != should_be_eligible:
        raise ValueError("Verifier technical_eligible is inconsistent")
    if output["status"] == "UNKNOWN_TOOLING" and output["technical_eligible"]:
        raise ValueError("UNKNOWN_TOOLING cannot be technically eligible")


def build_product_pack(
    display_cards: list[str],
    id_factory: Callable[[str], str] = random_blind_id,
) -> tuple[dict[str, Any], dict[str, int]]:
    pack = {
        "schema_version": "product-pack.v0.1",
        "pack_blind_id": id_factory("PACK"),
        "cards": [],
    }
    sealed_mapping = {}
    for index, display_card in enumerate(display_cards):
        if not 240 <= count_display_codepoints(display_card) <= 280:
            raise ValueError("Product card is outside 240–280 code points")
        blind_id = "P-" + secrets.token_hex(6).upper()
        pack["cards"].append(
            {
                "blind_id": blind_id,
                "display_card_zh": display_card,
                "owner_response": None,
            }
        )
        sealed_mapping[blind_id] = index
    validate_schema(pack, "product-pack.schema.json")
    return pack, sealed_mapping


def render_stage_request(stage: str, payload: dict[str, Any]) -> bytes:
    paths = {
        "normalizer": PROMPTS / "normalizer.md",
        "judge": PROMPTS / "technical-judge.md",
        "clusterer": PROMPTS / "clusterer.md",
        "verifier": PROMPTS / "verifier.md",
    }
    marker = {
        "normalizer": "{{SANITIZED_INPUT_JSON}}",
        "judge": "{{SANITIZED_INPUT_JSON}}",
        "clusterer": "{{SANITIZED_INPUT_JSON}}",
        "verifier": "{{SANITIZED_INPUT_JSON}}",
    }[stage]
    template = paths[stage].read_text(encoding="utf-8")
    if template.count(marker) != 1:
        raise ValueError(f"{stage} prompt marker drift")
    validate_schema(
        payload,
        {
            "normalizer": "normalizer-input.schema.json",
            "judge": "judge-input.schema.json",
            "clusterer": "cluster-input.schema.json",
            "verifier": "verifier-input.schema.json",
        }[stage],
    )
    return template.replace(
        marker, json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    ).encode("utf-8")
