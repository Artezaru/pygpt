import openai
from .message import Message

class GPTApi(object):
    """
    `GPTApi` is a class that provides an interface to communicate with OpenAI's GPT models.

    This class facilitates connecting to the OpenAI API using an API key, setting the desired GPT model, and sending messages to obtain responses from the model. The supported models are restricted to `"gpt-3.5-turbo"` and `"gpt-4"`.

    Parameters
    ----------
    api_key : bytearray
        The API key used to authenticate with the OpenAI API. It must be a `bytearray`.

    model : str
        The name of the GPT model to be used. It must be one of the following: `["gpt-3.5-turbo", "gpt-4"]`. Default is `"gpt-3.5-turbo"`.
    """

    _correct_models = [
        "gpt-3.5-turbo",
        "gpt-4",
    ]

    def __init__(self, 
                 api_key: bytearray,
                 model: str = "gpt-3.5-turbo") -> None:
        """
        Initializes the GPTApi instance with an API key and an optional model.

        Parameters
        ----------
        api_key : bytearray
            The API key used for authentication with OpenAI.

        model : str, optional
            The name of the GPT model to use. Default is `"gpt-3.5-turbo"`.

        Raises
        ------
        ValueError
            If the model is not a valid string or not in the list of supported models.
        """
        self.api_key = api_key
        self.model = model

    @property
    def model(self) -> str:
        """
        Getter for the model attribute.

        Returns
        -------
        str
            The currently configured GPT model.
        """
        return self._model
    
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
            If the model is not a string or not in the list of supported models.
        """
        if not isinstance(model, str):
            raise ValueError("model must be a string")
        if model not in self._correct_models:
            raise ValueError(f"model must be in {self._correct_models}")
        self._model = model

    @property
    def api_key(self) -> bytearray:
        """
        Getter for the api_key attribute.

        Returns
        -------
        bytearray
            The API key used for authentication.
        """
        return self._api_key
    
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
            If the API key is not a `bytearray`.
        """
        if not isinstance(api_key, bytearray):
            raise ValueError("api_key must be a bytearray")
        self._api_key = api_key
        self._connect_api_key()

    def _connect_api_key(self) -> None:
        """
        Internal method to configure the OpenAI API key.

        This method decodes the API key and sets it for the OpenAI library.
        """
        openai.api_key = self.api_key.decode('utf-8')

    def ask_gpt(self, message: Message) -> str:
        """
        Sends a message to the GPT model and retrieves the response.

        Parameters
        ----------
        message : Message
            A `Message` object containing the message history and the input for the GPT model.

        Returns
        -------
        str
            The response content from the GPT model.

        Raises
        ------
        ValueError
            If the `message` parameter is not an instance of `Message`.

        Exceptions
        ----------
        openai.AuthenticationError
            Raised if the API key is invalid or not configured correctly.
        
        openai.OpenAIError
            Raised for any other API-related errors.

        Exception
            Raised for any unexpected errors during execution.
        """
        if not isinstance(message, Message):
            raise ValueError("message must be a Message object")
        try:
            response = openai.chat.completions.create(
                messages=message.message,
                model=self.model
            )
            return response.choices[0].message.content
        except openai.AuthenticationError as e:
            return f"Error - invalid or not configured API key: {e}"
        except openai.OpenAIError as e:
            return f"Error - related to the OpenAI API: {e}"
        except Exception as e:
            return f"Error - Unexpected error: {e}"
