# gothbot
_this bot sucks do not add it to your server_

### Introduction
Gothbot is a discord bot written for a community discord server I am apart of. It is entirely written as a joke and some
of the src may be offensive to some (or all) people. Its written as 50% of a reason to fuck around with my friends and
code a project, if they ever commit anything, and 50% to utilise my very under utilised home server. There are no plans
for any features outside of whats in issues and theres no timeline for any features or fixes.

### Contributing
Fork this repo, make a pull request, assuming your code isn't ass, adds something to the bot, and passes both the black
formatter and existing unittests, I'll merge it in.

### Deploying
Unfortuately this thing is on (docker hub)[https://hub.docker.com/r/tomnieuwland/gothbot]. I highly suggest deploying
it using docker-compose. Your `docker-compose.yml` should have something like this in it

```dockerfile
gothbot:
    container_name: gothbot
    image: tomnieuwland/gothbot
    env_file:
     - ../.env
    restart: unless-stopped
```

You will need to supply it some environment variables to get this bad boy running. The bare minimum you need is your (own
discord bot token)[https://discord.com/developers/applications] (mostly because I don't know how to shard bots or do 
anything fancy yet, so you have to run a copy of this thing for yourself)

You can find all enviroment variables in `.env.template`. If you really wanna know what each of them does, go read the
src.

### Developing
You can run this either by using run.py or by running the included dockerfile. For run.py you can use environment
variables given at runtime, or a `.env` file located at the repo root. For docker, you will need to use a `.env` file
located at root.

This repo uses `black` for formatting and `pylint` for unit testing. Please add unittests if you contribute or I just
won't add your code :)

As far as actually developing, I highly suggest you make a bot token, and use it to run a "test" bot, which is added
only to a server suitable for testing. I personally use two tokens, one for production deployment and one for testing.
To add YOUR bot to YOUR server, use the following link 
`https://discord.com/oauth2/authorize?client_id=<INSERT YOUR ID HERE>&scope=bot` where you add your own generated client
id from the discord developer dashboard

If you have multiple instances of the bot running, all instances will respond to any incoming queries.

