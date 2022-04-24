# Omnia - **THE** Discord bot.

## This README.md will show you how to setup and use this bot.

&nbsp;

### Setting up your environment

Setting up your environment is simple. Just `git clone` the repository!

```sh
git clone https://github.com/szskill/omnia
```

### Configuring the bot

To configure the bot, all you have to do is to modify `config.yaml`. The options
should be self-explainable.

Then, you also have to create a file named `.env`, then place your token like
this:

```
TOKEN=InsertTokenHere
```

Of course, replace `InsertTokenHere` with your bot token.

### Running the bot

From the root folder (the folder where config.yaml is stored), run this in the
terminal:

```sh
pip install -r requirements.txt
python -m omnia
```

or for Windows users:

```sh
py -m pip install -r requirements.txt
py -m omnia
```

...and wait for it to start. That's it! You're done.
