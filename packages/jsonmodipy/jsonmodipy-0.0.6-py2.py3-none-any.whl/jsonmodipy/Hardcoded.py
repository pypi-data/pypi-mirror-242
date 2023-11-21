"""Stores hardcoded project data."""


from typeguard import typechecked


# pylint: disable=R0903
class Hardcoded:
    """Stores hardcoded data."""

    @typechecked
    def __init__(self) -> None:
        """Initialise the hardcoded data."""
        self.indent_spaces: int = 4
        self.json_identifier = "json_"
        self.reconstruct_id = "reconstructed_"
        self.config_filepath = "../config.ini"
        self.llm_storage_dirname = "__llm_storage__"
        self.json_structures_dir = "json_structures"
        self.user_data_dir = "../user_data_dir"

    @typechecked
    def getJsonTructureFilename(self, target_repopath: str) -> str:
        """Get the filename of the json structure of a target repository.

        Args:
            target_repopath (str): The path to the target repository.

        Returns:
            str: The filename of the json structure of the target repository.
        """

        return target_repopath.split("/")[-1] + ".json"
