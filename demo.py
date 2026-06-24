"""Demo: personalized B2B sales emails without API keys."""

from __future__ import annotations

SAMPLE_LEADS = [
    {
        "name": "Jordan Lee",
        "company": "Northwind Analytics",
        "role": "VP Operations",
        "industry": "logistics",
        "pain_point": "manual freight reporting",
    },
    {
        "name": "Samira Khan",
        "company": "Harbor Fintech",
        "role": "Head of Product",
        "industry": "fintech",
        "pain_point": "slow onboarding for SMB clients",
    },
]


def generate_email(lead: dict) -> str:
    return (
        f"Subject: Quick idea for {lead['company']}'s {lead['pain_point']}\n\n"
        f"Hi {lead['name']},\n\n"
        f"I noticed {lead['company']} is scaling {lead['role'].lower()} workflows in {lead['industry']}. "
        f"Teams similar to yours cut reporting time by ~40% after automating {lead['pain_point']}.\n\n"
        f"Would a 15-minute walkthrough next week be useful?\n\n"
        f"Best,\nAnahita\n"
        f"---\n(Demo mode — template email, no OpenAI key required)"
    )


def main() -> None:
    print("AI Sales Email Personalization — DEMO MODE\n")
    for i, lead in enumerate(SAMPLE_LEADS, 1):
        print(f"=== Lead {i}: {lead['name']} @ {lead['company']} ===\n")
        print(generate_email(lead))
        print()


if __name__ == "__main__":
    main()
