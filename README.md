# twitch-plays-switch
A python script to let twitch chat control your Nintendo Switch.
And yes, I know the code is terrible.
**Only works on Linux.**


# Instructions
Install the dependencies:
Run the following:
    sudo pip3 install -r requirements.txt
Create a file named ``secretsio.py``
In it put the following:

    TMI_TOKEN="oauth:your bot token"
    CHANNEL="your twitch channel"
    BOT_NICK"your bots name
The bot account cannot be the same as the streamer.
Then, mod the bot on your channel
On the switch, go to change grip/order
Then, run the following in a terminal in the same folder as the script:

    sudo python3 ./cli.py PRO_CONTROLLER
  The controller should connect and the !twitchplays command should work.
  You can add ``-r the switch's mac address`` to avoid having to go to change grip/order in the future.

