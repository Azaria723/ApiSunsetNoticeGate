from pathlib import Path
S=Path("contracts/ApiSunsetNoticeGate.py").read_text(encoding="utf-8")
def test_runtime_is_pinned():
    lines=S.splitlines();assert lines[0]=="# v0.2.16";assert "py-genlayer:" in lines[1]
def test_requester_cannot_supply_evidence_host_or_url():
    sig=S.split("def propose_sunset",1)[1].split(") ->",1)[0].lower();assert "url" not in sig and "host" not in sig and "repo" not in sig
def test_contract_builds_canonical_raw_urls_and_hashes_bytes():
    assert '"https://raw.githubusercontent.com/" + service["repo_owner"]' in S;assert "hashlib.sha256(response.body)" in S
    for term in ["api.github.com/repos/","/commits/","/git/trees/","truncated","_git_blob_sha1","100644"]: assert term in S
def test_model_surface_is_boolean_only_and_contract_derives_verdict():
    assert "exactly these five boolean keys" in S;assert 'type(data[k]) is not bool' in S;assert 'verdict = "SUNSET_ELIGIBLE"' in S
def test_authorization_is_bound_and_single_use():
    for term in ["authorization_digest","action_digest","service_revision","expires_at","AUTHORIZATION_ALREADY_CONSUMED"]:assert term in S
def test_addresses_are_canonical_hex_not_runtime_stringification():
    assert 'format(numeric, "040x")' in S;assert 'return value.as_hex' in S
def test_no_custody_or_arbitrary_execution():
    assert "emit_transfer" not in S and "payable" not in S and "exec(" not in S
