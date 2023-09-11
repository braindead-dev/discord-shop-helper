# Discord Product Store Bot

## Introduction

This bot was designed to assist digital product store owners on Discord with basic tasks such as displaying store information and facilitating custom giveaway events with a captcha feature. 

## Features

1. **Store Information Command**: Quickly display essential store links with the `$shop` command.
2. **Support Command**: Get support links using the `$support` command.
3. **Custom Giveaway Command**: Host custom giveaways with captcha verification. This feature is exclusively accessible by users with the "Giveaway Host" role.
4. **Giveaway Reroll**: Reroll a specified giveaway and select a new winner.

## Command Details

- `$help`: Displays all the commands and their details.
- `$shop`: Shows the main shop link.
- `$support`: Provides the support chat link.
- `$giveaway`: Initiates a new giveaway event (Accessible only by "Giveaway Host" role).
- `$reroll '#channel_name' 'message_id'`: Rerolls a giveaway to select a new winner. Specify the channel name and message ID where the giveaway was held (Accessible only by "Giveaway Host" role).

## Setup

1. **Configuration**:
    - Set your bot's token in the `main.py` file.
    - Configure your shop's link and support chat link in the `main.py` file.

2. **Running the Bot**:
    - Execute `main.py` to run the bot.
    - Ensure you have all the necessary modules installed, as indicated in the `main.py` imports section.

3. **Assigning Roles**:
    - Assign the "Giveaway Host" role to users who should have permission to initiate and reroll giveaways.

## Dependencies

- `discord.py`: A modern, easy-to-use, feature-rich library to make Discord bots with Python.
- `asyncio`: For asynchronous operations.
- `datetime`: For date and time operations.
- `captcha`: For generating captcha images.

## Note

This was a bot I made a long time ago for a commission, mainly for the function of a giveaway command that supported captchas. Now that the original comissioner is out of business and has given me publishing permissions, here it is. With this being said, I don't remember how well this bot even worked and how long ago I made it, so it might be outdated and buggy. Use it at your own risk and ensure you test thoroughly before deploying in a production environment. I am no longer maintaining this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
