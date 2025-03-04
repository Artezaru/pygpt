from typing import List, Dict, Optional


class Message(object):
    """
    `Message` is a class designed to construct and manage messages exchanged with the GPT model.

    This class provides methods to initialize, update, clear, and append to the message history.
    Messages are formatted according to the structure required by OpenAI's API, where each message consists of a `role` and `content`.
    """

    def __init__(self) -> None:
        """
        Initializes the `Message` object and clears any existing messages.

        This ensures that the message history starts empty.
        """
        self.clear()

    @property
    def message(self) -> List[Dict[str, str]]:
        """
        Getter for the `message` attribute.

        Returns
        -------
        List[Dict[str, str]]
            The current list of messages in the conversation.
        """
        return self._message

    def clear(self) -> None:
        """
        Clears the message history.

        This method resets the message list to an empty state.
        """
        self._message = []

    def clear_except_system(self) -> None:
        """
        Clears all messages except the system message.

        This method retains the first message if it has the `role` set to `"system"`.
        """
        if len(self._message) > 0 and self._message[0]["role"] == "system":
            self._message = [self._message[0]]
        else:
            self.clear()

    @property
    def system_content(self) -> Optional[str]:
        """
        Gets the content of the system message.

        Returns
        -------
        Optional[str]
            The content of the system message, or `None` if no system message exists.
        """
        if len(self._message) > 0 and self._message[0]["role"] == "system":
            return self._message[0]["content"]
        return None

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
        if content is None:
            # Remove the system message if it exists
            if len(self._message) > 0 and self._message[0]["role"] == "system":
                self._message.pop(0)
        else:
            # If no system message exists or the first message is not a system message, add it
            if len(self._message) == 0 or self._message[0]["role"] != "system":
                self._message.insert(0, {"role": "system", "content": content})
            else:
                # Update the existing system message
                self._message[0]["content"] = content

    def add_message(self, role: str, content: str) -> None:
        """
        Adds a single message to the conversation history.

        If the role is `"system"`, this method updates the system content using the `system_content` property.

        Parameters
        ----------
        role : str
            The role of the message sender. Valid values are typically `"user"`, `"assistant"`, or `"system"`.

        content : str
            The message content to be added.

        Raises
        ------
        ValueError
            If the `role` is not a string or if `content` is not a string.
        """
        if not isinstance(role, str):
            raise ValueError("role must be a string")
        if not isinstance(content, str):
            raise ValueError("content must be a string")

        # If the role is "system", use system_content property
        if role == "system":
            self.system_content = content
        else:
            # Add the message to the history
            self._message.append({"role": role, "content": content})
