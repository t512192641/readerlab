from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[1]
CONTRACTS = WORKSPACE / "contracts"

CURRENT_CONTRACT_PATH = "contracts/BOOK-CONTENT-FLOW-v2.md"
CURRENT_CONTRACT = WORKSPACE / CURRENT_CONTRACT_PATH
CURRENT_RECEIPT_PATH = "contracts/BOOK-CONTENT-FLOW-v2-freeze-receipt.md"
CURRENT_RECEIPT = WORKSPACE / CURRENT_RECEIPT_PATH
PIPELINE_MAP = WORKSPACE / "blueprints" / "PIPELINE-MAP.md"
GLOSSARY = CONTRACTS / "GLOSSARY.md"
ASSET_REGISTER = WORKSPACE / "audit" / "ASSET-LIFECYCLE-REGISTER.md"
M1_RECEIPT = CONTRACTS / "M1-freeze-receipt.md"

CURRENT_CONTRACT_SHA256 = (
    "daf2e546ec84715481746056abb7ed58110468ec64d424c440600139cca67e91"
)
CURRENT_CONTRACT_BYTES = 21_930

LEGACY_EVIDENCE_SHA256 = {
    "M1-freeze-receipt.md": (
        "6dd5ce00a3a0c14e0c2dc8036e7543c113d885a986b6c393025d60e1e5432aa1"
    ),
    "T1.3-discovery.md": (
        "c56377d70861237f39d773ba414c4080d7a2e163962d256e98a0faf388b05178"
    ),
    "T1.4-expert-and-knowledge-card.md": (
        "979cf646150b4085ae36d47104261ad76e22fbce986313cbad57e89f511b8048"
    ),
    "T1.5-independent-review.md": (
        "aa55e7f1136f9fa59577134c1ead5f675042a33900a8db9b78d4f7002d932de8"
    ),
    "T1.6-writer.md": (
        "79a15346dea8d90bbde1f14bdb9fc7b966cd38438ed0eed357b8da4ac7190129"
    ),
    "T1.7-b2-assembly.md": (
        "6bbaaae335c2737a543b791118c2dddc44afe78e861e8df956eeb96728b9b474"
    ),
}


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return {}

    result: dict[str, str] = {}
    for line in lines[1:]:
        if line == "---":
            return result
        key, separator, value = line.partition(":")
        if separator:
            result[key.strip()] = value.strip()
    return {}


def _receipt_identity(
    receipt: str,
    contract_path: str,
) -> tuple[str, int] | None:
    matching_rows: list[list[str]] = []
    for line in receipt.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [
            cell.strip().strip("`")
            for cell in line.strip().strip("|").split("|")
        ]
        if contract_path not in cells:
            continue
        matching_rows.append(cells)

    if len(matching_rows) != 1 or matching_rows[0].count(contract_path) != 1:
        return None

    hashes = [
        cell for cell in matching_rows[0] if re.fullmatch(r"[0-9a-f]{64}", cell)
    ]
    byte_counts = [
        int(cell) for cell in matching_rows[0] if re.fullmatch(r"[0-9]+", cell)
    ]
    if len(hashes) != 1 or len(byte_counts) != 1:
        return None
    return hashes[0], byte_counts[0]


def _markdown_link_targets(markdown: str) -> set[str]:
    return set(re.findall(r"\[[^\]]+\]\(([^)\s]+)\)", markdown))


