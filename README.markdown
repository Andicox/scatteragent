# ScatterAgent Discord Bot

A feature-rich Discord bot for game and development community servers, built with nextcord.

## Features
- **War Scatter Integration**: Game status updates, leaderboard, /register, /ticket
- **Moderation**: Auto-moderation, /kick, /ban, /timeout, /warn, /clear
- **Community**: /verify, /suggest, /poll, welcome/farewell system
- **Admin Tools**: /announce, /pingopt, custom command creation, reaction roles
- **Optional AI**: /ask command (not implemented in this version)

## Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd scatteragent
   ```

2. **Install Dependencies**
   ```bash
   pip install nextcord python-dotenv
   ```

3. **Create a `.env` File**
   ```env
   DISCORD_TOKEN=your_bot_token
   GUILD_ID=your_server_id
   SUPPORT_CHANNEL_ID=support_channel_id
   MOD_LOG_CHANNEL_ID=mod_log_channel_id
   VERIFIED_ROLE_ID=verified_role_id
   SUGGESTIONS_CHANNEL_ID=suggestions_channel_id
   WELCOME_CHANNEL_ID=welcome_channel_id
   DEFAULT_ROLE_ID=default_role_id
   ANNOUNCEMENT_CHANNEL_ID=announcement_channel_id
   ```

4. **Create Directory Structure**
   ```
   scatteragent/
   ├── cogs/
   │   ├── game.py
   │   ├── moderation.py
   │   ├── community.py
   │   ├── admin.py
   ├── main.py
   ├── scatteragent.db
   ├── .env
   ```

5. **Run the Bot**
   ```bash
   python main.py
   ```

## Notes
- Ensure your bot has the necessary permissions (Manage Roles, Kick/Ban Members, etc.).
- The bot uses SQLite for data storage. The database is automatically created on first run.
- The /ask command (AI integration) is not implemented in this version but can be added using an OpenAI API key.
- Cooldowns can be added using `@commands.cooldown` decorator as needed.