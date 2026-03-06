# Jules AI v92.0 Test Runner
Write-Host "Executing Project OMEGA Test Suite..." -ForegroundColor Yellow
$env:PYTHONPATH = "."
pytest tests/test_v71_alpha.py tests/test_v71_beta_sanity.py tests/verify_sih_enforcement.py tests/test_transition_rollback.py
Write-Host "Testing Complete." -ForegroundColor Green
