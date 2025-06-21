import os
from datetime import datetime
from dotenv import load_dotenv
import anthropic
from progress.bar import Bar

MAX_TOKENS = 4096
N_ROUNDS = 4 # number of rounds of conversation
N_TURNS = 2 # number of times the two models go back and forth per round
CLAUDE_MODEL = "claude-3-5-sonnet-20240620"
# CLAUDE_MODEL = 'claude-opus-4-20250514'

# open first_message.md as first_message
with open("first_message.md", "r") as f:
    FIRST_MESSAGE = f.read()


COMMON_SYSTEM_PROMPT = """
Be brief. Skip niceties.
Get to the bottom of the topic.
The conversation is endless.
Do not conclude the conversation.
"""

SYSTEM_PROMPT_CLAUDE_1 = f"""
{COMMON_SYSTEM_PROMPT}
Argue in favor.
"""

SYSTEM_PROMPT_CLAUDE_2 = f"""
{COMMON_SYSTEM_PROMPT}
Offer skeptical criticism to improve the other model's argument.
"""

SYSTEM_PROMPT_MODERATOR = f"""
Create a more robust version of this thesis: {FIRST_MESSAGE}
Integrate skeptical arguments. But support the original thesis.
Be brief. Skip niceties.
The revised thesis is for a new audience who has not followed the conversation or read the initial thesis.
Only respond with the revised thesis.
"""

# Create a progress bar
progress_bar = Bar(
    "Progress",
    max=N_ROUNDS*(N_TURNS*2) + N_ROUNDS,
    # width=50,
)
progress_bar.update()  # Force display at 0%

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_claude_response(messages, system_prompt):
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=MAX_TOKENS,
        messages=messages,
        system=system_prompt,
    )
    return response.content[0].text

# initialize the conversation with the initial thesis
thesis = FIRST_MESSAGE

for round in range(N_ROUNDS):

    # Start the conversation with an initial message
    messages_claude2 = [
        {"role": "user", "content": thesis}
    ]

    messages_claude1 = [
        {"role": "assistant", "content": thesis}
    ]

    for turn in range(N_TURNS):  # Run n turns of back-and-forth
        # Claude 2 responds
        claude2_reply = get_claude_response(messages_claude2, SYSTEM_PROMPT_CLAUDE_2)
        progress_bar.next()

        messages_claude2.append({"role": "assistant", "content": claude2_reply})
        messages_claude1.append({"role": "user", "content": claude2_reply})

        # Claude 1 responds
        claude1_reply = get_claude_response(messages_claude1, SYSTEM_PROMPT_CLAUDE_1)
        progress_bar.next()

        messages_claude1.append({"role": "assistant", "content": claude1_reply})
        messages_claude2.append({"role": "user", "content": claude1_reply})

    # Moderator responds with a revised thesis
    moderator_reply = get_claude_response(messages_claude2, SYSTEM_PROMPT_MODERATOR)
    progress_bar.next()

    messages_claude2.append({"role": "user", "content": moderator_reply})

    # update the thesis
    thesis = moderator_reply

progress_bar.finish()
print(thesis)
