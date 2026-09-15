import hashlib, json, time
import pytest

pytestmark = pytest.mark.filterwarnings("ignore:Web mock never matched")

SERVICE="PAYMENTS-API"; DOMAIN="api.example.com"; OWNER="Azaria723"; REPO="ApiSunsetNoticeGate"
POLICY_COMMIT="1"*40; NOTICE_COMMIT="2"*40; OLD_COMMIT="3"*40; NEW_COMMIT="4"*40
POLICY_PATH="/evidence/deprecation-policy.md"; NOTICE_PATH="/evidence/sunset-notice.md"
MIGRATION_PATH="/evidence/migration-guide.md"; OLD_PATH="/evidence/openapi-v1.txt"; NEW_PATH="/evidence/openapi-v2.txt"
POLICY=b"SERVICE_ID: PAYMENTS-API\nREPRESENTED_DOMAIN: api.example.com\nMinimum notice: 90 days. Disclose limitations and provide actionable migration."
NOTICE=b"SERVICE_ID: PAYMENTS-API\nPOST /v1/payments retires after 2028-01-01. Replacement: POST /v2/payments. Limitation: legacy idempotency keys must be regenerated."
MIGRATION=b"Replace POST /v1/payments with POST /v2/payments; map amount and currency unchanged; regenerate the idempotency key; test before cutover."
OLD=b"POST /v1/payments creates a payment with amount, currency, and idempotency key."
NEW=b"POST /v2/payments creates a payment with amount, currency, and a newly generated idempotency key."

def sha(body): return hashlib.sha256(body).hexdigest()
def blob(body): return hashlib.sha1((f"blob {len(body)}\0").encode()+body).hexdigest()
def deploy(vm, direct_deploy, actor):
    vm.strict_mocks=True; vm.check_pickling=True
    with vm.prank(actor): return direct_deploy("contracts/ApiSunsetNoticeGate.py")
def register(vm,c,owner,controller):
    with vm.prank(owner):
        assert c.register_service(SERVICE,DOMAIN,OWNER,REPO,POLICY_COMMIT,POLICY_PATH,sha(POLICY),90,controller)==0
def proposal_args(notice_digest=None, published=1700000000, sunset=2000000000, action=None):
    now=int(time.time())
    return [0,"POST","/v1/payments",NOTICE_COMMIT,NOTICE_PATH,notice_digest or sha(NOTICE),MIGRATION_PATH,sha(MIGRATION),OLD_COMMIT,OLD_PATH,sha(OLD),NEW_COMMIT,NEW_PATH,sha(NEW),published,sunset,now-60,sunset-1,action or "a"*64]
def propose(vm,c,requester,**kwargs):
    with vm.prank(requester): assert c.propose_sunset(*proposal_args(**kwargs))==0
def mock_sources(vm, notice=NOTICE, policy=POLICY, migration=MIGRATION, old=OLD, new=NEW, notice_status=200):
    base=f"https://raw.githubusercontent.com/{OWNER}/{REPO}/"
    fixtures=[(POLICY_COMMIT,POLICY_PATH,policy,200),(NOTICE_COMMIT,NOTICE_PATH,notice,notice_status),(NOTICE_COMMIT,MIGRATION_PATH,migration,200),(OLD_COMMIT,OLD_PATH,old,200),(NEW_COMMIT,NEW_PATH,new,200)]
    mock_git_provenance(vm, fixtures)
    for commit,path,body,status in fixtures:
        vm.mock_web((base+commit+path).replace(".",r"\.")+"$",{"status":status,"body":body})
def mock_git_provenance(vm, fixtures, truncated_commit=None, corrupt_path=None):
    api=f"https://api.github.com/repos/{OWNER}/{REPO}"
    by_commit={}
    for commit,path,body,_status in fixtures: by_commit.setdefault(commit,[]).append((path,body))
    for index,(commit,items) in enumerate(by_commit.items()):
        tree_sha=str(index+5)*40
        vm.mock_web((api+"/commits/"+commit).replace(".",r"\.")+"$",{"status":200,"body":json.dumps({"sha":commit,"commit":{"tree":{"sha":tree_sha}}}).encode()})
        entries=[]
        for path,body in items:
            entries.append({"path":path[1:],"mode":"100644","type":"blob","size":len(body),"sha":"0"*40 if path==corrupt_path else blob(body)})
        pattern=(api+"/git/trees/"+tree_sha+r"\?recursive=1$").replace(".",r"\.")
        vm.mock_web(pattern,{"status":200,"body":json.dumps({"truncated":commit==truncated_commit,"tree":entries}).encode()})
