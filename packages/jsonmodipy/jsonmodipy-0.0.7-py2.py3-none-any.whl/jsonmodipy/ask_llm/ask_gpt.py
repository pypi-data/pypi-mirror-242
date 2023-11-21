"""Facilitates asking a question to ChatGPT through CLI."""
from typing import Dict, Optional

from typeguard import typechecked

from jsonmodipy.arg_parser.process_args_engine import Llm_and_coms
from jsonmodipy.chatgpt35.conversations.Conversation import Gpt_conversation
from jsonmodipy.chatgpt35.website_question import ask_chatgpt35


@typechecked
def ask_question(
    *,
    coms: Llm_and_coms,
    question: str,
    config: Dict[str, Dict[str, str]],
    conversation: Optional[Gpt_conversation] = None,
) -> Gpt_conversation:
    """Initialises the chatbot and asks the question."""
    if coms.engine != "chatgpt3.5":
        raise NotImplementedError(
            f"Error, LLM: {coms.engine} not yet implemented."
        )

    creds: Dict[str, str] = config[coms.engine]
    return ask_chatgpt35(
        username=creds["username"],
        password=creds["password"],
        question=question,
        conversation=conversation,
    )
