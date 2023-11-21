"""Facilitates asking a question to ChatGPT through CLI."""
from typing import Dict, Optional

from typeguard import typechecked

from jsonmodipy.arg_parser.process_args_engine import Llm_and_coms
from jsonmodipy.chatgpt35.conversations.Conversation import Gpt_conversation
from jsonmodipy.chatgpt35.website_question import ask_chatgpt35
from jsonmodipy.file_parsing import load_config
from jsonmodipy.Hardcoded import Hardcoded


@typechecked
def ask_question(
    *,
    coms: Llm_and_coms,
    question: str,
    config: Optional[Dict[str, Dict[str, str]]] = None,
    conversation: Optional[Gpt_conversation] = None,
) -> Gpt_conversation:
    """Initialises the chatbot and asks the question."""
    loaded_config: Dict[str, Dict[str, str]]
    if config is None:
        hardcoded: Hardcoded = Hardcoded()
        loaded_config = load_config(
            config_filepath=hardcoded.config_filepath,
            coms=coms,
        )
    else:
        loaded_config = config
    if coms.engine == "chatgpt3.5":
        creds: Dict[str, str] = loaded_config["chatgpt3.5"]

        return ask_chatgpt35(
            username=creds["username"],
            password=creds["password"],
            question=question,
            conversation=conversation,
        )
    raise NotImplementedError(
        f"Error, LLM: {coms.engine} not yet implemented."
    )