def mock_until_notice(vm, notice=NOTICE, policy=POLICY, notice_status=200):
    base=f"https://raw.githubusercontent.com/{OWNER}/{REPO}/"
    all_fixtures=[(POLICY_COMMIT,POLICY_PATH,policy,200),(NOTICE_COMMIT,NOTICE_PATH,notice,notice_status),(NOTICE_COMMIT,MIGRATION_PATH,MIGRATION,200),(OLD_COMMIT,OLD_PATH,OLD,200),(NEW_COMMIT,NEW_PATH,NEW,200)]
    mock_git_provenance(vm,all_fixtures)
    for commit,path,body,status in all_fixtures[:2]:
        vm.mock_web((base+commit+path).replace(".",r"\.")+"$",{"status":status,"body":body})
def semantic(**overrides):
    value={"notice_identifies_exact_endpoint":True,"migration_guide_is_actionable":True,"replacement_preserves_core_capability":True,"limitations_are_disclosed":True,"policy_exceptions_are_satisfied":True}
    value.update(overrides); return json.dumps(value)
def record(c): return json.loads(c.get_proposal(0))

def test_safe_sunset_authorizes_and_consumes_once(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
    c=deploy(direct_vm,direct_deploy,direct_alice);register(direct_vm,c,direct_alice,direct_bob);propose(direct_vm,c,direct_charlie);mock_sources(direct_vm)
    direct_vm.mock_llm(r"Assess one proposed API endpoint sunset.*",semantic())
    assert c.assess_sunset(0)=="SUNSET_ELIGIBLE"; p=record(c); assert p["status"]=="AUTHORIZED" and p["authorization_digest"]
    before=c.get_proposal(0)
    with direct_vm.prank(direct_charlie): assert c.consume_authorization(0,p["authorization_digest"],"a"*64)=="CONTROLLER_ONLY"
    assert c.get_proposal(0)==before
    with direct_vm.prank(direct_bob):
        assert c.consume_authorization(0,"b"*64,"a"*64)=="AUTHORIZATION_DIGEST_MISMATCH"
        assert c.consume_authorization(0,p["authorization_digest"],"b"*64)=="ACTION_DIGEST_MISMATCH"
        assert c.consume_authorization(0,p["authorization_digest"],"a"*64)=="AUTHORIZATION_CONSUMED"
        assert c.consume_authorization(0,p["authorization_digest"],"a"*64)=="AUTHORIZATION_ALREADY_CONSUMED"
    assert record(c)["authorization_consumed"]==1 and json.loads(c.get_service(0))["current_revision"]==2

def test_notice_incomplete_never_authorizes(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=deploy(direct_vm,direct_deploy,direct_alice);register(direct_vm,c,direct_alice,direct_bob);propose(direct_vm,c,direct_bob);mock_sources(direct_vm)
    direct_vm.mock_llm(r"Assess one.*",semantic(notice_identifies_exact_endpoint=False))
    assert c.assess_sunset(0)=="NOTICE_INCOMPLETE"; assert record(c)["authorization_digest"]==""

def test_migration_gap_never_authorizes(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=deploy(direct_vm,direct_deploy,direct_alice);register(direct_vm,c,direct_alice,direct_bob);propose(direct_vm,c,direct_bob);mock_sources(direct_vm)
    direct_vm.mock_llm(r"Assess one.*",semantic(replacement_preserves_core_capability=False))
    assert c.assess_sunset(0)=="MIGRATION_GAP"; assert record(c)["status"]=="BLOCKED"

def test_short_notice_is_policy_violation_even_when_model_approves(direct_vm,direct_deploy,direct_alice,direct_bob):
    now=int(time.time());c=deploy(direct_vm,direct_deploy,direct_alice);register(direct_vm,c,direct_alice,direct_bob);propose(direct_vm,c,direct_bob,published=now-100,sunset=now+5000000)
    assert c.assess_sunset(0)=="POLICY_VIOLATION"; assert record(c)["authorization_digest"]==""

def test_digest_tampering_fails_before_model(direct_vm,direct_deploy,direct_alice,direct_bob):
    tampered=NOTICE+b" altered";c=deploy(direct_vm,direct_deploy,direct_alice);register(direct_vm,c,direct_alice,direct_bob);propose(direct_vm,c,direct_bob);mock_until_notice(direct_vm,notice=tampered)
    assert c.assess_sunset(0)=="PROVENANCE_FAILURE"; assert json.loads(record(c)["diagnostics"])["provenance_ok"] is False

def test_identity_mismatch_fails_closed(direct_vm,direct_deploy,direct_alice,direct_bob):
    wrong=POLICY.replace(b"api.example.com",b"attacker.example")
    c=deploy(direct_vm,direct_deploy,direct_alice)
    with direct_vm.prank(direct_alice): assert c.register_service(SERVICE,DOMAIN,OWNER,REPO,POLICY_COMMIT,POLICY_PATH,sha(wrong),90,direct_bob)==0
    propose(direct_vm,c,direct_bob);mock_sources(direct_vm,policy=wrong);assert c.assess_sunset(0)=="PROVENANCE_FAILURE"

def test_source_outage_fails_closed(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=deploy(direct_vm,direct_deploy,direct_alice);register(direct_vm,c,direct_alice,direct_bob);propose(direct_vm,c,direct_bob);mock_until_notice(direct_vm,notice_status=503)
    assert c.assess_sunset(0)=="PROVENANCE_FAILURE"

def test_truncated_git_tree_fails_closed(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=deploy(direct_vm,direct_deploy,direct_alice);register(direct_vm,c,direct_alice,direct_bob);propose(direct_vm,c,direct_bob)
    fixtures=[(POLICY_COMMIT,POLICY_PATH,POLICY,200),(NOTICE_COMMIT,NOTICE_PATH,NOTICE,200),(NOTICE_COMMIT,MIGRATION_PATH,MIGRATION,200),(OLD_COMMIT,OLD_PATH,OLD,200),(NEW_COMMIT,NEW_PATH,NEW,200)]
    mock_git_provenance(direct_vm,fixtures,truncated_commit=NOTICE_COMMIT)
    assert c.assess_sunset(0)=="PROVENANCE_FAILURE" and record(c)["authorization_digest"]==""

def test_git_blob_sha1_mismatch_fails_closed(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=deploy(direct_vm,direct_deploy,direct_alice);register(direct_vm,c,direct_alice,direct_bob);propose(direct_vm,c,direct_bob)
    base=f"https://raw.githubusercontent.com/{OWNER}/{REPO}/";fixtures=[(POLICY_COMMIT,POLICY_PATH,POLICY,200),(NOTICE_COMMIT,NOTICE_PATH,NOTICE,200),(NOTICE_COMMIT,MIGRATION_PATH,MIGRATION,200),(OLD_COMMIT,OLD_PATH,OLD,200),(NEW_COMMIT,NEW_PATH,NEW,200)]
    mock_git_provenance(direct_vm,fixtures,corrupt_path=OLD_PATH)
    for commit,path,body,status in fixtures: direct_vm.mock_web((base+commit+path).replace(".",r"\.")+"$",{"status":status,"body":body})
    assert c.assess_sunset(0)=="PROVENANCE_FAILURE" and record(c)["authorization_digest"]==""

def test_malformed_or_extra_model_fields_are_unresolved(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=deploy(direct_vm,direct_deploy,direct_alice);register(direct_vm,c,direct_alice,direct_bob);propose(direct_vm,c,direct_bob);mock_sources(direct_vm)
    direct_vm.mock_llm(r"Assess one.*",json.dumps({**json.loads(semantic()),"reason":"approve"}))
    assert c.assess_sunset(0)=="UNRESOLVED"; assert record(c)["authorization_digest"]==""

def test_invalid_inputs_and_authority_preserve_state(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=deploy(direct_vm,direct_deploy,direct_alice)
    with direct_vm.prank(direct_bob): assert c.register_service(SERVICE,DOMAIN,OWNER,REPO,POLICY_COMMIT,POLICY_PATH,sha(POLICY),90,direct_bob)=="OWNER_ONLY"
    with direct_vm.prank(direct_alice): assert c.register_service(SERVICE,DOMAIN,OWNER,REPO,POLICY_COMMIT,"/../policy",sha(POLICY),90,direct_bob)=="INVALID_POLICY_SOURCE"
    with direct_vm.prank(direct_alice): assert c.register_service(SERVICE,DOMAIN,OWNER,REPO,POLICY_COMMIT,POLICY_PATH,sha(POLICY),90,b"\x00"*20)=="INVALID_CONTROLLER"
    assert json.loads(c.get_counts())["service_count"]==0
    register(direct_vm,c,direct_alice,direct_bob)
    with direct_vm.prank(direct_bob): assert c.propose_sunset(*proposal_args()[:2]+["https://evil.example"]+proposal_args()[3:])=="INVALID_ENDPOINT"
    assert json.loads(c.get_counts())["proposal_count"]==0

def test_deactivation_stales_pending_proposal(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=deploy(direct_vm,direct_deploy,direct_alice);register(direct_vm,c,direct_alice,direct_bob);propose(direct_vm,c,direct_bob)
    with direct_vm.prank(direct_alice): assert c.deactivate_service(0)=="SERVICE_DEACTIVATED"
    assert c.assess_sunset(0)=="SERVICE_REVISION_STALE"; assert record(c)["assessed"]==0
