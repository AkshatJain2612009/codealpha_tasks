# Basic Rule-Based Chatbot
"""
A simple chatbot that responds to a few predefined user inputs.
It demonstrates:
- Functions
- if‑elif statements
- while loop for continuous conversation
- input / print for I/O
"""

def get_reply(user_input: str) -> str:
    """Return a predefined reply based on the user's input.

    Args:
        user_input: The raw string entered by the user.
    Returns:
        A reply string. If the input is not recognised, a default
        fallback response is returned.
    """
    # Normalise the input to make matching easier
    normalized = user_input.strip().lower()
    if normalized in {"hello", "hi", "hey"}:
        return "Hi!"
    elif normalized in {"how are you", "how are you?"}:
        return "I'm fine, thanks!"
    elif normalized in {"bye", "goodbye", "exit"}:
        return "Goodbye!"
    else:
        return "I didn't understand that. Try 'hello', 'how are you' or 'bye'."


def main() -> None:
    """Run the interactive chatbot loop.

    The loop continues until the user says a farewell phrase.
    """
    print("Simple Chatbot – type something (type 'bye' to quit)")
    while True:
        try:
            user_input = input("> ")
        except (EOFError, KeyboardInterrupt):
            # Gracefully handle Ctrl‑D / Ctrl‑C
            print("\nGoodbye!")
            break

        reply = get_reply(user_input)
        print(reply)
        # Exit condition – match the farewell reply
        if reply.lower().startswith("goodbye"):
            break


if __name__ == "__main__":
    main()

