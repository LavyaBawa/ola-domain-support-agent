import random

SEED = 42

random.seed(SEED)
CATEGORIES = [
    "Billing",
    "Technical Issue",
    "Account Access",
    "Product Defect",
    "General Inquiry",
]

CATEGORY_WEIGHTS = [0.25, 0.25, 0.20, 0.15, 0.15]

STATUSES = [
    "Open",
    "In Progress",
    "Escalated",
    "Resolved",
    "Closed",
]

STATUS_WEIGHTS = [0.20, 0.25, 0.15, 0.25, 0.15]

NUM_TICKETS = 60
tickets = []

for i in range(NUM_TICKETS):
    category = random.choices(CATEGORIES, weights=CATEGORY_WEIGHTS, k=1)[0]
    status = random.choices(STATUSES, weights=STATUS_WEIGHTS, k=1)[0]
    days_since_created = random.randint(0, 30)   
    resolution_time_hours = random.randint(1, 48)
    escalated = random.random() < 0.20
    ticket = {
        "record_id": i + 1,
        "category": category,
        "status": status,
        "days_since_created": days_since_created,
        "resolution_time_hours": resolution_time_hours,
        "escalated": escalated
    }

    tickets.append(ticket)
   
assert len(tickets) == NUM_TICKETS
print(f"Total tickets: {len(tickets)}")

escalated_count = sum(ticket["escalated"] for ticket in tickets)
escalated_percentage = (escalated_count / len(tickets)) * 100

print(f"Escalated tickets: {escalated_count}")
print(f"Escalation percentage: {escalated_percentage:.2f}%")

required_categories = {
    "Billing",
    "Technical Issue",
    "Account Access",
    "Product Defect",
    "General Inquiry",
}

required_statuses = {
    "Open",
    "In Progress",
    "Escalated",
    "Resolved",
    "Closed",
}

actual_categories = {ticket["category"] for ticket in tickets}
actual_statuses = {ticket["status"] for ticket in tickets}

for category in required_categories:
    count = sum(ticket["category"] == category for ticket in tickets)
    assert count >= 3
assert required_statuses.issubset(actual_statuses)

for ticket in tickets:
    assert isinstance(ticket["record_id"], int)
    assert isinstance(ticket["category"], str)
    assert isinstance(ticket["status"], str)
    assert isinstance(ticket["resolution_time_hours"], int)
    assert isinstance(ticket["days_since_created"], int)
    assert isinstance(ticket["escalated"], bool)

    assert 0 <= ticket["days_since_created"] <= 30
    assert 1 <= ticket["resolution_time_hours"] <= 48

assert 10 <= escalated_percentage <= 30

print("All dataset validation checks passed.")
