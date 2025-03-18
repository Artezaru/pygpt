Usage
==============

This guide provides step-by-step instructions on how to use the `pygpt` tool for managing discussions with OpenAI's GPT models.

Getting Started
---------------

1. **Install the package**:  
Make sure the `pygpt` package is installed and properly configured.

2. **Set your OpenAI API key**:  
Export your API key as an environment variable:

.. code-block:: console

    export OPENAI_API_KEY=your-api-key

3. **Run the interface**:  
Start the `pygpt` terminal interface by running the following command:

.. code-block:: console

    pygpt

4. **Interact with the tool**:  
Use the commands listed in :doc:`commands` to interact with the GPT discussions.

Basic Workflow
--------------

1. **Create a new discussion**:  
To start a new discussion, use the `!new` command:

.. code-block:: console

    >>> !new MyFirstDiscussion

2. **Add messages to the discussion**:  
Simply type your messages to send them to the GPT model:

.. code-block:: console

    >>> Hello, GPT! Can you help me with a Python question?
    GPT: Sure! What's your question?

3. **Copy the last assistant response**:  
To quickly copy the last response, use the `!copy` command:

.. code-block:: console

    >>> !copy
    Last assistant response copied to clipboard.

4. **Search the discussion history**:  
To find specific content, use the `!search` command:

.. code-block:: console

    >>> !search Python
    GPT: Sure! What's your Python question?

5. **Set a system message**:  
To configure the system message for context, use `!system`:

.. code-block:: console

    >>> !system You are an expert Python assistant.

6. **Manage discussions**:  
List and open discussions with `!open`:

.. code-block:: console

    >>> !open

Close the current discussion with `!close`:

.. code-block:: console

    >>> !close

7. **Delete discussions**:  
Delete the current discussion:

.. code-block:: console

    >>> !delete

Delete all discussions:

.. code-block:: console

    >>> !delete_all

Advanced Options
----------------

1. **Set token limits**:  
Use `!token_limit` to define the maximum token limit for a discussion:

.. code-block:: console

    >>> !token_limit 2048

2. **Change GPT models**:  
Switch between GPT models with the `!model` command:

.. code-block:: console

    >>> !model gpt-4

Help and Documentation
-----------------------

Use `!help` or `!?` to display the list of commands:

.. code-block:: console

    >>> !help

Refer to :doc:`./commands` for a detailed description of each command.

For more information about the API, refer to the :doc:`./api` documentation.