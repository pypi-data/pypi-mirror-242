## Chat with GPT in Terminal

[![English badge](https://img.shields.io/badge/%E8%8B%B1%E6%96%87-English-blue)](https://github.com/xiaoxx970/chatgpt-in-terminal/blob/main/README.md)
[![简体中文 badge](https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-Simplified%20Chinese-blue)](https://github.com/xiaoxx970/chatgpt-in-terminal/blob/main/README.zh-CN.md)
[![Platform badge](https://img.shields.io/badge/Platform-MacOS%7CWindows%7CLinux-green)]()
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg)](https://github.com/RichardLitt/standard-readme)

This project enables chatting with ChatGPT in the terminal.

Markdown content in answers is rendered as beautifully formatted rich text.

Supports history retrieval with the up arrow key, optional multi-line questions, and tokens counting.

Slash (/) commands are available in the chat box to toggle multi-line submit mode, undo the last question and answer, modify the system prompt and more, see the available commands below for details.

Supports saving chat messages to a JSON file and loading them from the file.

![example](https://github.com/xiaoxx970/chatgpt-in-terminal/raw/main/README.assets/small.gif)

Uses the [gpt-3.5-turbo](https://platform.openai.com/docs/guides/chat/chat-completions-beta) model, which is the same model used by ChatGPT (Free Edition), as default.

### Related Projects

[GPTerm implemented in C/C++](https://github.com/Ace-Radom/cGPTerm) by @Ace-Radom

[gpt-term that can call POE API](https://github.com/Lemon-2333/chatgpt-in-terminal-Poe-Api) by @Lemon-2333

## Changelog

### 2023-11-17

- Added the feature of setting the default model. Now you can use `gpt-term --set-model MODEL_NAME` to set the default model. This setting will be written into the configuration file and will take effect every time it is started.

- Added new model candidates: `gpt-4-1106-preview`, `gpt-4-vision-preview`, `gpt-3.5-turbo-1106`.

### 2023-06-21

- Added direct query mode, now you can run `gpt-term` with the content of the question as a parameter to conduct a single question and answer

  ```sh
  gpt-term "What's the weather like today?"
  ```

  The answer will be printed directly, or piped into a variable

  ```sh
  gpt-term "What's the weather like today" | read answer
  echo $answer
  ```

<details>
  <summary>More Change log</summary>

### 2023-05-20

- Added host configuration support, which is very useful when using self-built API reverse proxy server ([#49](https://github.com/xiaoxx970/chatgpt-in-terminal/issues/49)), you can now use `gpt-term --set-host HOST` to configure host, the default is https://api.openai.com

### 2023-05-18

- Added multi-language support: English, Chinese, Japanese, German, follow the system language by default, now you can use `/lang` to switch languages
### 2023-05-11

- Find the command the user most likely intended to enter when typing an unrecognized command

### 2023-05-05

- Add `/rand` command to set temperature parameter

- Add overflow mode switch for `/stream` command, now you can run command `/stream visible` to switch to always visible mode. In this mode, the content that exceeds the screen will be scrolled up, and the new content will be output until it is completed

### 2023-04-23

Released `gpt-term` on [Pypi](https://pypi.org/project/gpt-term/), started version control. No need to clone the project locally anymore, simply use the `pip` command to install gpt-term.

### 2023-04-15

- Added the ability to create a line break in single-line mode using `Esc` + `Enter`

### 2023-04-13

- Added the function of generating and setting the terminal title in the background, and now the client will use the summary of the first question content as the terminal title

### 2023-04-09

- Add filename generate function, client will suggest the summary of the first question as filename when save command executed.

### 2023-04-05

- Add `/delete` command to delete the first question and answer in this chat to reduce token.

### 2023-04-01

- Add `/copy` command to copy the last reply's content to the clipboard
- Add streaming output mode, enabled by default, use `/stream` to switch

### 2023-03-28

- Add `--model` runtime argument and `/model` command to choose / change AI models.

### 2023-03-27

- Added `--key` runtime argument to select which API key in the `.env` file to use.

### 2023-03-23

- Added slash (/) command functionality
- Added `--load` runtime argument to load previously saved chat history
- Modified program structure and interaction methods, changing the original `input()` function to the `prompt_toolkit` library's input interface, supporting multi-line input, command-line completion, and other features.
- Improved error handling mechanisms, added chat history backup, logging, and other features, enhancing the program's reliability and fault tolerance.
- Refactored code logic and function structure, improving modularity and readability.

</details>

## Preparation

1. An OpenAI API key. You need to register an OpenAI account and obtain an API key.

   OpenAI's API key can be generated on the page opened by clicking "View API keys" in the upper right corner of the homepage, direct link: https://platform.openai.com/account/api-keys

   ![image-20230303233352970](https://github.com/xiaoxx970/chatgpt-in-terminal/raw/main/README.assets/image-20230303233352970.png)

2. [Python](https://www.python.org/downloads/) version 3.7 or higher.

   **Attention: Try not to use the Python that comes with the system (including Windows 11 app store version and MacOS pre-installed Python), otherwise the gpt-term command will not be found after installation ([#38](https://github.com/xiaoxx970/chatgpt-in-terminal/issues/38))**

## Installation


1. Install `GPT-Term` using `pip`

   ```shell
   pip3 install gpt-term
   ```

2. Configure the API Key

   ```shell
   gpt-term --set-apikey YOUR_API_KEY
   ```

   > If you don't configure the API Key now, you can enter it when prompted during runtime.

## Update

To update `GPT-Term` to the latest version, run the following command in your terminal:

```sh
pip3 install --upgrade gpt-term
```

> If there is a new version, `GPT-Term` will prompt the user to update upon exiting.

## How to Use

Run with the following command:

```shell
gpt-term
```

Or:

```shell
python3 -m gpt_term
```

Quick query:

```sh
gpt-term "What's the weather like today?"
```

When entering a question in single-line mode, use `Esc` + `Enter` to start a new line, and use `Enter` to submit the question.

Here are some common shortcut keys (also shortcut keys for the shell):

- `Ctrl+_`:	Undo
- `Ctrl+L`: Clear screen, equivalent to `clear` command in shell
- `Ctrl+C`: Stop the current answer or cancel the current input
- `Tab`: Autocomplete commands or parameters
- `Ctrl+U`: Delete all characters to the left of the cursor
- `Ctrl+K`: Delete all characters to the right of the cursor
- `Ctrl+W`: Delete the word to the left of the cursor

> Original chat logs will be saved to `~/.gpt-term/chat.log`

### Available Arguments

| Arguments | Description | Examples |
| ------------- | --------------------------------- | ------------------------------------------------ |
| -h, --help | show this help message and exit | `gpt-term --help` |
| --load FILE | Load chat history from file | `gpt-term --load chat_history_code_check.json` |
| --key API_KEY | Select the API key to use in the config.ini file | `gpt-term --key OPENAI_API_KEY1` |
| --model MODEL | Select AI model to use | `gpt-term --model gpt-3.5-turbo` |
| --host HOST | Set the API Host address used in this run (this is usually used to configure proxy) | `gpt-term --host https://closeai.deno.dev` |
| -m, --multi | Enable multiline mode | `gpt-term --multi` |
| -r, --raw | Enable raw mode | `gpt-term --raw` |
| -l, --lang LANG | Set the current running language: en, zh_CN, jp, de | `gpt-term --lang en` |
| --set-model HOST | Set the AI model to use | `gpt-term --set-model gpt-4-1106-preview` |
| --set-host HOST | Set API Host address (this is usually used to configure proxy) | `gpt-term --set-host https://closeai.deno.dev` |
| --set-apikey KEY | Set OpenAI API key | `gpt-term --set-apikey sk-xxx` |
| --set-timeout SEC | Set the maximum wait time for API requests | `gpt-term --set-timeout 10` |
| --set-gentitle BOOL | Set whether to auto-generate title for chat | `gpt-term --set-gentitle True` |
| --set-saveperfix PERFIX | Set the save prefix for chat history files | `gpt-term --set-saveperfix chat_history_` |
| --set-loglevel LEVEL | Set log level: DEBUG, INFO, WARNING, ERROR, CRITICAL | `gpt-term --set-loglevel DEBUG` |
| --set-lang LANG | Set language: en, zh_CN, jp, de | `gpt-term --set-lang en` |

> Multi-line mode and raw mode can be used simultaneously

### Configuration File

The configuration file is located at `~/.gpt-term/config.ini` and is autogenerated. It can be modified using the program's `--set` option or edited manually.

The default configuration is as follows:

```ini config.ini
[DEFAULT]
# API key for OpenAI
OPENAI_API_KEY=

# The maximum waiting time for API requests, the default is 30s
OPENAI_API_TIMEOUT=30

# Whether to automatically generate titles for conversations, enabled by default (generating titles will consume a small amount of tokens)
AUTO_GENERATE_TITLE=True

# Define the default file prefix when the /save command saves the chat history. The default value is "./chat_history_", which means that the chat history will be saved in the file starting with "chat_history_" in the current directory
# At the same time, the prefix can also be specified as a directory + / to allow the program to save the chat history in a folder (note that the corresponding folder needs to be created in advance), for example: CHAT_SAVE_PERFIX=chat_history/
CHAT_SAVE_PERFIX=./chat_history_

# Log level, default is INFO, available value: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO

# Set the language of the program, the default is empty, it will follow the system language
LANGUAGE=

# 设置api的host，默认为https://api.openai.com
OPENAI_HOST=

# 设置使用的模型，默认为gpt-3.5-turbo
# 可用模型: https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo, https://platform.openai.com/docs/models/gpt-3-5
OPENAI_MODEL=
```

### Available Commands

- `/raw`: Display raw text in replies instead of rendered Markdown format

  > After switching, use the `/last` command to reprint the last reply

- `/multi`: Enable or disable multi-line mode, allowing users to enter multi-line text

  > In multi-line mode, use `Esc` + `Enter` to submit the question
  >
  > If pasting multi line text, single-line mode can also paste properly

- `/stream`: disable or enable stream mode

   > In stream mode, the answer will start outputting as soon as the first response arrives, which can reducing waiting time. Stream mode is on by default.

   - `/stream ellipsis` (default)

     > Switch the mode of streaming output to auto omission, when the output content exceeds the screen, three small dots will be displayed at the bottom of the screen and wait until the output is completed

   - `/stream visible`

      > Toggle the streaming output mode to always visible, in this mode, the content that exceeds the screen will be scrolled up, and the new content will be output until it is completed. Note that in this mode the terminal will not properly clean up off-screen content.

- `/tokens`: Display the total tokens spent and the tokens for the current conversation

  > GPT-3.5 has a token limit of 4096; use this command to check if you're approaching the limit

- `/usage`: Display the API credits summary

  > This feature may not be stable. If it fails to operate, you can visit the [usage page](https://platform.openai.com/account/usage) to view further information.

- `/model`: Show or change the Model in use

  > `gpt-4` , `gpt-4-32k` , `gpt-3.5-turbo` are supported by default. when using other models you need to change the API endpoint in code.

- `/last`: Show the last reply

- `/copy` or `/copy all`: Copy the last reply's content to the clipboard

  - `/copy code [index]`: Copy the `index`-th code block from the last reply's content to the clipboard

    > If `index` is not specified, the terminal will print all code blocks and ask for the number of the one to be copied

- `/delete` or `/delete first`: delete the first question and answer in the current chat

     > When the token is about to reach the upper limit, the user will be warned, and when the upper limit has been exceeded, it will be asked whether to delete the first message

   - `/delete all`: delete all messages

- `/save [filename_or_path]`: Save the chat history to the specified JSON file

  > If no filename or path is provided, the client will generate one, and if generation fails, the filename `chat_history_YEAR-MONTH-DAY_HOUR,MINUTE,SECOND.json` is suggested on input.

- `/system [new_prompt]`: Modify the system prompt

- `/rand [randomness]`: Set Model sampling temperature (0~2), higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.

- `/title [new_title]`: Set terminal title for this chat

  > If new_title is not provided, a new title will be generated based on first question

- `/timeout [new_timeout]`: Modify API timeout.

  > The default timeout is 30 seconds, it can also be configured by setting `OPENAI_API_TIMEOUT=` in the `~/.gpt-term/config.ini` file.
  
- `/undo`: Delete the previous question and answer

- `/version`: Display the local and remote versions of `GPT-Term`

- `/help`: Display available commands

- `/exit`: Exit the application

### Exit Words

In the chat, use exit words to end the current session. Exit words include:

```python
['再见', 'bye', 'goodbye', '结束', 'end', '退出', 'exit', 'quit']
```

Exit words will be sent as a question to ChatGPT, and the application will exit after GPT replies.

You can also use `Ctrl-D` or `/exit` to exit immediately.

Upon exit, the token count for the chat session will be displayed.

> Current price: $0.002 / 1K tokens, Free Edition rate limit: 20 requests / min (`gpt-3.5-turbo`)

## Dependencies

Thanks to the following projects for providing strong support for this script:

- [requests](https://github.com/psf/requests): For handling HTTP requests
- [pyperclip](https://github.com/asweigart/pyperclip): A cross-platform clipboard operation library
- [rich](https://github.com/willmcgugan/rich): For outputting rich text in the terminal
- [prompt_toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit): Command-line input processing library
- [sseclient-py](https://github.com/mpetazzoni/sseclient): For implementing streaming output of answers
- [tiktoken](https://github.com/OpenAI/tiktoken): A library for calculating and processing OpenAI API tokens

## Contributing

Feel free to dive in! [Open an issue](https://github.com/xiaoxx970/chatgpt-in-terminal/issues/new) or submit PRs.

### Contributors

This project exists thanks to all the people who contribute. 
<a href="https://github.com/xiaoxx970/chatgpt-in-terminal/graphs/contributors"><img src="https://opencollective.com/chatgpt-in-terminal/contributors.svg?width=890&button=false" /></a>

## Project Structure

```sh
.
├── LICENSE                   # License
├── README.md                 # Documentation
├── chat.py                   # Script entry point
├── gpt_term                  # Project package folder
│   ├── __init__.py
│   ├── config.ini            # API key storage and other settings
│   └── main.py               # Main program
├── requirements.txt          # List of dependencies
└── setup.py
```

## License

This project is licensed under the [MIT License](LICENSE).
