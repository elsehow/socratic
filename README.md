# socratic

A Python script that strengthens a thesis using socratic dialgoue.

- **Input**: Thesis (in `first_message.py`)
- **Output:** A more robust version of the thesis.

Full debates are saved to `conversations.log`

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

## License

BSD-3