from dataset import tickets


ESCALATION_THRESHOLD = 0.60


def lookup_ticket(record_id):
    for ticket in tickets:
        if ticket["record_id"] == record_id:
            recency_score = 1 - (
                ticket["days_since_created"] / 30
            )

            escalation_score = (
                0.7 * int(ticket["escalated"])
                + 0.3 * recency_score
            )

            return {
                "record_id": ticket["record_id"],
                "status": ticket["status"],
                "resolution_time_hours": ticket["resolution_time_hours"],
                "escalation_score": round(escalation_score, 3),
                "escalated": ticket["escalated"],
                "days_since_created": ticket["days_since_created"],
                "escalation_required": (
                    escalation_score >= ESCALATION_THRESHOLD
                ),
            }

    return {
        "error": f"Ticket {record_id} was not found."
    }


if __name__ == "__main__":
    print(lookup_ticket(1))
    print(lookup_ticket(2))
    print(lookup_ticket(999))
