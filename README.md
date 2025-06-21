# socratic

A Python script that strengthens a thesis using socratic dialgoue.

- **Input**: Thesis (in `first_message.py`)
- **Output:** A more robust version of the thesis.

## Overview

This script simulates a structured debate between two AI models (Claude) to iteratively refine and strengthen arguments on a given topic.

- **Claude 1**: Argues in favor of the thesis
- **Claude 2**: Provides skeptical criticism to improve arguments
- **Moderator**: Synthesizes the discussion into a refined thesis for the next round

The conversation runs for multiple rounds, with each round consisting of several back-and-forth exchanges between the models, followed by a moderator synthesis that becomes the new thesis for the next round.

## install

```
cp sample.env .env
# place your API key in .env
pip install requirements.txt
```

## run

Update `first_message.md` to be your thesis.

Then:

```
python3 chat.py
```

## Requirements

- Python 3.7+
- Anthropic API key
- Required Python packages (see Installation)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd conversations
```

2. Install required packages:
```bash
pip install anthropic python-dotenv progress
```

3. Create a `.env` file in the project root:
```bash
ANTHROPIC_API_KEY=your_api_key_here
```

4. Ensure you have a `first_message.md` file with your initial thesis.

## Configuration

You can modify the following parameters in `chat.py`:

- `MAX_TOKENS`: Maximum tokens per response (default: 4096)
- `N_ROUNDS`: Number of conversation rounds (default: 4)
- `N_TURNS`: Number of back-and-forth exchanges per round (default: 2)
- `CLAUDE_MODEL`: Claude model to use (default: "claude-3-5-sonnet-20240620")

## Usage

Run the conversation simulator:

```bash
python chat.py
```

The script will:
1. Load the initial thesis from `first_message.md`
2. Run the specified number of rounds
3. Display progress with a progress bar
4. Output the final refined thesis

## Output

The final output is a refined thesis that incorporates:
- Original arguments in favor
- Skeptical criticisms and counterarguments
- Synthesized insights from the debate
- Strengthened reasoning and evidence

## File Structure

```
conversations/
├── chat.py                 # Main conversation simulator
├── first_message.md        # Initial thesis to debate
├── Conversations/          # Directory for saved conversations
└── README.md              # This file
```

## How It Works

1. **Initialization**: Loads the thesis from `first_message.md`
2. **Round Structure**: For each round:
   - Claude 2 provides skeptical criticism
   - Claude 1 defends and strengthens the argument
   - This exchange repeats for the specified number of turns
   - Moderator synthesizes the discussion into a new thesis
3. **Iteration**: The new thesis becomes the starting point for the next round
4. **Completion**: After all rounds, the final refined thesis is output

## System Prompts

The script uses three distinct system prompts:

- **Claude 1**: Focuses on arguing in favor of the thesis
- **Claude 2**: Provides skeptical criticism to improve arguments
- **Moderator**: Creates a robust, integrated version of the thesis

All prompts emphasize brevity, directness, and continuous conversation without premature conclusions.

## Customization

To use this with a different topic:

1. Replace the content in `first_message.md` with your thesis
2. Optionally adjust the system prompts in `chat.py` for different debate styles
3. Modify the number of rounds and turns as needed

## Notes

- The conversation is designed to be endless and non-conclusive
- Each model maintains its role throughout the conversation
- The moderator's role is to integrate rather than choose sides
- API costs will depend on the number of rounds and turns configured

## License

[Add your license information here] 