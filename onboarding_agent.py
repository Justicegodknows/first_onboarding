#!/usr/bin/env python3
"""
Onboarding Agent — guides new users through the onboarding process interactively.
"""

import json
import os
import sys
from datetime import datetime, timezone


RESOURCES = {
    "engineering": [
        "Set up your development environment: https://github.com/Justicegodknows/first_onboarding#setup",
        "Review the coding standards document",
        "Join the #engineering Slack channel",
        "Schedule a 1-on-1 with your tech lead",
    ],
    "design": [
        "Access the design system / Figma workspace",
        "Review brand guidelines",
        "Join the #design Slack channel",
        "Schedule a 1-on-1 with the design lead",
    ],
    "product": [
        "Read the product roadmap",
        "Join the #product Slack channel",
        "Schedule a 1-on-1 with your product manager",
        "Review user research docs",
    ],
    "marketing": [
        "Review brand voice & tone guide",
        "Join the #marketing Slack channel",
        "Access marketing calendar and campaign tracker",
        "Schedule a 1-on-1 with the marketing lead",
    ],
    "other": [
        "Review the employee handbook",
        "Join your team's Slack channel",
        "Schedule a 1-on-1 with your manager",
        "Complete HR paperwork if not already done",
    ],
}

COMMON_CHECKLIST = [
    "Set up company email and calendar",
    "Complete security / compliance training",
    "Review the Code of Conduct",
    "Add yourself to the team directory",
    "Attend the company all-hands meeting",
]


def prompt(question: str, default: str = "") -> str:
    """Display a question and return the user's answer."""
    if default:
        answer = input(f"{question} [{default}]: ").strip()
        return answer if answer else default
    answer = input(f"{question}: ").strip()
    return answer


def choose(question: str, options: list[str]) -> str:
    """Present a numbered menu and return the selected option."""
    print(f"\n{question}")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option.capitalize()}")
    while True:
        raw = input("Enter number: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        print(f"  Please enter a number between 1 and {len(options)}.")


def print_section(title: str) -> None:
    width = 60
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def run_onboarding() -> dict:
    """Run the interactive onboarding flow and return the collected profile."""
    print_section("👋  Welcome to the Onboarding Agent!")
    print(
        "\nThis agent will help you get set up quickly by collecting a few details\n"
        "and providing a personalised checklist of next steps.\n"
    )

    # --- Collect basic info ---
    name = prompt("What is your full name?")
    while not name:
        print("  Name cannot be empty.")
        name = prompt("What is your full name?")

    start_date = prompt("What is your start date? (YYYY-MM-DD)", datetime.today().strftime("%Y-%m-%d"))
    while True:
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            break
        except ValueError:
            print("  Invalid date. Please use the format YYYY-MM-DD (e.g. 2026-04-01).")
            start_date = prompt("What is your start date? (YYYY-MM-DD)")

    department_options = list(RESOURCES.keys())
    department = choose("Which department are you joining?", department_options)

    role = prompt("What is your job title / role?")

    manager = prompt("Who is your manager? (name or email, optional)")

    # --- Display personalised checklist ---
    print_section(f"✅  Your Onboarding Checklist — {name}")

    print("\n🔹 Common tasks for all new joiners:")
    for item in COMMON_CHECKLIST:
        print(f"   [ ] {item}")

    dept_resources = RESOURCES.get(department, RESOURCES["other"])
    print(f"\n🔹 Tasks specific to {department.capitalize()}:")
    for item in dept_resources:
        print(f"   [ ] {item}")

    # --- Build profile dict ---
    profile = {
        "name": name,
        "role": role,
        "department": department,
        "manager": manager,
        "start_date": start_date,
        "onboarded_at": datetime.now(timezone.utc).isoformat(),
        "checklist": {
            "common": COMMON_CHECKLIST,
            "department_specific": dept_resources,
        },
    }

    # --- Optionally save profile ---
    print_section("💾  Save Your Profile")
    save = prompt("Save your onboarding profile to a JSON file? (yes/no)", "yes").lower()
    if save in ("yes", "y"):
        filename = f"onboarding_{name.lower().replace(' ', '_')}.json"
        with open(filename, "w", encoding="utf-8") as fh:
            json.dump(profile, fh, indent=2)
        print(f"\n  Profile saved to: {filename}")

    print_section("🎉  You're all set!")
    print(
        f"\n  Welcome aboard, {name}! Your manager{' (' + manager + ')' if manager else ''} will be in touch.\n"
        "  Work through the checklist above and don't hesitate to ask for help.\n"
    )

    return profile


def main() -> None:
    try:
        run_onboarding()
    except KeyboardInterrupt:
        print("\n\n  Onboarding cancelled. Run again whenever you're ready. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
