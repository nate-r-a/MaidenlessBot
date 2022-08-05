from email import message
from gc import callbacks
from http.client import responses
from operator import xor
from urllib import response
import discord
from discord import Button, SelectOption
from discord.ui import Select
import os # default module
from dotenv import load_dotenv
# from discord_components import Button, Select, SelectOption, ComponentsBot

load_dotenv() # load all the variables from the env file
bot = discord.Bot(debug_guilds=[982370052915470336, 755579309921403000])

templates1 = [
    "**** ahead",
    "No **** ahead",
    "**** required ahead",
    "Be wary of ****",
    "Try ****",
    "Likely ****",
    "First off, ****",
    "Seek ****",
    "Still no ****...",
    "Why is it always ****?",
    "If only I had a ****...",
    "Visions of ****...",
    "Could this be a ****?",
    "Time for ****",
    "****, O ****",
    "Behold, ****!",
    "Offer ****",
    "Praise the ****!",
    "Let there be ****",
    "Ahh, ****...",
    "****",
    "****!",
    "****?",
    "****..."
]
templates2 = [
    "~none~",
    "**** ahead",
    "no **** ahead",
    "**** required ahead",
    "be wary of ****",
    "try ****",
    "likely ****",
    "seek ****",
    "still no ****...",
    "why is it always ****?",
    "if only I had a ****...",
    "didn't expect ****...",
    "visions of ****...",
    "could this be a ****?",
    "time for ****",
    "****, O ****",
    "behold, ****!",
    "offer ****",
    "praise the ****!",
    "let there be ****",
    "ahh, ****...",
    "****",
    "****!",
    "****?",
    "****..."
]
conjunctions = [
  "~none~",
  "and then",
  "or",
  "but",
  "therefore",
  "in short",
  "except",
  "by the way",
  "so to speak",
  "all the more",
  ","
]

templates1_list = []
for x in templates1:
  templates1_list.append(discord.SelectOption(label=x))

templates2_list = []
for x in templates2:
  templates2_list.append(discord.SelectOption(label=x))

conjunctions_list = []
for x in conjunctions:
  conjunctions_list.append(discord.SelectOption(label=x))

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="ring", description="Create a message")
async def ring(ctx):                       
  await ctx.respond("Create a message", view=TemplateView(responses={}), ephemeral=True)

class TemplateView(discord.ui.View):
  def __init__(self, responses, *args, **kwargs):
    self.responses = responses
    super().__init__(*args, **kwargs)

  @discord.ui.select(row=0, options=templates1_list, placeholder="First template")
  async def first_select_callback(self, select, interaction):
    self.responses["first"] = select.values[0]
    await interaction.response.send_message("")

  @discord.ui.select(row=1, options=conjunctions_list, placeholder="Conjunction")
  async def conjunction_select_callback(self, select, interaction):
    self.responses["conjunction"] = select.values[0]
    await interaction.response.send_message("")

  @discord.ui.select(row=2, options=templates2_list, placeholder="Second templates")
  async def second_select_callback(self, select, interaction):
    self.responses["second"] = select.values[0]
    await interaction.response.send_message("")

  @discord.ui.button(label="Create message", row=3, style=discord.ButtonStyle.primary)
  async def first_button_callback(self, button, interaction):
    await interaction.response.send_modal(MessageModal(title="Message", labels=self.responses))


class MessageModal(discord.ui.Modal):
  def __init__(self, labels, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)

    conjunction1 = None
    if labels["conjunction"] == ",":
      conjunction1 = ","
      labels["conjunction"] = None

    self.add_item(discord.ui.InputText(label="".join(filter(None, [labels["first"], conjunction1]))))

    if labels["conjunction"] == "~none~":
      labels["conjunction"] = None

    if labels["second"] != "~none~":
      self.add_item(discord.ui.InputText(label=" ".join(filter(None, [labels["conjunction"], labels["second"]]))))

  async def callback(self, interaction: discord.Interaction):
    text = []
    for child in self.children:
      text.append(child.label.replace("****", child.value))

    embed = discord.Embed(
      description="\n".join(text)
    )
    embed.set_author(name=interaction.user.display_name, icon_url="https://i.imgur.com/puVQ0Bp.png")

    await interaction.response.send_message(embeds=[embed])

bot.run(os.getenv('TOKEN'))