import json
import datetime
from typing import Optional
from .message import Message
from .gpt_api import GPTApi


class Discussion:
    """
    `Discussion` manages the entire flow of a conversation, including saving and loading messages
    to and from a JSON file. It ensures that the discussion remains within token limits by
    summarizing the conversation when necessary.

    Parameters
    ----------
    api_key : bytearray
        The API key used for authentication with OpenAI.

    token_limit : int, optional
        The maximum number of tokens allowed in the summarized discussion. Default is 4096.

    model : str, optional
        The GPT model to use (e.g., "gpt-3.5-turbo" or "gpt-4"). Default is "gpt-3.5-turbo".
    """

    def __init__(self, api_key: bytearray, token_limit: int = 4096, model: str = "gpt-3.5-turbo") -> None:
        self.token_limit = token_limit
        self.gpt_api = GPTApi(api_key=api_key, model=model)
        self.complete_message = Message()
        self.resume_message = Message()
        self.title = None
        self.created_date = None
        self.modified_date = None

    @property
    def token_limit(self) -> int:
        """
        Getter for the token_limit attribute.

        Returns
        -------
        int
            The maximum number of tokens allowed in the summarized discussion.
        """
        return self._token_limit

    @token_limit.setter
    def token_limit(self, token_limit: int) -> None:
        """
        Setter for the token_limit attribute.

        Parameters
        ----------
        token_limit : int
            The maximum number of tokens allowed in the summarized discussion.
        """
        if not isinstance(token_limit, int) or token_limit <= 0:
            raise ValueError("Token limit must be a positive integer.")
        self._token_limit = token_limit

    @property
    def model(self) -> str:
        """
        Getter for the model attribute.

        Returns
        -------
        str
            The GPT model to use.
        """
        return self.gpt_api.model
    
    @model.setter
    def model(self, model: str) -> None:
        """
        Setter for the model attribute.

        Parameters
        ----------
        model : str
            The name of the GPT model to use.

        Raises
        ------
        ValueError
            If the model is not a valid string or not in the list of supported models.
        """
        self.gpt_api.model = model

    @property
    def api_key(self) -> bytearray:
        """
        Getter for the api_key attribute.

        Returns
        -------
        bytearray
            The API key used for authentication.
        """
        return self.gpt_api.api_key

    @api_key.setter
    def api_key(self, api_key: bytearray) -> None:
        """
        Setter for the api_key attribute.

        Parameters
        ----------
        api_key : bytearray
            The API key used for authentication.

        Raises
        ------
        ValueError
            If the API key is not a valid bytearray.
        """
        self.gpt_api.api_key = api_key

    @property
    def title(self) -> Optional[str]:
        """
        Gets the title of the discussion.

        Returns
        -------
        Optional[str]
            The title of the discussion, or `None` if no title is set.
        """
        return self._title

    @title.setter
    def title(self, title: Optional[str]) -> None:
        """
        Sets the title of the discussion.

        Parameters
        ----------
        title : Optional[str]
            The title to set for the discussion.
        """
        if title is not None and not isinstance(title, str):
            raise ValueError("Title must be a string or None.")
        self._title = title

    @property
    def created_date(self) -> Optional[datetime.datetime]:
        """
        Gets the creation date of the discussion.

        Returns
        -------
        Optional[datetime.datetime]
            The creation date of the discussion, or `None` if no creation date is set.
        """
        return self._created_date
    
    @created_date.setter
    def created_date(self, created_date: Optional[datetime.datetime]) -> None:
        """
        Sets the creation date of the discussion.

        Parameters
        ----------
        created_date : Optional[datetime.datetime]
            The creation date to set for the discussion.
        """
        if created_date is not None and not isinstance(created_date, datetime.datetime):
            raise ValueError("Create date must be a datetime object or None.")
        self._created_date = created_date
    
    @property
    def modified_date(self) -> Optional[datetime.datetime]:
        """
        Gets the last update date of the discussion.

        Returns
        -------
        Optional[datetime.datetime]
            The last update date of the discussion, or `None` if no update date is set.
        """
        return self._modified_date

    @modified_date.setter
    def modified_date(self, modified_date: Optional[datetime.datetime]) -> None:
        """
        Sets the last update date of the discussion.

        Parameters
        ----------
        modified_date : Optional[datetime.datetime]
            The last update date to set for the discussion.
        """
        if modified_date is not None and not isinstance(modified_date, datetime.datetime):
            raise ValueError("Update date must be a datetime object or None.")
        self._modified_date = modified_date

    @property
    def system_content(self) -> Optional[str]:
        """
        Gets the content of the system message.

        Returns
        -------
        Optional[str]
            The content of the system message, or `None` if no system message exists.
        """
        return self.resume_message.system_content
    
    @system_content.setter
    def system_content(self, content: Optional[str]) -> None:
        """
        Sets the content of the system message.

        If the content is `None`, the system message is removed from the conversation.
        Otherwise, the system message is added or updated.

        Parameters
        ----------
        content : Optional[str]
            The content to set for the system message. If `None`, the system message is removed.
        """
        self.resume_message.system_content = content
        self.complete_message.system_content = content

    def clear(self) -> None:
        """
        Clears the current discussion data.
        """
        self.complete_message.clear()
        self.resume_message.clear()
        self.title = None
        self.created_date = None
        self.modified_date = None

    def add_user_question(self, question: str) -> str:
        """
        Adds a user's question to the discussion.

        The question is added to both the complete and summarized discussions. If the summarized
        discussion exceeds the token limit, it is summarized.

        Parameters
        ----------
        question : str
            The user's question to add to the discussion.

        Returns
        -------
        str
            The GPT model's response.
        """
        # Add the question to the complete and summarized messages
        self.complete_message.add_message("user", question)
        self.resume_message.add_message("user", question)

        # Send the summarized message to GPT
        response = self.gpt_api.ask_gpt(self.resume_message)

        # Add the assistant's response to both messages
        self.complete_message.add_message("assistant", response)
        self.resume_message.add_message("assistant", response)

        # Check if the summarized message is over the token limit
        if self._is_over_token_limit():
            self.handle_long_discussion()

        return response

    def load(self, file_path: str) -> None:
        """
        Loads the discussion from a JSON file.

        This method clears the current discussion data before loading the new discussion
        from the file to ensure a clean state.

        Parameters
        ----------
        file_path : str
            The path to the JSON file containing the discussion.

        Raises
        ------
        FileNotFoundError
            If the specified file does not exist.
        """
        self.complete_message.clear()
        self.resume_message.clear()

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.title = data.get("title", None)
                self.model = data.get("model", "gpt-3.5-turbo")
                self.token_limit = data.get("token_limit", 4096)
                self.created_date = datetime.datetime.fromisoformat(data["created_date"])
                self.modified_date = datetime.datetime.fromisoformat(data["modified_date"])
                self.complete_message._message = data.get("complete_message", [])
                self.resume_message._message = data.get("resume_message", [])
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{file_path}' not found.")

    def dump(self, file_path: str) -> None:
        """
        Saves the discussion to a JSON file.

        Parameters
        ----------
        file_path : str
            The path to the JSON file where the discussion will be saved.
        """
        data = {}
        # Prepare the data to be saved
        if self.title is not None:
            data["title"] = self.title

        if self.created_date is not None:
            data["created_date"] = self.created_date.isoformat()
        else:
            data["created_date"] = datetime.datetime.now().isoformat()
        
        data["modified_date"] = datetime.datetime.now().isoformat()

        data["complete_message"] = self.complete_message.message
        data["resume_message"] = self.resume_message.message

        data["token_limit"] = self.token_limit
        data["model"] = self.model

        # Save the data to the file
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def handle_long_discussion(self) -> None:
        """
        Summarizes the discussion if it exceeds the token limit.

        The summarized conversation replaces the current resume message.
        """
        old_system_content = self.resume_message.system_content
        # Ask GPT to summarize the conversation
        self.resume_message.system_content = "Summarizing the conversation..."
        self.resume_message.add_message("user", f"Summarize the conversation less than {int(self.token_limit/4)} tokens.")
        summary = self.gpt_api.ask_gpt(self.resume_message)
        # Replace the summarized message with the new summary
        self.resume_message.clear()
        self.resume_message.system_content = old_system_content
        self.resume_message.add_message("user", "Summarize the previous conversation less than {int(self.token_limit/4)} tokens.")
        self.resume_message.add_message("assistant", summary)

    def _is_over_token_limit(self) -> bool:
        """
        Checks if the resume message exceeds the token limit.

        Returns
        -------
        bool
            True if the message exceeds the token limit, False otherwise.
        """
        # Estimate token count based on message content length
        token_count = int(sum(len(msg["content"]) for msg in self.resume_message.message)/4)
        return token_count > self.token_limit
