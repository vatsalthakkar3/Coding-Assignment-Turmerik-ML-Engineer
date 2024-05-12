# Turmerik ML Home Assignment

This project aims to showcase proficiency in ethical web scraping, data analysis with sentiment analysis, and the integration of AI for personalized communication. This readme provides guidelines for setting up and running the code, a brief discussion of the methodology, examples of collected data, and an overall data analysis along with generated personalized messages.

## Author

- Vatsal Thakkar (<vatsalthakkar3.vt@gmail.com>)

## Requirements

### Hard Requirements

1. Python (v3.11)
2. Reddit Account

### Soft Requirements

1. Miniconda
2. VS Code (code editor)
3. SQLite (Extension for VSCode)
4. SQLite Viewer (Extension for VSCode)

## Setup Steps

### Install Python Dependencies

If you prefer to use Miniconda for managing Python environments, follow all the steps (1-5) outlined. However, if you opt not to use Miniconda, make sure you have Python version 3.11 installed, and you can skip steps 1-4, proceeding directly to step 5. I recommend using Miniconda for smoother Python environment management.

1. **Download Miniconda**: Visit the [Miniconda website](https://docs.conda.io/en/latest/miniconda.html) and download the appropriate installer for your OS.

2. **Install Miniconda**: Follow the installation instructions provided on the Miniconda website after downloading the installer.

3. **Set up Conda Environment**:
    ```bash
    conda create --name turmerik_ml python=3.11
    ```

4. **Activate the Environment**:
    ```bash
    conda activate turmerik_ml
    ```

5. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    This command installs all necessary packages listed in `requirements.txt` into your Python environment.

### Setting up the Environment Variables

To setup the environment variables for your application I prefer using the `.env` configuration file to store all the environment variable and keep the environment variables in the same place and private 

1. **Create a `.env` File**: Start by creating a file named `.env` in the root directory of your application.

    ```bash
    touch .env
    ```

2. **Define Environment Variables**: Inside the `.env` file, define your environment variables using the KEY=VALUE format. I have provide the `.env.example` file containing the example variables you want to define. You can just copy and paste the example variables and set your environment variables.

    ```bash
       # REDDIT API
       REDDIT_SECRET_KEY="" # Write Your Reddit Secret Key in quotes
       REDDIT_CLIENT_ID=""  # Write Your Reddit Client ID in quotes
       USER_AGENT=""        # Write Your Reddit User Agent in quotes
       REDDIT_USERNAME=""   # Write Your Reddit Username in quotes (Not Required)
       REDDIT_PASSWORD=""   # Write Your Reddit Password in quotes (Not Required)

       # OPENAI_API_KEY
       OPENAI_API_KEY="" # Write Your OpenAI API Key in quotes
    ```
### Running the code 

All the code is 
