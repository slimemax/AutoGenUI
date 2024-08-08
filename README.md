# Claude Auto Script Generator

Claude Auto Script Generator is a Python application that uses the Anthropic Claude API to automatically generate and improve code based on user-defined prompts. It features a graphical user interface built with Tkinter, allowing users to easily interact with the Claude AI model.

## Features

- Custom first prompt and follow-up prompt inputs
- Adjustable maximum iteration count
- Real-time preview of generated code
- Automatic code saving for each iteration
- Sleek black and red interface design
- Supports multiple file types (html, py, js, css, txt)

## Requirements

- Python 3.6+
- anthropic
- tkinter (usually comes pre-installed with Python)

## Installation

1. Clone this repository:

    ```sh
    git clone https://github.com/slimemax/AutoGenUI/tree/main
    ```
2. Navigate to the project directory:

    ```sh
    cd AutoGenUI
    ```
3. Install the required packages:

    ```sh
    pip install anthropic
    ```

## Usage

1. Run the script:

    ```sh
    python autogen.py
    ```
2. Enter your desired prompts in the "First Prompt" and "Follow-up Prompt" text areas.
3. Set the maximum number of iterations.
4. Select the desired file type for the generated code.
5. Click "Start" to begin the code generation process.
6. The generated code will be saved in separate files for each iteration.

## Note

This application requires an Anthropic API key to function. Make sure to replace the placeholder API key in the script with your own before running.

## License

[MIT License](https://opensource.org/licenses/MIT)

## Disclaimer

This tool is for educational and experimental purposes only. Always review and test any generated code before using it in a production environment.

## Changelog

### V3 Autogen

- Added support for multiple file types (html, py, js, css, txt)
- Enhanced logging functionality
- Improved user interface and usability
- Optimized code generation process
- Included error handling for API calls and file saving

