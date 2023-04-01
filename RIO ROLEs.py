import requests
import discord
from discord.ext import commands

# Initialize the bot client
bot = commands.Bot(command_prefix="!")

# Define the API endpoints
USER_API_ENDPOINT = "https://use1-common-restapi.prod.recurforever.com/platform/customers/profiles/public/"
NFT_API_ENDPOINT = "https://use1-common-restapi.prod.recurforever.com/platform/nfts/"

# Define the emoji ID to add to the nickname
EMOJI_ID = 1234567890

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


@bot.command()
async def check(ctx, *, name: str):
    # Send a message to let the user know we're searching for their account
    await ctx.send(f"Searching for account with name: {name}")

    # Get the user's ID using the username
    user_response = requests.get(USER_API_ENDPOINT + name)
    print(user_response.url)

    if user_response.status_code == 200 and user_response.json().get("result"):
        user_id = user_response.json()["result"]["id"]

        # Get the list of NFTs owned by the user
        nft_names = {
            "APPLE": "Hello Kitty",
            "CHERRY": "Care Bears",
            "KIWI": "Star Trek",
            "PEAR": "Top Gun: Maverick",
            "ORANGE": "Nickelodeon",
            "PAPAYA": "NFTU",
            "MANGO": "Emoji Forever",
            "DRAGON": "Slotomania",
            "RECUR": "RECUR Pass"
        }

        for nft_name, display_name in nft_names.items():
            nft_url = f"{NFT_API_ENDPOINT}{nft_name}"
            nft_response = requests.get(nft_url, params={"filter": f"user_id=={user_id}"})
            #print(nft_response.url)

            # If the user owns the NFT, add the corresponding role and edit their nickname
            if nft_response.status_code == 200 and nft_response.json()["result"]['pagination']["totalItems"] > 0:
                role = discord.utils.get(ctx.guild.roles, name=f"{nft_name} Holder")
                #await ctx.author.add_roles(role)
                #await ctx.author.edit(nick=f"{ctx.author.display_name} {nft_name} Holder")
                total_items = nft_response.json()["result"]['pagination']["totalItems"]
                await ctx.send(f"Congratulations {ctx.author.name}, you own {total_items} NFTs and are a {display_name} holder!")
            else:
                await ctx.send(f"Sorry {ctx.author.name}, you do not own any {display_name} NFTs and are not a holder.")

        # Send the user's ID as a message
        #await ctx.send(f"{ctx.author.name}, your ID is: {user_id}")
    else:
        await ctx.send(f"Sorry {ctx.author.name}, we could not find an account with that name.")





bot.run("SECRET")