class BookContentFlowContractTests(unittest.TestCase):
    def test_legacy_m1_interface_evidence_keeps_frozen_bytes(self) -> None:
        for filename, expected_sha256 in LEGACY_EVIDENCE_SHA256.items():
            with self.subTest(filename=filename):
                self.assertEqual(
                    _sha256((CONTRACTS / filename).read_bytes()),
                    expected_sha256,
                )

    def test_current_contract_has_frozen_identity_and_long_term_scope(self) -> None:
        payload = CURRENT_CONTRACT.read_bytes()
        metadata = _frontmatter(CURRENT_CONTRACT)

        self.assertEqual(metadata.get("status"), "frozen")
        self.assertEqual(metadata.get("scope"), "long-term")
        self.assertEqual(_sha256(payload), CURRENT_CONTRACT_SHA256)
        self.assertEqual(len(payload), CURRENT_CONTRACT_BYTES)

    def test_freeze_receipt_uniquely_binds_current_contract_identity(self) -> None:
        receipt = CURRENT_RECEIPT.read_text(encoding="utf-8")

        self.assertEqual(
            _receipt_identity(receipt, CURRENT_CONTRACT_PATH),
            (CURRENT_CONTRACT_SHA256, CURRENT_CONTRACT_BYTES),
        )

    def test_pipeline_current_pointer_links_contract_and_receipt(self) -> None:
        pipeline_map = PIPELINE_MAP.read_text(encoding="utf-8")
        targets = _markdown_link_targets(pipeline_map)

        self.assertEqual(pipeline_map.count("current-book-content-flow-contract"), 1)
        self.assertIn("../" + CURRENT_CONTRACT_PATH, targets)
        self.assertIn("../" + CURRENT_RECEIPT_PATH, targets)

    def test_pipeline_contract_registry_covers_current_and_historical_scopes(
        self,
    ) -> None:
        pipeline_map = PIPELINE_MAP.read_text(encoding="utf-8")
        targets = _markdown_link_targets(pipeline_map)

        current_contracts = {
            "../contracts/T1.1-material-intake.md": "现行上游节点",
            "../contracts/T1.2-b1-source.md": "现行上游节点",
            "../contracts/BOOK-CONTENT-FLOW-v2.md": "现行内容流",
            "../contracts/T1.8-independent-acceptance.md": "现行下游验收语义",
        }
        for target, status in current_contracts.items():
            with self.subTest(target=target):
                self.assertIn(target, targets)
                matching_rows = [
                    line
                    for line in pipeline_map.splitlines()
                    if f"]({target})" in line
                    and f"| `{status}` |" in line
                ]
                self.assertEqual(
                    len(matching_rows),
                    1,
                    f"expected one registry row for {target}",
                )

        self.assertIn(
            "`contracts/T1.3-discovery.md`—`contracts/T1.7-b2-assembly.md`",
            pipeline_map,
        )
        self.assertIn("`历史接口`", pipeline_map)

    def test_legacy_glossary_keeps_frozen_identity_and_current_terms_use_v2(
        self,
    ) -> None:
        glossary_hash = _sha256(GLOSSARY.read_bytes())
        receipt = M1_RECEIPT.read_text(encoding="utf-8")
        current_contract = CURRENT_CONTRACT.read_text(encoding="utf-8")
        pipeline_map = PIPELINE_MAP.read_text(encoding="utf-8")

        self.assertEqual(
            glossary_hash,
            "333b3eb4840cea16b7f5049fe7a8dbba09ddedb4ecb2b37479c1c13129737844",
        )
        self.assertIn(glossary_hash, receipt)
        self.assertIn("Writer 的组织单位是获准的完整 Expert 初稿", current_contract)
        self.assertIn("不是知识卡", current_contract)
        self.assertIn("M1 历史术语表", pipeline_map)

    def test_asset_lifecycle_keeps_current_node_contracts_out_of_history(
        self,
    ) -> None:
        register = ASSET_REGISTER.read_text(encoding="utf-8")
        current_section = register.split(
            "### 现行节点合同与项目专用能力",
            1,
        )[1].split("### 支持性参考", 1)[0]
        historical_section = register.split(
            "### 历史合同、路线、专题文档与透镜资产",
            1,
        )[1].split("### 历史诊断", 1)[0]

        for path in (
            "contracts/T1.1-material-intake.md",
            "contracts/T1.2-b1-source.md",
            "contracts/T1.8-independent-acceptance.md",
        ):
            with self.subTest(path=path):
                self.assertIn(path, current_section)
                self.assertNotIn(path, historical_section)
        self.assertIn("contracts/GLOSSARY.md", historical_section)


if __name__ == "__main__":
    unittest.main()
