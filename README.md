# Password Strength Checker

[English](README.md) | [日本語](README.ja.md)

## Overview

Password Strength Checker is a Python-based command-line application that evaluates passwords using a custom rule-based scoring system.

It analyzes password length, character diversity, consecutive character repetition, and repeated patterns to calculate a score between 0 and 100.

This project is intended for educational purposes and does not guarantee actual password security.

## Motivation

This project was developed to improve my understanding of:

- Python programming
- Password security
- Algorithm design
- Modular software architecture
- Input validation and error handling
- Unit and integration testing

## Features

- Password strength scoring from 0 to 100
- Printable ASCII character validation
- Unique character count evaluation
- Unique character ratio evaluation
- Password length evaluation
- Consecutive character repetition detection
- Repeated substring detection
- Length-based score restrictions
- Interactive command-line interface
- Unit and integration tests

## Requirements

- Python 3.14.10 (tested version)
- No third-party Python libraries are required.

Compatibility with other Python versions has not yet been verified.

## Installation

Clone the repository:

```bash
git clone https://github.com/fin-hoppy/password-checker.git
cd password-checker/v1.0
```

## Usage

Run the following command:

```bash
python3 password_checker.py
```

Example:

```text
Enter a password: aB3!
Password is valid.
Password strength score: 5

1.Enter another password
2.Exit

Select an option: 2
Exiting the program.
```

Use sample passwords only. Do not enter real passwords.

## Project Structure

```text
password-checker/
├── .gitignore
├── README.md
├── README.ja.md
└── v1.0/
    ├── password_checker.py
    ├── cli.py
    ├── validation.py
    ├── scoring.py
    └── test_password_checker.py
```

## Architecture

The application separates user interaction, input validation, and scoring logic to improve maintainability and testability.

| Module | Responsibility |
|---|---|
| password_checker.py | Application entry point and module imports |
| cli.py | User input, output, and menu control |
| validation.py | Input validation and structured error handling |
| scoring.py | Password scoring and pattern detection |
| test_password_checker.py | Unit and integration testing |

## Scoring Algorithm

The scoring system uses the following criteria:

| Criterion | Maximum Score |
|---|---:|
| Unique character count | 45 |
| Unique character ratio | 20 |
| Password length | 20 |
| Repeated pattern evaluation | 15 |
| Total | 100 |

Consecutive character repetition may result in a penalty of up to 30 points.

### Length-Based Restrictions

| Password Length | Maximum Final Score |
|---|---:|
| 1–4 characters | 5 |
| 5–7 characters | 30 |
| 8–14 characters | 60 |
| 15 or more characters | 100 |

For passwords of four characters or fewer, only the length score and consecutive repetition penalty are applied.

### Repeated Patterns

The application searches for repeated substrings that:

- Contain at least two characters.
- Contain at least two distinct characters.
- Appear more than once at non-overlapping positions.
- Are evaluated in a case-sensitive manner.

When multiple repeated patterns are detected, the lowest pattern score is selected.

## Input Validation

The application rejects:

- Empty passwords
- Passwords consisting entirely of spaces
- Non-ASCII characters
- Characters outside the printable ASCII range (32–126)

Multiple validation errors can be returned together.

## Testing

The application uses Python's built-in unittest framework.

Run the tests from the v1.0 directory:

```bash
python3 -m unittest -v test_password_checker.py
```

Latest local test result:

```text
Ran 22 tests

OK
```

The tests cover:

- Input validation and boundary conditions
- Individual scoring functions
- Consecutive repetition penalties
- Repeated pattern detection
- Final score calculation
- CLI interaction and error handling

## Limitations

- The scoring system is heuristic and does not guarantee password security.
- The application does not estimate password cracking time.
- Common passwords and previously compromised passwords are not detected.
- Predictable sequences may receive high scores.
- Unicode passwords are not supported.
- Password input is visible in the terminal.
- Repeated pattern detection may become computationally expensive for long inputs.
- No explicit maximum password length is currently enforced.

## Proposed Roadmap

- [ ] Improve the scoring algorithm
- [ ] Detect predictable character sequences
- [ ] Evaluate common and compromised passwords
- [ ] Implement hidden password input
- [ ] Improve pattern detection performance
- [ ] Expand test coverage
- [ ] Introduce continuous integration with GitHub Actions

## Disclaimer

This application is intended for educational purposes.

A high score does not guarantee that a password is resistant to real-world attacks. Do not use actual passwords when testing this application.

## License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.