# ApolloBot
A Discord bot written in Python. Currently supports monitoring subreddits and posting new posts to configured channels.

## Features
- Discord and Reddit integration
- Environment-based configuration
- Modular command system
- Logging system for monitoring and debugging

## Prerequisites
- Python 3.x
- Discord account and bot token
- Reddit API credentials

## Installation
### Local Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/ApolloBot.git
cd ApolloBot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following variables:
```env
DISCORD_PREFIX=your_preferred_prefix
DISCORD_TOKEN=your_discord_bot_token
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
```

## Configuration
The bot uses environment variables for configuration, which can be set in the `.env` file:

- `DISCORD_PREFIX`: Command prefix for the bot
- `DISCORD_TOKEN`: Your Discord bot token
- `REDDIT_CLIENT_ID`: Reddit API client ID
- `REDDIT_CLIENT_SECRET`: Reddit API client secret

The bot uses a dedicated channel named `apollo-config` for configuration purposes.

## Project Structure
```
ApolloBot/
├── bot/                # Core bot functionality
├── commands/          # Command implementations
├── utils/            # Utility functions and helpers
├── main.py           # Entry point of the application
├── settings.py       # Configuration settings
└── requirements.txt  # Project dependencies
```

## Usage

The bot provides the following commands for managing Reddit subscriptions:

```
!reddit subscribe <subreddit> [filters]  - Subscribe to a subreddit with optional filters
                                          Example: !reddit subscribe bapcsales "gpu,cpu"
!reddit unsubscribe                      - Unsubscribe the current channel from Reddit updates
!reddit list                             - List Reddit subscriptions for this channel
```

Replace `!` with your configured prefix in the `.env` file.

### Configuration
The bot automatically creates a private `apollo-config` channel in your server for storing configuration. Only users with the "Manage Channels" permission can use the Reddit commands.

### Example Usage
1. Subscribe to a subreddit:
   ```
   !reddit subscribe buildapcsales
   ```

2. Subscribe with filters (only show posts containing these keywords):
   ```
   !reddit subscribe buildapcsales "gpu,rtx,3080"
   ```

3. View current subscriptions:
   ```
   !reddit list
   ```

> [!NOTE]
> Only posts newer than when the last time the bot checked for new posts will be processed. This is to prevent the bot from processing duplicate, existing posts.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Support
If you encounter any issues or have questions, please open an issue in the GitHub repository.
