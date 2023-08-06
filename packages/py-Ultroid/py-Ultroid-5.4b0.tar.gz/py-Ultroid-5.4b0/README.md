# py-Ultroid Library
A stable userbot base library, based on Telethon.

## Installation:-
`pip install py-Ultroid`

## Usage:-
=> Create folders named plugins, addons, assistant, resources.<br/>
=> Add your plugins in plugins folder and accordingly.<br/>
=> Create .env file with `API_ID`, `API_HASH`, `SESSION`, 
`BOT_TOKEN`, `BOT_USERNAME`, `REDIS_URI`, `REDIS_PASSWORD` & 
`LOG_CHANNEL` as mandatory environment variables check
[.env.sample](https://github.com/TeamUltroid/Ultroid/.env.sample).<br/>
=> Then run `python -m pyUltroid`<br/>

### Creating plugins:-
`@ultroid_cmd(pattern="start$")`<br/>
`async def _(e):`<br/>
ㅤㅤㅤㅤ	`await e.reply("Ultroid Started")`<br/>


Made with 💕 by [@TeamUltroid](https://t.me/TeamUltroid). <br />

# Credits
* [Lonami](https://github.com/LonamiWebs/) for [Telethon](https://github.com/LonamiWebs/Telethon)

