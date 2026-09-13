from src.governance.budget import validate_request_budget


normal_request = "What is the SLA for a critical ticket?"

large_request = "x" * 5000

print("NORMAL REQUEST:")
print(validate_request_budget(normal_request))

print("\nOVERSIZED REQUEST:")
print(validate_request_budget(large_request))

assert validate_request_budget(normal_request)["allowed"] is True
assert validate_request_budget(large_request)["allowed"] is False

print("\nBudget guardrail test passed.")
