"""Acceptance tests for the Caesar exercise.

Each test runs your program as a whole, exactly as a user would: it gives
it a key on the command line, types a message, then checks what your
program prints and tries to explain what is wrong.

Run the tests from the exercise folder with:

    python test_caesar.py
"""

import os
import subprocess
import sys
from pathlib import Path

EXERCISE_DIR = Path(__file__).resolve().parent
SCRIPT = "caesar.py"
USAGE = "Usage: python caesar.py key"
PLAIN_PROMPT = "plaintext : "
CIPHER_PROMPT = "ciphertext: "
TIMEOUT = 5  # seconds

# Encryption: (what is checked, key, plaintext typed by the user).
CASES = [
    ("key 13 (example of the instructions)", "13", "Hi there!"),
    ("key 1 on uppercase letters", "1", "AA"),
    ("key 1, the case is kept", "1", "Ab"),
    ("key 2, punctuation and spaces are kept", "2", "Ab, cD"),
    ("key 1 on z and Z (back to a and A)", "1", "Zz"),
    ("key 3, digits and symbols are kept", "3", "DNA: ATG-GCC x 42"),
    ("key 5", "5", "ExPiaLiDoCiouS"),
    ("key 17", "17", "SuperCaliFragiLisTic"),
    ("key 26 (a full turn: nothing changes)", "26", "Hello"),
    ("key 27 (same as key 1)", "27", "Hello, World!"),
    ("key 100 (same as key 22)", "100", "Bioinformatics"),
]

# Invalid command lines: (what is checked, arguments).
# The program must print the usage message and stop.
USAGE_CASES = [
    ("no key at all", []),
    ("a word as key", ["HELLO"]),
    ("three arguments", ["1", "2", "3"]),
    ("two numbers", ["1", "2"]),
    ("a negative key", ["-3"]),
    ("a decimal key", ["2.5"]),
    ("a key mixing digits and letters", ["3abc"]),
]

# Bonus, decryption: (what is checked, key, ciphertext typed by the user).
BONUS_CASES = [
    ("key 13 -r (example of the instructions)", "13", "Uv gurer!"),
    ("key 19 -r", "19", "Ab maxkx!"),
    ("key 1 -r on a and A (back to z and Z)", "1", "Aa"),
]

# Bonus, invalid command lines.
BONUS_USAGE_CASES = [
    ("another flag than -r", ["13", "-x"]),
    ("-r without key", ["-r"]),
    ("-r before the key", ["-r", "13"]),
]

# Text typed when the program is NOT supposed to ask anything:
# it lets us see if the program asks something anyway.
UNEXPECTED_INPUT = "Hello"


# ---------------------------------------------------------------------------
# Expected answer
# ---------------------------------------------------------------------------

def shift_text(text, key):
    """Shift every letter of text by key places (key may be negative)."""
    result = ""
    for char in text:
        if "a" <= char <= "z":
            result += chr((ord(char) - ord("a") + key) % 26 + ord("a"))
        elif "A" <= char <= "Z":
            result += chr((ord(char) - ord("A") + key) % 26 + ord("A"))
        else:
            result += char
    return result


# ---------------------------------------------------------------------------
# Running the student's program
# ---------------------------------------------------------------------------

