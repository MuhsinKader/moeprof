from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUARD = ROOT / "adapters" / "codex" / "hooks" / "policy_guard.py"

spec = importlib.util.spec_from_file_location("moeprof_policy_guard", GUARD)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def blocked(command: str) -> bool:
    return module.match_rule(command) is not None


def test_blocks_catastrophic_root_deletion():
    assert blocked("rm -rf /")


def test_blocks_force_push_to_main():
    assert blocked("git push origin main --force")


def test_blocks_whole_database_drop():
    assert blocked("DROP DATABASE production;")


def test_blocks_infrastructure_destroy():
    assert blocked("terraform destroy")


def test_blocks_known_credential_store_read():
    assert blocked("cat ~/.aws/credentials")


def test_allows_normal_recursive_cleanup():
    assert not blocked("rm -rf ./build")


def test_allows_normal_git_push():
    assert not blocked("git push origin feature/moeprof")


def test_allows_database_migration_command():
    assert not blocked("python manage.py migrate")


def test_allows_terraform_plan():
    assert not blocked("terraform plan")


def test_allows_normal_config_read():
    assert not blocked("cat pyproject.toml")
