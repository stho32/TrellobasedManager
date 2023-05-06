# Trello Task Manager

Trello Task Manager is a simple Python script that selects a random task from a specified Trello list and displays it for you. It can be run with a customizable work duration and break duration, playing a gong sound when a new task starts and a rooster crowing sound when the break starts. The tool is designed to help improve focus and productivity by providing a clear and randomized task to work on.

## Installation

To get started, first install the required dependencies:

```
pip install requests
pip install pygame
pip install pyttsx3
```

## Sound

### Gong Sound

This project uses a gong sound by Daniel Simon, licensed under CC BY 3.0. You can find the source and license details below:

- Gong sound by Daniel Simon is licensed under Attribution 3.0.
- Source: [https://soundbible.com/2148-Chinese-Gong.html](https://soundbible.com/2148-Chinese-Gong.html)
- License: [https://creativecommons.org/licenses/by/3.0/](https://creativecommons.org/licenses/by/3.0/)

### Rooster Sound

- Rooster Crowing sound by Mike Koenig is licensed under Attribution 3.0.
- Source: [https://soundbible.com/1134-Rooster-Crowing.html](https://soundbible.com/1134-Rooster-Crowing.html)
- License: [https://creativecommons.org/licenses/by/3.0/](https://creativecommons.org/licenses/by/3.0/)

## Usage

The main script is `main.py`. To run it, simply execute the following command in your terminal:

```
python main.py --work-duration MINUTES
```

Replace `MINUTES` with the desired work duration in minutes for each task.

To add a break after each task, use the `--break-duration` flag:

```
python main.py --work-duration MINUTES --break-duration MINUTES
```

Replace the second `MINUTES` with the desired break duration in minutes after each task.

In this mode, the script will continuously select a new task after the specified work duration, play the gong sound as an alarm, and then take a break for the specified break duration while playing a rooster crowing sound.

## Configuration

To configure the script to work with your Trello account, create a `config.json` file in the same directory as the `main.py` script with the following format:

```json
{
  "API_KEY": "your_trello_api_key",
  "TOKEN": "your_trello_token",
  "board_name": "your_board_name",
  "list_name": "your_list_name"
}
```

Replace the placeholders with your Trello API key, token, and the names of the board and list you want to use.

For information on how to obtain your Trello API key and token, refer to the [Trello API documentation](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/#authentication-and-authorization).

## Repository Structure

The repository is organized into the following files and directories:

- `main.py`: The main script that selects and displays tasks.
- `task_utils.py`: Contains functions related to selecting and displaying tasks.
- `trello_utils.py`: Contains functions for interacting with the Trello API.
- `sound_utils.py`: Contains the `play_mp3_async` function for playing MP3 files asynchronously.
- `Sounds`: A directory containing the gong sound file (`chinese-gong-daniel_simon.mp3`) and the rooster crowing sound file (`Rooster_Crowing-SoundBible.com-43612401.mp3`).

## Contributing

Feel free to submit issues or pull requests to improve the tool.