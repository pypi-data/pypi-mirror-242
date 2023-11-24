import os
import sys
from importlib import import_module
import click

BASE_DIRECTORY = "cli"


class Command:
    def __init__(self, name) -> None:
        # Construct the module path and extract the name of the command
        self.module_path = f"{BASE_DIRECTORY}.{name}"
        self.name = name.split(".")[-1]

    def module(self):
        # Dynamically import the module and return a Click command
        imported_module = import_module(self.module_path)
        return click.command()(getattr(imported_module, self.name, None))


class Group:
    def __init__(self, name) -> None:
        # Set the module path and folder path for the group
        self.module_path = f"{BASE_DIRECTORY}.{name}"
        self.folder_path = self.module_path.replace(".", "/")
        self.name = name

    def _load_commands(self, group):
        # Load commands from the specified folder into the Click group
        for item in os.listdir(self.folder_path):
            if self._is_valid_file(item, self.folder_path):
                # Create a Command object and add it to the group
                command = Command(f"{self.module_path[4:]}.{item[:-3]}")
                group.add_command(command.module())

    def _is_valid_file(self, item, folder_path):
        # Check if the item is a valid file (not starting with "__")
        return not item.startswith("__") and os.path.isfile(
            os.path.join(folder_path, item)
        )

    def module(self):
        # Dynamically import the module and return a Click group with loaded commands
        imported_module = import_module(self.module_path)
        group = click.group()(getattr(imported_module, self.name, None))
        self._load_commands(group)
        return group


class TreeCommands:
    def __init__(self):
        # Initialize the TreeCommands class and load commands
        self.load_commands()
        self.root()

    @staticmethod
    @click.group()
    def root():
        # Define the root Click group
        pass

    def _is_valid_directory(self, item, folder_path):
        # Check if the item is a valid directory (not starting with "__")
        return not item.startswith("__") and os.path.isdir(
            os.path.join(folder_path, item)
        )

    def _is_valid_file(self, item, folder_path):
        # Check if the item is a valid file (not starting with "__")
        return not item.startswith("__") and os.path.isfile(
            os.path.join(folder_path, item)
        )

    def load_commands(self):
        # Load commands into the root Click group
        current_directory = os.getcwd()
        sys.path.append(current_directory)
        folder_path = os.path.join(current_directory, BASE_DIRECTORY)

        for item in os.listdir(folder_path):
            if self._is_valid_directory(item, folder_path):
                # Create a Group object and add it to the root group
                group = Group(item)
                self.root.add_command(group.module())

            if self._is_valid_file(item, folder_path):
                # Create a Command object and add it to the root group
                command = Command(item[:-3])
                self.root.add_command(command.module())

        sys.path.remove(current_directory)


if __name__ == "__main__":
    # Instantiate the TreeCommands class when the script is executed
    TreeCommands()
