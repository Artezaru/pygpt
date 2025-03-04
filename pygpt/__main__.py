from .user_interface import UserInterface

def main() -> None:
    r"""
    This method contains the script to run if the user enter the name of the package on the command line. 

    .. code-block:: console
        pygpt
        
    """
    ui = UserInterface()
    ui.run()

if __name__ == "__main__":
    main()