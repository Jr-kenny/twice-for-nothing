"""Write the entry text for Unsent: The Micro-Confession Sprint.

The program writes a two-part micro-confession to /output/entry.txt:
a To: line, one newline, then the unsent message on one line, with
no trailing newline.
"""

import os

TEXT = (
    "To: the nurse on the second night\n"
    "I pressed the buzzer twice when I needed nothing. The ward had "
    "gone quiet and I was scared to fall asleep alone."
)


def validate(text):
    if not 1 <= len(text) <= 260:
        raise ValueError("entry text must be 1 to 260 characters")
    if not text.strip():
        raise ValueError("entry text must not be only white space")
    if "\r" in text:
        raise ValueError("entry text must not contain a carriage return")
    parts = text.split("\n")
    if len(parts) != 2:
        raise ValueError("entry text must have exactly two parts")
    to_line, message = parts
    if not to_line.startswith("To: ") or not to_line[4:].strip():
        raise ValueError("first part must be a To: line")
    if not message.strip() or message.strip() != message:
        raise ValueError("message must be one line with no stray whitespace")
    if len(message) > 200:
        raise ValueError("message must be at most 200 characters")
    if "  " in text:
        raise ValueError("entry text must not have double spaces")
    if chr(0x2014) in text:
        raise ValueError("entry text must not contain an em dash")
    # The gate counts characters in UTF-8 text, so confirm the text
    # encodes cleanly and round-trips before anything is written.
    if text.encode("utf-8").decode("utf-8") != text:
        raise ValueError("entry text must round-trip as UTF-8")


def main():
    validate(TEXT)

    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(TEXT)

    # Read the file back as bytes and confirm it holds exactly the
    # text: same UTF-8 bytes, no trailing newline, nothing added.
    with open("/output/entry.txt", "rb") as f:
        written = f.read()
    if written != TEXT.encode("utf-8"):
        raise ValueError("written entry does not match the text")
    if written.endswith(b"\n") or written.endswith(b"\r"):
        raise ValueError("written entry must not end with a newline")


if __name__ == "__main__":
    main()
