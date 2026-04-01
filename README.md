# Evolution WhatsApp Bot

## Project Overview
This project is a WhatsApp automation bot utilizing the Evolution API and FastAPI. It aims to provide seamless interaction and automation of tasks through WhatsApp, enabling users to automate replies, send messages, and manage contacts efficiently.

## Architecture
The bot architecture is based on a microservices approach, utilizing FastAPI for building the web services. The Evolution API provides the underlying functionality to interact with WhatsApp, while the bot logic handles user requests and responses.

### Components
- **FastAPI**: Serves as the framework for building the API.
- **Evolution API**: Facilitates communication with WhatsApp.
- **Database**: (optional) For storing user interactions and logs.

## Features
- Automated responses based on user queries.
- Integration with the Evolution API for WhatsApp messaging.
- User-friendly setup and configuration.
- Support for handling media messages.
- Logging and error handling for improved reliability.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/sethnwoks/evolution-whatsapp-bot.git
   cd evolution-whatsapp-bot
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the environment variables as required by the Evolution API.

## Usage
- Start the FastAPI server:
  ```bash
  uvicorn main:app --reload
  ```
- Access the API documentation at `http://127.0.0.1:8000/docs`.
- Use the available API endpoints to interact with the WhatsApp bot.

## Deployment
This bot can be deployed on various platforms like Heroku, AWS, or any server that supports Python applications.
1. Create a requirements.txt if deploying on Heroku.
2. Ensure all environment variables are correctly set before deployment.

## Contributing
Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for more information on how to get involved.

## License
This project is licensed under the MIT License - see the LICENSE file for details.