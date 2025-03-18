import os
import sys
import pyperclip
import json
import random
import datetime
from typing import List, Tuple
import string
from rich import print
from rich.table import Table
from .discussion import Discussion


class UserInterface:
    r"""
    `UserInterface` handles interactions with the local user for managing discussions.

    Initializes the `UserInterface` object.

    This sets up the basic structure for managing discussions.

    The discussion data is stored in the `~/.pygpt/discussions` directory.

    To set the OpenAI API key, use the environment variable `OPENAI_API_KEY`.

    .. code-block:: console

        export OPENAI_API_KEY=your-api-key

    Commands:
    ---------

    - [bold yellow]!open[/bold yellow] or [bold yellow]!o[/bold yellow]: List all discussions and allow the user to open a specific one.
    - [bold yellow]!new[/bold yellow] <[bold magenta]title[/bold magenta]> or [bold yellow]!n[/bold yellow] <[bold magenta]title[/bold magenta]>: Create a new discussion with the specified title.
    - [bold yellow]!close[/bold yellow] or [bold yellow]!x[/bold yellow]: Close the current discussion.
    - [bold yellow]!model[/bold yellow] <[bold magenta]model[/bold magenta]> or [bold yellow]!m[/bold yellow] <[bold magenta]model[/bold magenta]>: Change the GPT model for the current discussion.
    - [bold yellow]!title[/bold yellow] <[bold magenta]title[/bold magenta]> or [bold yellow]!t[/bold yellow] <[bold magenta]title[/bold magenta]>: Change the title of the current discussion.
    - [bold yellow]!delete[/bold yellow] or [bold yellow]!d[/bold yellow]: Delete the current discussion. This operation is irreversible.
    - [bold yellow]!delete_all[/bold yellow] or [bold yellow]!da[/bold yellow]: Delete all discussions. This operation is irreversible.
    - [bold yellow]!history[/bold yellow] or [bold yellow]!h[/bold yellow]: Display the complete history of the current discussion.
    - [bold yellow]!exit[/bold yellow] or [bold yellow]!q[/bold yellow]: Exit the program.
    - [bold yellow]!copy[/bold yellow] or [bold yellow]!c[/bold yellow]: Copy the last assistant response to the clipboard.
    - [bold yellow]!search[/bold yellow] <[bold magenta]content[/bold magenta]> or [bold yellow]!f[/bold yellow] <[bold magenta]content[/bold magenta]>: Search the content in the complete history of the current discussion.
    - [bold yellow]!info[/bold yellow] or [bold yellow]!i[/bold yellow]: Display information about the current discussion.
    - [bold yellow]!system[/bold yellow] <[bold magenta]message[/bold magenta]> or [bold yellow]!sys[/bold yellow] <[bold magenta]message[/bold magenta]>: Set the system message to the current discussion.
    - [bold yellow]!token_limit[/bold yellow] <[bold magenta]limit[/bold magenta]> or [bold yellow]!tl[/bold yellow] <[bold magenta]limit[/bold magenta]>: Set the token limit for the current discussion before resuming.
    - [bold yellow]!help[/bold yellow] or [bold yellow]!?[/bold yellow]: Display this help message.
    """

    def __init__(self) -> None:
        self.get_api_key()
        directory = os.path.expanduser("~/.pygpt/discussions")
        os.makedirs(directory, exist_ok=True)
        self.base_directory = directory
        os.makedirs(self.base_directory, exist_ok=True)
        self.discussion_util: Discussion = Discussion(api_key=self.api_key)
        self.discussion_code = None

    def get_api_key(self) -> None:
        """
        Retrieves the OpenAI API key from the environment variables.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            print("[bold red]Error:[/bold red] OpenAI API key not found. Set the environment variable OPENAI_API_KEY with your API key.\nUsage: [bold yellow]export OPENAI_API_KEY=your-api-key[/bold yellow]")
            exit(1)
        self.api_key = bytearray(api_key.encode("utf-8"))

    def run(self) -> None:
        """
        Starts the terminal interface for user interaction.
        """
        print("[bold cyan]Welcome to the GPT Discussion Tool![/bold cyan]")
        while True:
            user_input = input(">>> ").strip()
            if user_input.lower() == "!exit" or user_input.lower() == "!q":
                print("[bold cyan]Goodbye![/bold cyan]")
                break
            self.handle_input(user_input)
        sys.exit(0)

    def is_discussion_open(self) -> bool:
        """
        Checks if a discussion is currently open.

        Returns
        -------
        bool
            True if a discussion is open, False otherwise.
        """
        if self.discussion_code is None:
            print("[bold red]Error:[/bold red] No discussion loaded. Open or create one first using [bold yellow]!new[/bold yellow] or [bold yellow]!open[/bold yellow].")
            return False
        return True

    def handle_input(self, user_input: str) -> None:
        """
        Handles user input, checking for commands or passing input to GPT API.

        Parameters
        ----------
        user_input : str
            The input provided by the user.
        """
        if user_input.startswith("!"):
            command, *args = user_input.split(" ")
            self.handle_command(command, args)
        else:
            if not self.is_discussion_open():
                return
            self.handle_gpt_interaction(user_input)

    def handle_command(self, command: str, args: str) -> None:
        """
        Handles commands prefixed with `!`.

        Parameters
        ----------
        command : str
            The command name prefixed with `!`.

        args : str
            The arguments to the command, if any.
        """
        # New discussion
        if command == "!new" or command == "!n":
            if any(not arg.isalnum() for arg in args):
                print("[bold red]Error:[/bold red] Title must be alphanumeric.")
                return
            title = " ".join(args)
            self.create_new_discussion(title)

        # Open discussion
        elif command == "!open" or command == "!o":
            self.user_open_discussion()

        # Close discussion
        elif command == "!close" or command == "!x":
            self.user_close_discussion()

        # Change model
        elif command == "!model" or command == "!m":
            if not self.is_discussion_open():
                return
            if len(args) != 1:
                print("[bold red]Error:[/bold red] Missing model name. Usage: [bold yellow]!model[/bold yellow] <[bold magenta]model[/bold magenta]>")
                return
            model = args[0].strip().lower()
            self.change_model(model)
        
        # Set title
        elif command == "!title" or command == "!t":
            if not self.is_discussion_open():
                return
            if any(not arg.isalnum() for arg in args):
                print("[bold red]Error:[/bold red] Title must be alphanumeric.")
                return
            title = " ".join(args)
            self.set_title(title)

        # Delete discussion
        elif command == "!delete" or command == "!d":
            if not self.is_discussion_open():
                return
            self.delete_current_discussion()
        
        # Delete all discussions
        elif command == "!delete_all" or command == "!da":
            self.delete_all_discussions()
        
        # Display information about the current discussion
        elif command == "!info" or command == "!i":
            if not self.is_discussion_open():
                return
            self.display_info()
        
        # Set the system message for the current discussion
        elif command == "!system" or command == "!sys":
            if self.discussion_code is None:
                print("[bold red]Error:[/bold red] No discussion loaded. Open or create one first using [bold yellow]!new[/bold yellow] or [bold yellow]!open[/bold yellow].")
                return
            message = " ".join(args)
            self.set_system_message(message)

        # Set the token limit for the current discussion
        elif command == "!token_limit" or command == "!tl":
            if not self.is_discussion_open():
                return
            if len(args) != 1:
                print("[bold red]Error:[/bold red] Missing token limit. Usage: [bold yellow]!token_limit[/bold yellow] <[bold magenta]limit[/bold magenta]>")
                return
            if not args[0].isdigit() or int(args[0]) <= 1000:
                print("[bold red]Error:[/bold red] Token limit must be a positive integer greater than 1000.")
                return
            limit = int(args[0])
            self.set_token_limit(limit)
                    
        # Show the complete history of the current discussion
        elif command == "!history" or command == "!h":
            if not self.is_discussion_open():
                return
            self.show_history()

        # Copy the last assistant response to the clipboard
        elif command == "!copy" or command == "!c":
            if not self.is_discussion_open():
                return
            self.copy_last_assistant_response()

        # Search into the complete history of the current discussion
        elif command == "!search" or command == "!f":
            if not self.is_discussion_open():
                return
            if len(args) == 0:
                print("[bold red]Error:[/bold red] Missing search content. Usage: [bold yellow]!search[/bold yellow] <[bold magenta]content[/bold magenta]>")
                return
            content = " ".join(args)
            self.search_history(content)

        # Help command
        elif command == "!help" or command == "!?":
            print(self.__doc__)

        # Unknown command
        else:
            print(f"[bold red]Unknown command:[/bold red] {command}. Type [bold green]!help[/bold green] for a list of available commands.")

    def generate_discussion_code(self) -> str:
        """
        Generates a random code for the current discussion.

        Returns
        -------
        str
            A randomly generated code for the discussion.
        """
        code = None
        while code is None or os.path.isfile(os.path.join(self.base_directory, f"{code}.json")):
            code = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        return code

    def close_discussion(self) -> None:
        """
        Closes the current discussion and saves the conversation history.
        """
        if self.discussion_code is not None:
            self.save_discussion()
            self.discussion_util.clear()
            self.discussion_code = None

    def open_discussion(self, code: str) -> None:
        """
        Opens an existing discussion with the specified code.

        Parameters
        ----------
        code : str
            The code of the discussion to open.
        """
        if self.discussion_code is not None:
            self.close_discussion()
        filepath = os.path.join(self.base_directory, f"{code}.json")
        self.discussion_util.load(filepath)
        self.discussion_code = code
        string_title = f"[bold green]Opened discussion:[/bold green] [bold yellow]{self.discussion_util.title}[/bold yellow]"
        print("="*len(string_title)+"\n"+string_title+"\n"+"="*len(string_title))

    def save_discussion(self) -> None:
        """
        Saves the current discussion.
        """
        if self.discussion_code is not None:
            filepath = os.path.join(self.base_directory, f"{self.discussion_code}.json")
            self.discussion_util.dump(filepath)

    def create_new_discussion(self, title: str) -> None:
        """
        Creates a new discussion with the specified title.

        Parameters
        ----------
        title : str
            The title of the new discussion.
        """
        code = self.generate_discussion_code()
        # Close the current discussion and create a new one
        self.close_discussion()
        # Initialize the new discussion
        self.discussion_util.title = title
        self.discussion_code = code
        self.save_discussion() # Create the file for the new discussion
        # Open properly the new discussion
        self.open_discussion(code)

    def list_discussions(self) -> List[Tuple[int, str]]:
        """
        Lists all existing discussions.

        Returns
        -------
        List[Tuple[int, str]]
            A list of tuples containing the index and code of each discussion.
        """
        discussion_list = []
        # Get all discussion files
        files = os.listdir(self.base_directory)
        discussions = [file for file in files if file.endswith(".json")]
        # Display the discussions in a table
        table = Table(title="Available Discussions")
        table.add_column("ID", style="cyan")
        table.add_column("Code", style="cyan")
        table.add_column("Title", style="cyan")
        table.add_column("Created date", style="cyan")
        table.add_column("Last modified date", style="cyan")
        for i, discussion in enumerate(discussions, start=1):
            code = discussion[:-5]
            # Load the discussion file to get the title and dates
            with open(os.path.join(self.base_directory, discussion), "r") as file:
                data = json.load(file)
            title = data.get("title", "")
            created_date = datetime.datetime.fromisoformat(data["created_date"]).strftime("%Y-%m-%d %H:%M:%S")
            modified_date = datetime.datetime.fromisoformat(data["modified_date"]).strftime("%Y-%m-%d %H:%M:%S")
            # Add the discussion to the table
            table.add_row(str(i), code, title, created_date, modified_date)
            discussion_list.append((i, code))
        print(table)
        return discussion_list

    def user_open_discussion(self) -> None:
        """
        Lists all existing discussions and allows the user to open one.
        """
        discussion_list = self.list_discussions()
        # Check the user input and open the selected discussion
        selection = input("Enter the ID of the discussion to open or 0 to cancel: ").strip()
        while not selection.isdigit() or int(selection) not in range(0, len(discussion_list) + 1):
            print("[bold red]Error:[/bold red] Invalid selection. Please enter the ID of the discussion to open or [bold yellow]0[/bold yellow] to cancel.")
            selection = input("Enter the ID of the discussion to open: ").strip()
        # Cancel the operation if the user enters 0
        if selection == "0":
            return
        self.close_discussion()
        # Load the selected discussion
        self.open_discussion(discussion_list[int(selection) - 1][1])

    def user_close_discussion(self) -> None:
        """
        Closes the current discussion.
        """
        self.close_discussion()
        print("[bold cyan]Discussion closed successfully.[/bold cyan]")

    def change_model(self, model: str) -> None:
        """
        Changes the GPT model for the current discussion.

        Parameters
        ----------
        model : str
            The name of the GPT model to use.
        """
        try:
            self.discussion_util.model = model
            print(f"[bold cyan]Model changed to:[/bold cyan] [bold yellow]{model}[/bold yellow]")
        except ValueError as e:
            string_models = ""
            for m in self.discussion_util.gpt_api._correct_models:
                string_models += f"[bold yellow]{m}[/bold yellow], "
            print(f"[bold red]Error:[/bold red] {e}, valid models are: {string_models[:-1]}") # Remove the last comma

    def set_title(self, title: str) -> None:
        """
        Changes the title of the current discussion.

        Parameters
        ----------
        title : str
            The new title for the current discussion.
        """
        self.discussion_util.title = title
        self.save_discussion()
        # Display the new title
        print(f"[bold cyan]Title changed to:[/bold cyan] [bold yellow]{title}[/bold yellow]")

    def delete_current_discussion(self) -> None:
        """
        Deletes the current discussion. The user must confirm the deletion.
        This operation is irreversible.
        """
        confirm = input("Are you sure you want to delete the current discussion? [y/N]").strip().lower()
        while confirm not in ["y", "n", "yes", "no"]:
            print("[bold red]Error:[/bold red] Invalid input. Please enter [bold yellow]y[/bold yellow] to confirm or [bold yellow]n[/bold yellow] to cancel.")
            confirm = input("Are you sure you want to delete the current discussion? [y/N]: ").strip().lower()
        if confirm in ["y", "yes"]:
            filepath = os.path.join(self.base_directory, f"{self.discussion_code}.json")
            self.close_discussion()
            os.remove(filepath)
            print("[bold cyan]Discussion deleted successfully.[/bold cyan]")
        else:
            print("[bold cyan]Deletion cancelled.[/bold cyan]")
    
    def set_system_message(self, message: str) -> None:
        """
        Sets the system message for the current discussion.

        Parameters
        ----------
        message : str
            The content of the system message.
        """
        self.discussion_util.system_content = message
        self.save_discussion()
        print(f"[bold cyan]System message set to:[/bold cyan] [bold yellow]{message}[/bold yellow]")

    def delete_all_discussions(self) -> None:
        """
        Deletes all discussions. The user must confirm the deletion.
        This operation is irreversible.
        """
        confirm = input("Are you sure you want to delete all discussions? [y/N]").strip().lower()
        while confirm not in ["y", "n", "yes", "no"]:
            print("[bold red]Error:[/bold red] Invalid input. Please enter [bold yellow]y[/bold yellow] to confirm or [bold yellow]n[/bold yellow] to cancel.")
            confirm = input("Are you sure you want to delete all discussions? [y/N]: ").strip().lower()
        if confirm in ["y", "yes"]:
            self.close_discussion()
            for file in os.listdir(self.base_directory):
                if file.endswith(".json"):
                    os.remove(os.path.join(self.base_directory, file))
            print("[bold cyan]All discussions deleted successfully.[/bold cyan]")
        else:
            print("[bold cyan]Deletion cancelled.[/bold cyan]")

    def show_history(self) -> None:
        """
        Displays the complete history of the current discussion.
        """
        for message in self.discussion_util.complete_message.message:
            role = message["role"]
            content = message["content"]
            if role == "user":
                print(f"[bold yellow]User:[/bold yellow] {content}")
            elif role == "assistant":
                print(f"[bold blue]GPT:[/bold blue] {content}")
            elif role == "system":
                print(f"[bold magenta]System:[/bold magenta] {content}")

    def set_token_limit(self, limit: int) -> None:
        """
        Sets the token limit for the current discussion.

        Parameters
        ----------
        limit : int
            The token limit for the current discussion.
        """
        self.discussion_util.token_limit = limit
        self.save_discussion()
        print(f"[bold cyan]Token limit set to:[/bold cyan] [bold yellow]{limit}[/bold yellow]")

    def display_info(self) -> None:
        """
        Displays information about the current discussion.
        """
        table = Table(title="Discussion Information")
        table.add_column("Attribute", style="cyan")
        table.add_column("Value", style="cyan")
        table.add_row("Code", self.discussion_code)
        table.add_row("Title", self.discussion_util.title)
        table.add_row("Model", self.discussion_util.model)
        table.add_row("Token limit", str(self.discussion_util.token_limit))
        table.add_row("System message", self.discussion_util.system_content)
        print(table)

    def handle_gpt_interaction(self, user_input: str) -> None:
        """
        Sends user input to GPT API via the current discussion.

        Parameters
        ----------
        user_input : str
            The input text to send to GPT.
        """
        response = self.discussion_util.add_user_question(user_input)
        print(f"[bold blue]GPT:[/bold blue] {response}")
        self.save_discussion()

    def copy_last_assistant_response(self) -> None:
        """
        Copies the last assistant response to the clipboard.
        """
        # find the last assistant response
        last_response = None
        for message in reversed(self.discussion_util.complete_message.message):
            if message["role"] == "assistant":
                last_response = message["content"]
                break
        # if no response is found, return
        if last_response is None:
            print("[bold red]Error:[/bold red] No assistant response found.")
            return
        # copy the response to the clipboard
        pyperclip.copy(last_response)
        print("[bold cyan]Last assistant response copied to clipboard.[/bold cyan]")
    
    def search_history(self, content: str) -> None:
        """
        Searches the complete history of the current discussion for the specified content.

        Parameters
        ----------
        content : str
            The content to search for in the discussion history.
        """
        found_content = []
        found = False
        for message in self.discussion_util.complete_message.message:
            if content in message["content"]:
                found = True
                role = message["role"]
                if role == "user":
                    print(f"[bold yellow]User:[/bold yellow] {message['content']}")
                elif role == "assistant":
                    print(f"[bold blue]GPT:[/bold blue] {message['content']}")
                elif role == "system":
                    print(f"[bold magenta]System:[/bold magenta] {message['content']}")
        if not found:
            print(f"[bold red]Info:[/bold red] No message found with the content: {content}")