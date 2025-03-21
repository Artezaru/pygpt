# pygpt

## Description

`pygpt` is a Python package for managing and interacting with discussions powered by OpenAI's GPT models. It provides a user-friendly interface and tools to handle conversations efficiently.

Export your API key as an environment variable:

```
export OPENAI_API_KEY=your-api-key
```

Then run the command:

```
pygpt
```

And the interface will be open.


```console
>>> !new MyFirstDiscussion
========================================================================================
Opened discussion: MyFirstDiscussion
========================================================================================
>>> Say Hello World
GPT: Hello World!
>>> !copy  
Last assistant response copied to clipboard.
>>> !close
Discussion closed successfully.
>>> !open
                               Available Discussions                               
┏━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Code       ┃ Title             ┃ Created date        ┃ Last modified date  ┃
┡━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ 1  │ S8TX8DSTXF │ MyFirstDiscussion │ 2025-01-28 16:32:09 │ 2025-01-28 16:32:48 │
│ 2  │ YBOHNRKQ9L │ pandas python     │ 2025-01-28 15:51:07 │ 2025-01-28 16:21:39 │
│ 3  │ TJC1UKVOGT │ Test              │ 2025-01-28 15:45:19 │ 2025-01-28 15:58:16 │
└────┴────────────┴───────────────────┴─────────────────────┴─────────────────────┘
Enter the ID of the discussion to open or 0 to cancel: 2
====================================================================================
Opened discussion: pandas python
====================================================================================
>>> what are we talking about ? 
GPT: We are discussing how to create a Python class to manage (such as resize, rotate and save) images using the Python 
imaging library, Pillow.
>>> 
```

Run the help command to display all the commands.

```
!help
```


## Authors

- Artezaru <artezaru.github@proton.me>

- **Git Plateform**: https://github.com/Artezaru/pygpt.git
- **Online Documentation**: https://Artezaru.github.io/pygpt

## Installation

Install with pip

```
pip install git+https://github.com/Artezaru/pygpt.git
```

Clone with git

```
git clone https://github.com/Artezaru/pygpt.git
```

## License

See LICENSE
