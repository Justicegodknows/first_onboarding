# first_onboarding

An interactive command-line **onboarding agent** that guides new team members through the onboarding process.

## Features

- Collects the new joiner's name, role, department, start date, and manager
- Generates a personalised checklist of common and department-specific tasks
- Optionally saves the onboarding profile to a JSON file for record-keeping
- Supports departments: Engineering, Design, Product, Marketing, and Other

## Requirements

- Python 3.10+

No third-party dependencies are required.

## Usage

```bash
python onboarding_agent.py
```

Follow the on-screen prompts. A sample session:

```
============================================================
  👋  Welcome to the Onboarding Agent!
============================================================

What is your full name?: Alice Smith
What is your start date? (YYYY-MM-DD) [2026-03-16]:
Which department are you joining?
  1. Engineering
  2. Design
  3. Product
  4. Marketing
  5. Other
Enter number: 1
What is your job title / role?: Software Engineer
Who is your manager? (name or email, optional): Bob

============================================================
  ✅  Your Onboarding Checklist — Alice Smith
============================================================

🔹 Common tasks for all new joiners:
   [ ] Set up company email and calendar
   [ ] Complete security / compliance training
   ...

🔹 Tasks specific to Engineering:
   [ ] Set up your development environment
   ...
```

## Running Tests

```bash
python -m unittest discover -s tests -v
```