def run_program(arguments, typed_text):
    """Run the program with the arguments, typing typed_text.

    Return (stdout, stderr, return code), or None if the program
    did not stop in time.
    """
    try:
        # sys.executable is the Python running the tests,
        # so "python" vs "python3" does not matter.
        result = subprocess.run(
            [sys.executable, SCRIPT] + arguments,
            input=typed_text + "\n",
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=EXERCISE_DIR,
            env=dict(os.environ, PYTHONIOENCODING="utf-8"),
            timeout=TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return None
    stdout = result.stdout.replace("\r\n", "\n")
    stderr = result.stderr.replace("\r\n", "\n").strip()
    return stdout, stderr, result.returncode


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def show(lines):
    """Indent lines and make spaces visible (shown as '·')."""
    if not lines:
        return "    (nothing)"
    return "\n".join("    " + line.replace(" ", "·") for line in lines)


def last_lines(text, nb_lines=4):
    """Return the last lines of a text, indented."""
    lines = text.split("\n")[-nb_lines:]
    return "\n".join("    " + line for line in lines)


def command(arguments):
    """Return the command line typed by the user, e.g. 'python caesar.py 3'."""
    return " ".join(["python", SCRIPT] + arguments)


def explain_crash(stderr):
    """Explain the most common errors that make the program crash."""
    message = f"Your program crashed:\n{last_lines(stderr)}"
    if "ValueError" in stderr and "int()" in stderr:
        message += ("\nint() fails when the text is not a whole number: check "
                    "the key first (e.g. with str.isdigit()) before "
                    "converting it.")
    elif "IndexError" in stderr and "argv" in stderr:
        message += ("\nsys.argv does not have as many elements as you think: "
                    "check len(sys.argv) before using sys.argv[1].")
    elif "IndexError" in stderr:
        message += ("\nAn index is too large: when a letter goes past 'z', it "
                    "must come back to 'a' (use % 26).")
    elif "TypeError" in stderr and "str" in stderr:
        message += ("\nThe key in sys.argv is a str: convert it with int() "
                    "before doing arithmetic with it.")
    return message


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_usage(arguments):
    """Check that an invalid command line prints the usage message only.

    Return None if the test passes, else an error message.
    """
    result = run_program(arguments, UNEXPECTED_INPUT)
    if result is None:
        return "Your program did not stop (infinite loop?)."
    stdout, stderr, return_code = result
    if stdout == USAGE + "\n" and stderr == "":
        return None
    # sys.exit("Usage: ...") writes the message on stderr: it is accepted too.
    if stdout == "" and stderr == USAGE:
        return None

    lines = stdout.splitlines()
    printed = "Your program printed:\n" + show(lines)
    if "Traceback" in stderr and USAGE in stdout:
        return (f"Your program printed the usage message, but then it went "
                f"on and crashed. It should stop right after the usage "
                f"message (e.g. with sys.exit()).\n{printed}\n"
                f"{explain_crash(stderr)}")
    if "Traceback" in stderr:
        return explain_crash(stderr)
    if PLAIN_PROMPT.strip() in stdout or CIPHER_PROMPT.strip() in stdout:
        if USAGE in stdout:
            return (f"Your program printed the usage message, but then it "
                    f"went on and asked for a text. It should stop right "
                    f"after the usage message (e.g. with sys.exit()).\n"
                    f"{printed}")
        return (f"The command line '{command(arguments)}' is invalid: your "
                f"program should print {USAGE!r} instead of asking for a "
                f"text.\n{printed}")
    if any(line.strip() == USAGE for line in lines):
        return (f"Your program should print only {USAGE!r}, nothing else "
                f"(not even spaces).\n{printed}")
    if any(line.strip().lower() == USAGE.lower() for line in lines):
        return (f"Check the case and the spelling: the message must be "
                f"exactly {USAGE!r}.\n{printed}")
    if any(line.startswith("Usage") for line in lines):
        return (f"The usage message must be exactly {USAGE!r}.\n{printed}")
    return f"Your program should print {USAGE!r}.\n{printed}"


def check_prompt(stdout, prompt):
    """Check that the output starts with the question.

    Return (error message or None, rest of the output after the question).
    """
    printed = "Your program printed:\n" + show(stdout.splitlines())
    if stdout.startswith((prompt + "\n", prompt.rstrip() + "\n")):
        return (f"The text must be typed on the same line as the question: "
                f"use input({prompt!r}) instead of print().\n{printed}"), ""
    if stdout.startswith(prompt):
        return None, stdout[len(prompt):]
    if stdout.startswith(USAGE):
        return (f"Your program printed the usage message, but the command "
                f"line is valid.\n{printed}"), ""
    compact = prompt.replace(" ", "")
    if stdout.replace(" ", "").startswith(compact):
        return (f"The question must be exactly {prompt!r} (spaces shown as "
                f"'·': {prompt.replace(' ', '·')!r}).\n{printed}"), ""
    return f"Your program should start by asking {prompt!r}.\n{printed}", ""


def explain_wrong_text(given, typed, expected, key):
    """Explain why the encrypted (or decrypted) text is wrong."""
    message = ""
    if given == typed:
        message = ("Your program printed the text unchanged: no letter was "
                   "shifted.")
    elif given == shift_text(typed, -key) and given != expected:
        message = "Your program shifted the letters in the wrong direction."
    elif given.lower() == expected.lower():
        message = ("The letters are right but not their case: an uppercase "
                   "letter must stay uppercase, a lowercase one lowercase.")
    elif len(given) != len(typed):
        message = (f"The text has {len(given)} characters instead of "
                   f"{len(typed)}: every character of the message must give "
                   f"exactly one character.")
    else:
        for wrong_key in range(26):
            if shift_text(typed, wrong_key) == given:
                message = (f"Your text looks shifted by {wrong_key} "
                           f"instead of {key % 26}.")
                break

    # First character that is wrong.
    for position, (char, good, bad) in enumerate(zip(typed, expected, given)):
        if good != bad:
            message += (f"\nCharacter {position} ({char!r}) should become "
                        f"{good!r}, but your program printed {bad!r}.")
            if not char.isalpha():
                message += (" Only letters are shifted: copy the other "
                            "characters unchanged.")
            elif not bad.isalpha():
                message += (" When a letter goes past 'z', it must come back "
                            "to 'a' (use % 26).")
            break
    return message.strip()


def check_text(arguments, typed, expected, first_prompt, second_prompt):
    """Run one encryption or decryption test.

    Return None if it passes, else an error message.
    """
    result = run_program(arguments, typed)
    if result is None:
        return "Your program did not stop (infinite loop?)."
    stdout, stderr, return_code = result
    if stdout == f"{first_prompt}{second_prompt}{expected}\n":
        return None

    message, rest = check_prompt(stdout, first_prompt)
    if message is not None:
        if "Traceback" in stderr:
            message += "\n" + explain_crash(stderr)
        return message
    if "EOFError" in stderr:
        return ("Your program asked for a text more than once: it should "
                "call input() only once.")
    if "Traceback" in stderr:
        return explain_crash(stderr)

    lines = rest.splitlines()
    printed = "Your program printed after the question:\n" + show(lines)
    if not lines:
        return (f"Your program printed nothing after reading the text: it "
                f"should print {second_prompt + expected!r}.")
    if len(lines) > 1:
        message = "Your program should print a single line after the question."
        if second_prompt + expected in lines:
            message += (" The right line is there: remove the other print() "
                        "(for instance prints used to debug).")
        return f"{message}\n{printed}"
    line = lines[0]
    if not line.startswith(second_prompt):
        return (f"The answer must start with {second_prompt!r} (spaces shown "
                f"as '·': {second_prompt.replace(' ', '·')!r}).\n{printed}")
    given = line[len(second_prompt):]
    if given.strip() == expected:
        return (f"Nothing should be printed before or after the text (not "
                f"even spaces).\n{printed}")
    key = int(arguments[0])
    return (f"Your program printed {given!r} instead of {expected!r}.\n"
            + explain_wrong_text(given, typed, expected, key))


# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------

def run_test(arguments, typed):
    """Run one test. Return None if it passes, else an error message.

    typed is None for an invalid command line (the usage message is expected).
    """
    if typed is None:
        return check_usage(arguments)
    key = int(arguments[0])
    if "-r" in arguments:
        expected = shift_text(typed, -key)
        return check_text(arguments, typed, expected,
                          CIPHER_PROMPT, PLAIN_PROMPT)
    expected = shift_text(typed, key)
    return check_text(arguments, typed, expected, PLAIN_PROMPT, CIPHER_PROMPT)


def run_tests(title, tests, colors):
    """Run a list of tests (description, arguments, typed text).

    Print the results and return the number of tests that pass.
    """
    green, red, reset = colors
    print(title)
    nb_ok = 0
    for description, arguments, typed in tests:
        message = run_test(arguments, typed)
        if message is None:
            nb_ok += 1
            print(f"{green}✔{reset} {description}")
        else:
            print(f"{red}✗{reset} {description}")
            print(f"    Command: {command(arguments)}")
            if typed is not None:
                print(f"    Text typed: {typed!r}")
            print("    " + message.replace("\n", "\n    ") + "\n")
    color = green if nb_ok == len(tests) else red
    print(f"Validated: {color}{nb_ok}/{len(tests)}{reset}\n")
    return nb_ok


def main():
    sys.stdout.reconfigure(errors="replace")
    use_colors = sys.stdout.isatty() and (
        os.name != "nt" or "WT_SESSION" in os.environ)
    green = "\033[32m" if use_colors else ""
    red = "\033[31m" if use_colors else ""
    reset = "\033[0m" if use_colors else ""
    colors = (green, red, reset)

    if not (EXERCISE_DIR / SCRIPT).is_file():
        print(f"No {SCRIPT} found in {EXERCISE_DIR}")
        return 1

    tests = [(description, [key], text) for description, key, text in CASES]
    tests += [(description, arguments, None)
              for description, arguments in USAGE_CASES]
    nb_ok = run_tests("Caesar", tests, colors)

    bonus = [(description, [key, "-r"], text)
             for description, key, text in BONUS_CASES]
    bonus += [(description, arguments, None)
              for description, arguments in BONUS_USAGE_CASES]
    run_tests("Bonus: -r (optional, ignore it if you did not do the bonus)",
              bonus, colors)

    return 0 if nb_ok == len(tests) else 1


if __name__ == "__main__":
    sys.exit(main())
