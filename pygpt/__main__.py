from .user_interface import UserInterface

def __main__() -> None:
    r"""
    Main entry point of the package.

    This method contains the script to run if the user enter the name of the package on the command line. 

    .. code-block:: console
        pygpt
        
    """
    user_interface = UserInterface()
    user_interface.run()

def __main_gui__() -> None:
    r"""
    Graphical user interface entry point of the package.

    This method contains the script to run if the user enter the name of the package on the command line with the ``gui`` extension.

    .. code-block:: console
        pygpt-gui
        
    """
    raise NotImplementedError("The graphical user interface entry point is not implemented yet.")

