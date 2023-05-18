Sure, here's the updated README.md content with information from the old README.

```markdown
# TrellobasedManager

TrellobasedManager is a Python application that helps to improve your productivity by interacting with your Trello board. The tool performs in two modes:

1. **Work mode**: The application randomly selects tasks from a specific Trello list for you to work on. Upon task completion, the task will be deleted from the Trello board. You can customize the duration of work on each task and the break time between tasks. When a new task starts, a gong sound will play, and when the break starts, you will hear a rooster crowing sound.

2. **Cleanup mode**: The application provides a way to manage your tasks across all lists on your Trello board. You can move tasks between lists, delete tasks, or stop the cleanup process at any time.

## Installation

To get started, first clone this repository and then install the required dependencies:

```bash
pip install -r requirements.txt
```

## Sound

### Gong Sound

This project uses a gong sound by Daniel Simon, licensed under CC BY 3.0:

- Gong sound by Daniel Simon is licensed under Attribution 3.0.
- Source: [Gong Sound](https://soundbible.com/2148-Chinese-Gong.html)
- License: [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/)

### Rooster Sound

- Rooster Crowing sound by Mike Koenig is licensed under Attribution 3.0.
- Source: [Rooster Crowing Sound](https://soundbible.com/1134-Rooster-Crowing.html)
- License: [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/)

## Usage

Firstly, you need to set up your Trello API Key and Token in a `config.json` file in the root directory of the application:

```json
{
    "API_KEY": "your_trello_api_key",
    "TOKEN": "your_trello_api_token",
    "board_name": "your_trello_board_name",
    "list_name": "your_trello_list_name_for_work_mode"
}
```

To start the application in work mode, use the following command:

```bash
python main.py --perform --work-duration <work_minutes> --break-duration <break_minutes>
```

To start the application in cleanup mode, use the following command:

```bash
python main.py --cleanup
```

## Repository Structure

The repository consists of the following files and directories:

- `main.py`: The main script to start the application.
- `performing_tasks.py`: Contains functions related to working with tasks.
- `trello_utils.py`: Contains functions for interacting with the Trello API.
- `output_utils.py`: Contains functions for clearing the console and printing and speaking text.
- `Sounds`: A directory containing the gong sound file (`chinese-gong-daniel_simon.mp3`) and the rooster crowing sound file (`Rooster_Crowing-SoundBible.com-43612401.mp3`).

## Contributing

Feel free to submit issues or pull requests to improve this tool.

## License

This project is licensed under the terms of the MIT license.
```

Remember to replace placeholders in the "Usage" section with actual values.