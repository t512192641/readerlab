import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_readerlab_package.py"


def run_builder(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["python3", str(SCRIPT), *args],
        check=True,
        text=True,
        capture_output=True,
    )


def write_manifest(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


class ReaderLabPackageBuilderTests(unittest.TestCase):
    def test_builds_shareable_package_with_audit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_builder("--output-dir", tmp)
            payload = json.loads(result.stdout)
            package_root = Path(tmp) / payload["package_root"]

            self.assertEqual(payload["status"], "shareable_package_prepared")
            self.assertTrue((package_root / "SKILL.md").is_file())
            self.assertTrue((package_root / "checks/readiness-checklist.md").is_file())
            self.assertTrue((package_root / "evals/output-cases.json").is_file())
            self.assertTrue((package_root / "examples/run-config-example.json").is_file())
            self.assertTrue((package_root / "scripts/readerlab.py").is_file())
            self.assertTrue((package_root / "scripts/readerlab_trace_validator.py").is_file())
            self.assertTrue((package_root / "tests/package_smoke_test.py").is_file())
            self.assertTrue((package_root / "tests/book_route_smoke_test.py").is_file())
            self.assertTrue((package_root / "tests/longform_route_smoke_test.py").is_file())
            self.assertTrue((package_root / "docs/product-spec.md").is_file())
            self.assertTrue((package_root / "docs/readerlab-v2-runtime-config.md").is_file())
            self.assertTrue((package_root / "docs/readerlab-v2-install-smoke.md").is_file())
            self.assertTrue((package_root / "docs/readerlab-v2-book-route-smoke.md").is_file())
            self.assertTrue((package_root / "docs/readerlab-v2-longform-route-smoke.md").is_file())
            self.assertTrue((package_root / "docs/contracts/trace-validation-v1.md").is_file())
            self.assertTrue((package_root / "fixtures/contract-validator-proof-v0/README.md").is_file())
            self.assertTrue((package_root / "fixtures/book-route-smoke-v0/audit/source-excerpts/chapter-01.md").is_file())
            self.assertTrue((package_root / "fixtures/longform-route-smoke-v0/audit/source-excerpts/report-argument.md").is_file())
            self.assertTrue((package_root / "PACKAGE_BOUNDARY.md").is_file())
            self.assertTrue((package_root / "PACKAGE_AUDIT.json").is_file())

            audit = json.loads((package_root / "PACKAGE_AUDIT.json").read_text(encoding="utf-8"))
            self.assertEqual(audit["status"], "pass")
            self.assertTrue(audit["not_reader_acceptance"])
            self.assertTrue(audit["not_production_ready"])
            self.assertFalse(audit["failures"])
            audit_paths = {file["path"] for file in audit["files"]}
            self.assertIn("PACKAGE_MANIFEST.json", audit_paths)
            self.assertEqual(audit["audit_file"], "PACKAGE_AUDIT.json")

            package_manifest = json.loads((package_root / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
            self.assertEqual(package_manifest["package_root"], "readerlab")
            manifest_text = json.dumps(package_manifest, ensure_ascii=False)
            self.assertNotIn("/Users/", manifest_text)
            self.assertNotIn("/private/", manifest_text)
            self.assertNotIn("/tmp/", manifest_text)
            self.assertNotIn("/workspace/", manifest_text)
            self.assertFalse((package_root / "contracts/trace-validation-v1.md").exists())

            smoke = subprocess.run(
                ["python3", str(package_root / "tests/package_smoke_test.py")],
                check=True,
                text=True,
                capture_output=True,
            )
            self.assertIn("PASS ReaderLab package smoke", smoke.stdout)

    def test_package_excludes_reports_and_private_demo_fixtures(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_builder("--output-dir", tmp)
            package_root = Path(tmp) / "readerlab"
            package_paths = {path.relative_to(package_root).as_posix() for path in package_root.rglob("*") if path.is_file()}

            self.assertFalse(any(path.startswith("docs/reports/") for path in package_paths))
            self.assertFalse(any("private-material-validation" in path for path in package_paths))
            self.assertFalse(any(path.startswith("fixtures/comment-replay/") for path in package_paths))
            self.assertFalse(any("experiments/" in path for path in package_paths))

    def test_package_sanitizes_local_paths_and_external_fixture_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_builder("--output-dir", tmp)
            package_root = Path(tmp) / "readerlab"
            combined = "\n".join(
                path.read_text(encoding="utf-8")
                for path in sorted(package_root.rglob("*"))
                if path.is_file() and path.suffix in {".md", ".json", ".py"}
            )

            self.assertNotIn("/Users/", combined)
            self.assertNotIn("技能项目/skills-canonical/packages/gstack", combined)
            self.assertNotIn(
                "python3 scripts/readerlab_trace_validator.py validate-suite --demo tests/fixtures/readerlab/private-material-validation",
                combined,
            )
            self.assertNotIn("只在本仓库 `.agents/skills/readerlab/` 激活", combined)
            self.assertNotIn("不安装到 `~/.codex/skills/`", combined)
            package_instructions = "\n".join(
                (package_root / path).read_text(encoding="utf-8")
                for path in [
                    "SKILL.md",
                    "checks/readiness-checklist.md",
                    "checks/activation-checklist.md",
                    "docs/readerlab-v2-runtime-config.md",
                    "docs/decisions.md",
                ]
            )
            self.assertNotIn(".agents/skills/readerlab/examples/run-config-example.json", package_instructions)
            self.assertNotIn("python3 tests/test_readerlab_trace_validator.py", package_instructions)
            self.assertNotIn("python3 tests/test_readerlab.py", package_instructions)
            self.assertIn("shareable Skill package 是候选包", package_instructions)
            self.assertIn("shareable_package_prepared", combined)

    def test_refuses_to_overwrite_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_builder("--output-dir", tmp)
            result = subprocess.run(
                ["python3", str(SCRIPT), "--output-dir", tmp],
                check=False,
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("pass --force", result.stderr + result.stdout)

    def test_refuses_to_delete_source_checkout_with_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = Path(tmp) / "dangerous-manifest.json"
            write_manifest(
                manifest_path,
                {
                    "schema": "readerlab.package-manifest.v1",
                    "package_root_name": ROOT.name,
                    "include_files": [],
                    "include_dirs": [],
                },
            )
            result = subprocess.run(
                [
                    "python3",
                    str(SCRIPT),
                    "--manifest",
                    str(manifest_path),
                    "--output-dir",
                    str(ROOT.parent),
                    "--force",
                ],
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("refusing to use source checkout as package output", result.stderr + result.stdout)
            self.assertTrue((ROOT / "scripts/build_readerlab_package.py").is_file())

    def test_refuses_package_root_inside_or_above_source_checkout(self) -> None:
        cases = [
            (ROOT, "docs", "refusing to use source checkout as package output"),
            (ROOT, "..", "refusing package output outside --output-dir"),
        ]
        for output_dir, package_root_name, expected_error in cases:
            with self.subTest(package_root_name=package_root_name), tempfile.TemporaryDirectory() as tmp:
                manifest_path = Path(tmp) / "dangerous-manifest.json"
                write_manifest(
                    manifest_path,
                    {
                        "schema": "readerlab.package-manifest.v1",
                        "package_root_name": package_root_name,
                        "include_files": [],
                        "include_dirs": [],
                    },
                )
                result = subprocess.run(
                    [
                        "python3",
                        str(SCRIPT),
                        "--manifest",
                        str(manifest_path),
                        "--output-dir",
                        str(output_dir),
                        "--force",
                    ],
                    check=False,
                    text=True,
                    capture_output=True,
                )

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected_error, result.stderr + result.stdout)

    def test_refuses_package_root_outside_output_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "out"
            victim = Path(tmp) / "victim"
            victim.mkdir()
            (victim / "keep.txt").write_text("do not delete", encoding="utf-8")
            cases = [
                "../victim",
                str(victim),
            ]
            for package_root_name in cases:
                with self.subTest(package_root_name=package_root_name):
                    manifest_path = Path(tmp) / "dangerous-manifest.json"
                    write_manifest(
                        manifest_path,
                        {
                            "schema": "readerlab.package-manifest.v1",
                            "package_root_name": package_root_name,
                            "include_files": [],
                            "include_dirs": [],
                        },
                    )
                    result = subprocess.run(
                        [
                            "python3",
                            str(SCRIPT),
                            "--manifest",
                            str(manifest_path),
                            "--output-dir",
                            str(output_dir),
                            "--force",
                        ],
                        check=False,
                        text=True,
                        capture_output=True,
                    )

                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("refusing package output outside --output-dir", result.stderr + result.stdout)
                    self.assertTrue((victim / "keep.txt").is_file())

    def test_refuses_output_dir_itself_as_package_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "out"
            output_dir.mkdir()
            (output_dir / "keep.txt").write_text("do not delete", encoding="utf-8")
            cases = [
                ".",
                str(output_dir),
            ]
            for package_root_name in cases:
                with self.subTest(package_root_name=package_root_name):
                    manifest_path = Path(tmp) / "dangerous-manifest.json"
                    write_manifest(
                        manifest_path,
                        {
                            "schema": "readerlab.package-manifest.v1",
                            "package_root_name": package_root_name,
                            "include_files": [],
                            "include_dirs": [],
                        },
                    )
                    result = subprocess.run(
                        [
                            "python3",
                            str(SCRIPT),
                            "--manifest",
                            str(manifest_path),
                            "--output-dir",
                            str(output_dir),
                            "--force",
                        ],
                        check=False,
                        text=True,
                        capture_output=True,
                    )

                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("refusing to use --output-dir itself as package output", result.stderr + result.stdout)
                    self.assertTrue((output_dir / "keep.txt").is_file())

    def test_refuses_manifest_sources_and_targets_outside_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            outside_source = Path(tmp) / "outside.md"
            outside_source.write_text("outside", encoding="utf-8")
            cases = [
                (
                    "source",
                    {
                        "include_files": [
                            {"source": str(outside_source), "target": "outside.md", "sanitize": False},
                        ],
                        "include_dirs": [],
                    },
                    "include source escapes allowed boundary",
                ),
                (
                    "target",
                    {
                        "include_files": [
                            {"source": "README.md", "target": "../escaped.md", "sanitize": False},
                        ],
                        "include_dirs": [],
                    },
                    "package target escapes allowed boundary",
                ),
                (
                    "dir-target",
                    {
                        "include_files": [],
                        "include_dirs": [
                            {"source": "docs/contracts", "target": "../escaped-dir", "sanitize": False},
                        ],
                    },
                    "package target escapes allowed boundary",
                ),
            ]
            for name, payload, expected_error in cases:
                with self.subTest(name=name):
                    manifest_path = Path(tmp) / f"{name}-manifest.json"
                    write_manifest(
                        manifest_path,
                        {
                            "schema": "readerlab.package-manifest.v1",
                            "package_root_name": f"readerlab-{name}",
                            **payload,
                        },
                    )
                    result = subprocess.run(
                        [
                            "python3",
                            str(SCRIPT),
                            "--manifest",
                            str(manifest_path),
                            "--output-dir",
                            tmp,
                        ],
                        check=False,
                        text=True,
                        capture_output=True,
                    )

                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(expected_error, result.stderr + result.stdout)
                    self.assertFalse((Path(tmp) / "escaped.md").exists())
                    self.assertFalse((Path(tmp) / "escaped-dir").exists())

    def test_accepts_relative_manifest_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    "python3",
                    str(SCRIPT),
                    "--manifest",
                    "packaging/readerlab-package-manifest.json",
                    "--output-dir",
                    tmp,
                ],
                check=True,
                text=True,
                capture_output=True,
                cwd=ROOT,
            )
            payload = json.loads(result.stdout)
            package_root = Path(tmp) / payload["package_root"]
            package_manifest = json.loads((package_root / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))

            self.assertEqual(package_manifest["manifest"], "packaging/readerlab-package-manifest.json")
            self.assertEqual(package_manifest["status"], "shareable_package_prepared")

    def test_reports_custom_package_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = Path(tmp) / "custom-manifest.json"
            write_manifest(
                manifest_path,
                {
                    "schema": "readerlab.package-manifest.v1",
                    "package_root_name": "custom-readerlab",
                    "include_files": [],
                    "include_dirs": [],
                },
            )
            result = subprocess.run(
                [
                    "python3",
                    str(SCRIPT),
                    "--manifest",
                    str(manifest_path),
                    "--output-dir",
                    tmp,
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            payload = json.loads(result.stdout)
            package_root = Path(tmp) / payload["package_root"]
            package_manifest = json.loads((package_root / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))

            self.assertEqual(payload["package_root"], "custom-readerlab")
            self.assertTrue((package_root / "PACKAGE_BOUNDARY.md").is_file())
            self.assertEqual(package_manifest["package_root"], "custom-readerlab")


if __name__ == "__main__":
    unittest.main()
