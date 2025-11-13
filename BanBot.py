#author: striving
#don't steal my code please
import asyncio
import discord
from discord import app_commands
import aiohttp

#use env variables 
token = ""
api_url = "http://"#your api url, something like "http://127.0.0.1:8000". i reccomend using aws for the bot and api
api_key = ""
#openssl rand -hex 32 to generate a api key

#ids of people that are mod
AUTHORIZED_USERS = [
    925935655257800714  #strvng
]

class client(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.session = None
    
    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        await self.tree.sync()
    
    async def close(self):
        if self.session:
            await self.session.close()
        await super().close()


intents = discord.Intents.default()
bot = client(intents=intents)


@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")


@bot.tree.command(name="ban", description="ban a roblox user by id")
@app_commands.describe(
    roblox_id="The Roblox user ID to ban",
    reason="The reason to give when the player joins the game"
)
async def ban(interaction: discord.Interaction, roblox_id: str, reason: str = "No reason provided"):
    #check if the user is authorized
    #probably a better way to do this is to restrict command usage to a specific role
    if interaction.user.id not in AUTHORIZED_USERS:
        await interaction.response.send_message("you are not authorized to use this command.", ephemeral=True)
        return
    
    await interaction.response.defer()
    
    data = {
        "robloxid": roblox_id,
        "moderatordiscordid": str(interaction.user.id),
        "reason": reason
    }
    headers = {"x-api-key": api_key} if api_key else {}
    
    try:
        async with bot.session.post(
            api_url.rstrip("/") + "/ban", 
            json=data, 
            headers=headers, 
            timeout=10
        ) as r:
            if r.status == 200:
                await interaction.followup.send(
                    f"**user banned**\nroblox id: {roblox_id}\nreason: {reason}\nmoderator: {interaction.user.mention}"
                )
            else:
                await interaction.followup.send("failed to ban user.")
    except Exception as e:
        await interaction.followup.send(f"something went wrong: {str(e)}")


@bot.tree.command(name="unban", description="unban a roblox user by id")
async def unban(interaction: discord.Interaction, roblox_id: str):
    if interaction.user.id not in AUTHORIZED_USERS:
        await interaction.response.send_message("you are not authorized to use this command.", ephemeral=True)
        return
    
    await interaction.response.defer(ephemeral=True)
    
    data = {
        "robloxid": roblox_id,
        "moderatordiscordid": str(interaction.user.id),
        "reason": ""
    }
    headers = {"x-api-key": api_key} if api_key else {}
    
    try:
        async with bot.session.post(
            api_url.rstrip("/") + "/unban", 
            json=data, 
            headers=headers, 
            timeout=10
        ) as r:
            result = await r.json()
            if r.status == 200:
                if result.get("status") == "ok":
                    await interaction.followup.send(f"unbanned {roblox_id}.")
                else:
                    await interaction.followup.send(f"user {roblox_id} was not banned.")
            else:
                await interaction.followup.send("failed to unban user.")
    except Exception as e:
        await interaction.followup.send(f"something went wrong: {str(e)}")





if __name__ == "__main__":
    bot.run(token)
