import logging
import os
from typing import Any

from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.chat_models.fake import FakeMessagesListChatModel
from langchain.schema import AIMessage
from pydantic import BaseModel, PrivateAttr

from codeas.codebase import Codebase
from codeas.file_handler import FileHandler
from codeas.initializer import Initializer
from codeas.request import Request
from codeas.utils import read_yaml

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class Assistant(BaseModel, validate_assignment=True, extra="forbid"):
    """Assistant is the main class of the codeas package. It is used to
    initialize the configs, execute prompts, and apply or reject changes.

    Attributes
    ----------
    codebase : Codebase
        Description
    file_handler : FileHandler
        Description
    max_tokens_per_module : int, optional
        Description, by default 2000
    model : str, optional
        Description, by default "gpt-3.5-turbo"
    """

    codebase: Codebase = Codebase()
    file_handler: FileHandler = FileHandler()
    max_tokens_per_module: int = 8000
    model: str = "gpt-3.5-turbo-1106"
    _prompts: dict = PrivateAttr(default_factory=dict)
    _openai_model: object = PrivateAttr(None)

    def model_post_init(self, __context: Any) -> None:
        """When the model is instantiated, this method is called to set the assistant
        attributes based on the configurations (if initialized).
        """
        if os.path.exists(".codeas/prompts.yaml"):
            self._set_prompts()
        self._set_openai_model()
        self._parse_codebase()

    def _set_prompts(self):
        self._prompts = read_yaml(".codeas/prompts.yaml")

    def _set_openai_model(self):
        if self.model == "fake":
            dummy_func = """def dummy_func():\n    pass"""
            msg = AIMessage(content=dummy_func)
            self._openai_model = FakeMessagesListChatModel(responses=[msg])
        else:
            self._openai_model = ChatOpenAI(
                model=self.model,
                callbacks=[StreamingStdOutCallbackHandler()],
                streaming=True,
            )

    def _parse_codebase(self):
        self.codebase.parse_modules()

    def init_configs(self, source_path: str = None):
        """Initialize the assistant configurations. If source_path is None, default
        configurations are used. Otherwise, the configurations in the source_path
        directory are used.
        """
        initializer = Initializer()
        initializer.init_configs(self, source_path)

    def execute_preprompt(self, name: str):
        """Execute a preprompt from prompts.yaml file

        Parameters
        ----------
        name : str
            The name of the preprompt
        """
        self._check_prompt_name(name)
        logging.info(f"Executing preprompt {name}")
        self.execute_prompt(self._prompts[name])

    def _check_prompt_name(self, name: str):
        if name not in self._prompts.keys():
            err_msg = f"Prompt {name} not found in prompts.yaml"
            logging.error(err_msg)
            raise ValueError(err_msg)

    def execute_prompt(self, instructions: str):
        """Execute a prompt on the codebase

        Parameters
        ----------
        instructions : str
            The instructions for the model to perform
        guideline_prompt : List[str], optional
            The list of guidelines to be used in the prompt, by default None
        """
        logging.info(f"Executing prompt {instructions}")
        request = Request(
            instructions=instructions,
            guidelines=self._prompts.get("guidelines"),
            model=self._openai_model,
        )
        request.execute(self.codebase)
        self.file_handler.export_modifications(self.codebase)

    def apply_changes(self):
        logging.info("Applying changes")
        self.file_handler.make_backup_dir()
        # handling the case when we generate files for the first time
        # TODO: need to think about how to better handle this in general
        try:
            self.file_handler.move_target_files_to_backup()
        except FileNotFoundError:
            pass
        self.file_handler.move_preview_files_to_target()

    def revert_changes(self):
        # this mechanism for undoing is not valid under the new CLI logic and should be reviewed
        logging.info("Reverting changes")
        self.file_handler.move_target_files_to_preview()
        self.file_handler.move_backup_files_to_target()
        self.file_handler.reset_backup_files()

    def reject_changes(self):
        logging.info("Rejecting changes")
        self.file_handler.remove_preview_files()
