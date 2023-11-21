"""Processes API arguments stores the LLM engine and communication channel."""
from argparse import Namespace

from typeguard import typechecked


# pylint: disable=R0903
class Llm_and_coms:
    """Stores the LLM communication target and method. E.g. which engine, and
    whether to use API, browser or other communication channel.

    Attributes:
        engine (str): The name of the LLM model/engine that is to be used.
        channel (str): The chosen communication method with the LLM model.
    """

    @typechecked
    def __init__(
        self,
        engine: str,
        channel: str,
    ):
        """Initializes LLM model target and communication method.

        Args:
            engine (str): The name of the LLM model/engine that is to be used.
            channel (str): The chosen communication method with the LLM model.
        """
        if engine == "chatgpt3.5":
            self.engine: str = engine
            if channel == "browser":
                self.channel: str = channel
            else:
                raise NotImplementedError(
                    f"Error, using official API for LLM:{engine} is not yet"
                    + " implemented."
                )
        else:
            raise NotImplementedError(
                f"Error, LLM:{engine} is not yet implemented."
            )


@typechecked
def process_api_args_engine(
    *,
    args: Namespace,
) -> Llm_and_coms:
    """Stores the LLM communication target and method.

    E.g. which engine, and whether to use API, browser or other
    communication channel.
    """
    return Llm_and_coms(
        engine=args.engine,
        channel=args.channel,
    )
