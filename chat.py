import os
from datetime import datetime
from dotenv import load_dotenv
import anthropic
from progress.bar import Bar
from loguru import logger

# Configure loguru logger
logger.add("conversations.log", rotation="1 day", retention="7 days", level="INFO")
logger.add(lambda msg: print(msg, end=""), level="INFO", format="{time:HH:mm:ss} | {level} | {message}")

MAX_TOKENS = 4096
N_ROUNDS = 4 # number of rounds of conversation
N_TURNS = 2 # number of times the two models go back and forth per round
CLAUDE_MODEL = "claude-3-5-sonnet-20240620"
# CLAUDE_MODEL = 'claude-opus-4-20250514'

logger.info(f"Starting conversation with model: {CLAUDE_MODEL}")
logger.info(f"Configuration: {N_ROUNDS} rounds, {N_TURNS} turns per round, max tokens: {MAX_TOKENS}")

# open first_message.md as first_message
with open("first_message.md", "r") as f:
    FIRST_MESSAGE = f.read()

logger.info(f"Loaded initial thesis from first_message.md: {FIRST_MESSAGE}")

COMMON_SYSTEM_PROMPT = """
You are engaging in a Socratic dialogue.
Be brief. Skip niceties.
Get to the bottom of the topic.
The conversation is endless.
Do not conclude the conversation.
Support claims with evidence and data.
"""

SYSTEM_PROMPT_CLAUDE_1 = f"""
{COMMON_SYSTEM_PROMPT}
Respond to the critical questions.
"""

SYSTEM_PROMPT_CLAUDE_2 = f"""
{COMMON_SYSTEM_PROMPT}
Offer skeptical questions to improve the other model's argument.
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
logger.debug("Initialized Anthropic client")

def get_claude_response(messages, system_prompt):
    logger.debug(f"Making API call with {len(messages)} messages")
    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS,
            messages=messages,
            system=system_prompt,
        )
        response_text = response.content[0].text
        logger.debug(f"Received response of {len(response_text)} characters")
        return response_text
    except Exception as e:
        logger.error(f"API call failed: {e}")
        raise

# initialize the conversation with the initial thesis
thesis = FIRST_MESSAGE
logger.debug("Starting conversation rounds")

for round in range(N_ROUNDS):
    logger.debug(f"=== Starting Round {round + 1}/{N_ROUNDS} ===")

    # Start the conversation with an initial message
    messages_claude2 = [
        {"role": "user", "content": thesis}
    ]

    messages_claude1 = [
        {"role": "assistant", "content": thesis}
    ]

    for turn in range(N_TURNS):  # Run n turns of back-and-forth
        logger.debug(f"Round {round + 1}, Turn {turn + 1}/{N_TURNS}")
        
        # Claude 2 responds
        logger.debug("Claude 2 (skeptic) responding...")
        claude2_reply = get_claude_response(messages_claude2, SYSTEM_PROMPT_CLAUDE_2)
        logger.info(f"Claude 2 (skeptic) response: {claude2_reply}")
        progress_bar.next()

        messages_claude2.append({"role": "assistant", "content": claude2_reply})
        messages_claude1.append({"role": "user", "content": claude2_reply})

        # Claude 1 responds
        logger.debug("Claude 1 (advocate) responding...")
        claude1_reply = get_claude_response(messages_claude1, SYSTEM_PROMPT_CLAUDE_1)
        logger.info(f"Claude 1 (advocate) response: {claude1_reply}")
        progress_bar.next()

        messages_claude1.append({"role": "assistant", "content": claude1_reply})
        messages_claude2.append({"role": "user", "content": claude1_reply})

    # Moderator responds with a revised thesis
    logger.debug("Moderator revising thesis...")
    moderator_reply = get_claude_response(messages_claude2, SYSTEM_PROMPT_MODERATOR)
    progress_bar.next()

    messages_claude2.append({"role": "user", "content": moderator_reply})

    # update the thesis
    thesis = moderator_reply
    logger.info(f"Round {round + 1} complete. Thesis updated: {thesis}")

progress_bar.finish()
logger.info(f"Conversation complete! Final thesis: {thesis}")
