import discord
from discord import FFmpegPCMAudio
from discord.ext import commands, tasks
from discord.utils import get
from discord import Embed
from random import choice
from discord.ext.commands import Cog
from discord.ext.commands import has_permissions
from dotenv import load_dotenv
from server import keep_alive
import asyncio
import youtube_dl

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot('!', intents=intents)

load_dotenv()
bot = commands.Bot(command_prefix = "hel", description="Estoy probando un bot")


youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def p_join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def p_play(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""
        try:
          async with ctx.typing():
              await ctx.reply("Cargando. . . . ",mention_author=True)
              player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
              ctx.voice_client.play(player, after=lambda e: print(f'Error de reproducción: {e}') if e else None)
          embed = discord.Embed(title=f"CVR Streamer", description=f'Ahora sonando: {player.title}', color=discord.Color.blue() )
          embed.set_thumbnail(url=f"https://i.postimg.cc/VvY0hVFH/youtube-logo-gif.gif")
          await ctx.reply(embed=embed, mention_author=True)
          print(ctx.guild.name+" yt")
        except:
          await ctx.send("Error con el enlace o error para conectar al canal. Contactar a @cvr#2378")

    @commands.command()
    async def p_radio_disney(self, ctx, *, url: str = 'https://unlimited3-cl.dps.live/disney/mp364k/icecast.audio'):
        """Streams from a url- DISNEY CL"""
        try:
          async with ctx.typing():
              await ctx.reply("Cargando. . . . ",mention_author=True)
              player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
              ctx.voice_client.play(player, after=lambda e: print(f'Error de reproducción: {e}') if e else None)
          embed = discord.Embed(title=f"CVR Streamer", description=f'Ahora sonando: Radio Disney\nObserva más radios con ***help_radio***\n\nCambia el volumen con ***help_volume [x]*** (X puede ser un numero de 0 a 100)', color=discord.Color.blue() )
          embed.set_thumbnail(url=f"https://i.postimg.cc/qvmVqZh8/radio-disney.gif")
          await ctx.reply(embed=embed, mention_author=True)
          print(ctx.guild.name+" stream")
        except:
          await ctx.send("Error con el enlace o error para conectar al canal. Contactar a @cvr#2378")
    @commands.command()
    async def p_radio_ilovemusic(self, ctx, *, url: str = 'https://streams.ilovemusic.de/iloveradio1.mp3'):
        """Streams from a url- ILOVEMUSIC DE"""
        
        try:
          async with ctx.typing():
              await ctx.reply("Cargando. . . . ",mention_author=True)
              player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
              ctx.voice_client.play(player, after=lambda e: print(f'Error de reproducción: {e}') if e else None)
          embed = discord.Embed(title=f"CVR Streamer", description=f'Ahora sonando: I LOVE MUSIC [Deutsch]\nObserva más radios con ***help_radio***\n\nCambia el volumen con ***help_volume [x]*** (X puede ser un numero de 0 a 100)', color=discord.Color.red() )
          embed.set_thumbnail(url=f"https://i.postimg.cc/1Xc6rFDZ/f4c5e12a-387e-4041-a5d9-d41e68343870.png")
          await ctx.reply(embed=embed, mention_author=True)
          print(ctx.guild.name+" stream")
        except:
          await ctx.send("Error con el enlace o error para conectar al canal. Contactar a @cvr#2378")
    
    @commands.command()
    async def p_radio_chill(self, ctx, *, url: str = 'https://streams.ilovemusic.de/iloveradio17.mp3'):
        """Streams from a url- ILOVEMUSIC DE"""
        
        try:
          async with ctx.typing():
              await ctx.reply("Cargando. . . . ",mention_author=True)
              player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
              ctx.voice_client.play(player, after=lambda e: print(f'Error de reproducción: {e}') if e else None)
          embed = discord.Embed(title=f"CVR Streamer", description=f'Ahora sonando: I LOVE MUSIC [Deutsch]: Chill Music\nObserva más radios con ***help_radio***\n\nCambia el volumen con ***help_volume [x]*** (X puede ser un numero de 0 a 100)', color=discord.Color.red() )
          embed.set_thumbnail(url=f"https://i.postimg.cc/1Xc6rFDZ/f4c5e12a-387e-4041-a5d9-d41e68343870.png")
          await ctx.reply(embed=embed, mention_author=True)
          print(ctx.guild.name+" stream")
        except:
          await ctx.send("Error con el enlace o error para conectar al canal. Contactar a @cvr#2378")

    @commands.command()
    async def p_radio_hard(self, ctx, *, url: str = 'https://streams.ilovemusic.de/iloveradio21.mp3'):
        """Streams from a url- ILOVEMUSIC DE"""
        
        try:
          async with ctx.typing():
              await ctx.reply("Cargando. . . . ",mention_author=True)
              player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
              ctx.voice_client.play(player, after=lambda e: print(f'Error de reproducción: {e}') if e else None)
          embed = discord.Embed(title=f"CVR Streamer", description=f'Ahora sonando: I LOVE MUSIC [Deutsch]: *HARD STYLE*\nObserva más radios con ***help_radio***\n\nCambia el volumen con ***help_volume [x]*** (X puede ser un numero de 0 a 100)', color=discord.Color.red() )
          embed.set_thumbnail(url=f"https://i.postimg.cc/VshdSz2k/tumblr-mgeu6fl-Zh-V1rd7d9oo1-1280.gif")
          await ctx.reply(embed=embed, mention_author=True)
          print(ctx.guild.name+" stream")
        except:
          await ctx.send("Error con el enlace o error para conectar al canal. Contactar a @cvr#2378")


    @commands.command()
    async def p_radio_monstercat(self, ctx, *, url: str = 'https://streams.ilovemusic.de/iloveradio24.mp3'):
        """Streams from a url- ILOVEMUSIC DE"""
        
        try:
          async with ctx.typing():
              await ctx.reply("Cargando. . . . ",mention_author=True)
              player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
              ctx.voice_client.play(player, after=lambda e: print(f'Error de reproducción: {e}') if e else None)
          embed = discord.Embed(title=f"CVR Streamer", description=f'Ahora sonando: I LOVE MUSIC [Deutsch]: *MONSTERCAT*\nObserva más radios con ***help_radio***\n\nCambia el volumen con ***help_volume [x]*** (X puede ser un numero de 0 a 100)', color=discord.Color.red() )
          embed.set_thumbnail(url=f"https://i.postimg.cc/T2bcfNxt/monstercat.gif")
          await ctx.reply(embed=embed, mention_author=True)
          print(ctx.guild.name+" stream")
        except:
          await ctx.send("Error con el enlace o error para conectar al canal. Contactar a @cvr#2378")

    @commands.command()
    async def p_radio_party(self, ctx, *, url: str = 'https://streams.ilovemusic.de/iloveradio14.mp3'):
        """Streams from a url- ILOVEMUSIC DE"""
        
        try:
          async with ctx.typing():
              await ctx.reply("Cargando. . . . ",mention_author=True)
              player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
              ctx.voice_client.play(player, after=lambda e: print(f'Error de reproducción: {e}') if e else None)
          embed = discord.Embed(title=f"CVR Streamer", description=f'Ahora sonando: I LOVE MUSIC [Deutsch]: *Party Time*\nObserva más radios con ***help_radio***\n\nCambia el volumen con ***help_volume [x]*** (X puede ser un numero de 0 a 100)', color=discord.Color.red() )
          embed.set_thumbnail(url=f"https://i.postimg.cc/J7jj9y3g/tenor.gif")
          await ctx.reply(embed=embed, mention_author=True)
          print(ctx.guild.name+" stream")
        except:
          await ctx.send("Error con el enlace o error para conectar al canal. Contactar a @cvr#2378")
    @commands.command()
    async def p_radio_carolina(self, ctx, *, url: str = 'http://unlimited3-cl.dps.live/carolinafm/aac/icecast.audio'):
        """Streams from a url- ILOVEMUSIC DE"""
        
        try:
          async with ctx.typing():
              await ctx.reply("Cargando. . . . ",mention_author=True)
              player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
              ctx.voice_client.play(player, after=lambda e: print(f'Error de reproducción: {e}') if e else None)
          embed = discord.Embed(title=f"CVR Streamer", description=f'Ahora sonando: I LOVE MUSIC [Deutsch]: *Party Time*\nObserva más radios con ***help_radio***\n\nCambia el volumen con ***help_volume [x]*** (X puede ser un numero de 0 a 100)', color=discord.Color.red() )
          embed.set_thumbnail(url=f"https://i.postimg.cc/J7jj9y3g/tenor.gif")
          await ctx.reply(embed=embed, mention_author=True)
          print(ctx.guild.name+" stream")
        except:
          await ctx.send("Error con el enlace o error para conectar al canal. Contactar a @cvr#2378")

    @commands.command()
    async def p_volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def p_stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        embed = discord.Embed(title=f"CVR Streamer", description=f'La reproducción se ha detenido\nObserva más radios con ***help_radio***\n\nCambia el volumen con ***help_volume [x]*** (X puede ser un numero de 0 a 100)', color=discord.Color.blue() )
        embed.set_thumbnail(url=f"https://i.postimg.cc/85mbkxsG/Stop-button-play-pause-music.png")
        await ctx.reply(embed=embed, mention_author=True)
        print(ctx.guild.name+" stop")
        await ctx.voice_client.disconnect()

    @p_play.before_invoke
    @p_radio_disney.before_invoke
    @p_radio_ilovemusic.before_invoke
    @p_radio_chill.before_invoke
    @p_radio_hard.before_invoke
    @p_radio_monstercat.before_invoke
    @p_radio_party.before_invoke
    @p_radio_carolina.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()






@bot.command()
async def p_creditos(ctx):
    embed = discord.Embed(title=f"CREDITOS HELPER ERPG", description="Bot created by CVR.", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name+" Creditos")

@bot.command()
async def p(ctx):
    embed = discord.Embed(title=f"Listado Comandos", description="-help_donate\n-help_creditos\n-help_duel\n-help[x]\n`(considere x como turno al hacer dungeon)`\nEjemplo: `help4`\n-help_area[x] (AÚN NO ESTÁ COMPLETO)\n`Considere x como numero de area`\nEjemplo: `help_area2`", color=discord.Color.red() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name+ " Help")


@bot.command()
async def p1(ctx):
    embed = discord.Embed(title=f"Turno 1", description="`Charge edgy sword`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p2(ctx):
    embed = discord.Embed(title=f"Turno 2", description="`Weakness spell`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p3(ctx):
    embed = discord.Embed(title=f"Turno 3", description="`Charge edgy sword`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p4(ctx):
    embed = discord.Embed(title=f"Turno 4", description="`Protect`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p5(ctx):
    embed = discord.Embed(title=f"Turno 5", description="Charge edgy sword`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p6(ctx):
    embed = discord.Embed(title=f"Turno 6", description="`Charge edgy armor`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p7(ctx):
    embed = discord.Embed(title=f"Turno 7", description="`Charge edgy sword`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p8(ctx):
    embed = discord.Embed(title=f"Turno 8", description="`Charge edgy armor`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p9(ctx):
    embed = discord.Embed(title=f"Turno 9", description="`Charge edgy sword`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p10(ctx):
    embed = discord.Embed(title=f"Turno 10", description="`Charge edgy armor`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p11(ctx):
    embed = discord.Embed(title=f"Turno 11", description="`Charge edgy sword`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p12(ctx):
    embed = discord.Embed(title=f"Turno 12", description="`Charge edgy armor`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p13(ctx):
    embed = discord.Embed(title=f"Turno 13", description="`Charge edgy sword`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p14(ctx):
    embed = discord.Embed(title=f"Turno 14", description="`protect`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p15(ctx):
    embed = discord.Embed(title=f"Turno 15", description="`Charge edgy sword`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p16(ctx):
    embed = discord.Embed(title=f"Turno 16", description="`Protect`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p17(ctx):
    embed = discord.Embed(title=f"Turno 17", description="`Charge edgy sword`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p18(ctx):
    embed = discord.Embed(title=f"Turno 18", description="`Invulneravility`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p19(ctx):
    embed = discord.Embed(title=f"Turno 19", description="`Charge edgy sword`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p20(ctx):
    embed = discord.Embed(title=f"Turno 20", description="`Healing Spell`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p21(ctx):
    embed = discord.Embed(title=f"Turno 21", description="`Charge edgy sword`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p22(ctx):
    embed = discord.Embed(title=f"Turno 22", description="`Protect`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p23(ctx):
    embed = discord.Embed(title=f"Turno 23", description="`Charge edgy sword`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p24(ctx):
    embed = discord.Embed(title=f"Turno 24", description="`Protect`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p25(ctx):
    embed = discord.Embed(title=f"Turno 25", description="`Charge edgy sword`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p26(ctx):
    embed = discord.Embed(title=f"Turno 26", description="`Protect`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p27(ctx):
    embed = discord.Embed(title=f"Turno 27", description="`Charge edgy sword`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p28(ctx):
    embed = discord.Embed(title=f"Turno 28", description="`Protect`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p29(ctx):
    embed = discord.Embed(title=f"Turno 29", description="`Charge edgy sword`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p30(ctx):
    embed = discord.Embed(title=f"Turno 30", description="`Protect`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p31(ctx):
    embed = discord.Embed(title=f"Turno 31", description="`Charge edgy sword`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p32(ctx):
    embed = discord.Embed(title=f"Turno 32", description="`Charge edgy sword`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p33(ctx):
    embed = discord.Embed(title=f"Turno 33", description="`Charge edgy sword`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p34(ctx):
    embed = discord.Embed(title=f"Turno 34", description="`Charge edgy sword`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p35(ctx):
    embed = discord.Embed(title=f"Turno 35", description="`Charge edgy sword`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def p36(ctx):
    embed = discord.Embed(title=f"TURNO FINAL", description="`ATTACK`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.listen()
async def on_message(message):
    if "rpg duel " in message.content.lower():
        await message.channel.send(":dagger: Ataque\n :shield: Defensa\n :anchor: Vida\n :straight_ruler: Nivel\n :credit_card: Monedas\n :tools: Espada y armadura\n :magnet: Encantamientos \nMira mas comandos de este bot con `help`")
        print(message.guild.name+ " Duel")
@bot.listen()
async def on_message(message):
    if "duel a bot lmao" in message.content.lower():
        embed = discord.Embed(title="XD", color=discord.Color.purple())
        embed.set_image(url="https://media.tenor.com/images/9133bff595c13cd663e40f6b73ff1196/tenor.gif")
        await message.channel.send(embed=embed)
        print(message.guild.name+ " risitas")
@bot.listen()
async def on_message(message):
    if "nobody won anything" in message.content.lower():
        embed = discord.Embed(title="oh :c", color=discord.Color.purple())
        embed.set_image(url="https://i.postimg.cc/vZPVPBZc/Press-F.jpg")
        await message.channel.send(embed=embed)
        print(message.guild.name+ " f")        
@bot.listen()
async def on_message(message):
    if "you have been in a duel recently" in message.content.lower():
        embed = discord.Embed(title="oh :c", color=discord.Color.purple())
        embed.set_image(url="https://i.postimg.cc/vZPVPBZc/Press-F.jpg")
        await message.channel.send(embed=embed)
        print(message.guild.name+ " f")        
@bot.listen()
async def on_message(message):
    if "both players are dead! better luck next time" in message.content.lower():
        embed = discord.Embed(title="oh :c", color=discord.Color.purple())
        embed.set_image(url="https://i.postimg.cc/vZPVPBZc/Press-F.jpg")
        await message.channel.send(embed=embed)
        print(message.guild.name+ " f")   
async def on_message(message):
    if "cancelled" in message.content.lower():
        embed = discord.Embed(title="oh :c", color=discord.Color.purple())
        embed.set_image(url="https://i.postimg.cc/vZPVPBZc/Press-F.jpg")
        await message.channel.send(embed=embed)
        print(message.guild.name+ " f") 

@bot.command()
async def p_radio(ctx):
    embed = discord.Embed(title=f"OPAAA RADIOS DISPONIBLES", description="-help_radio_disney\n-help_radio_ilovemusic\n-help_radio_chill\n-help_radio_hard\n-help_radio-monstercat\n-help_radio_party\n***Apagar con `-help_stop`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/discords-bots/images/2/2e/EPIC_RPG.png/revision/latest?cb=20200820053725")
    await ctx.send(embed=embed)
    print(ctx.guild.name+ "Lista radio")

@bot.command()
async def p_avatar(ctx, member:discord.Member):
  await ctx.send(member.avatar_url)

@bot.command()
async def p_tatakae(ctx):
  embed = discord.Embed(title="TATAKAE CSM", color=discord.Color.purple())
  embed.set_image(url="https://i.postimg.cc/Gpd6chD6/3d8b18ea81a564a37f7fc283f3a5a54a.gif")
  await ctx.channel.send(embed=embed)
  print(ctx.guild.name+ " tatakae")

@bot.command()
async def p_levi(ctx):
  embed = discord.Embed(title="DALE CHICO LEVI", color=discord.Color.purple())
  embed.set_image(url="https://i.postimg.cc/k553Qg5K/31c0776b109b76143605887067803464.gif")
  await ctx.channel.send(embed=embed)
  print(ctx.guild.name+ " levi")
@bot.command()
async def p_adioss(ctx):
  embed = discord.Embed(title="adioss", color=discord.Color.purple())
  embed.set_image(url="https://i.postimg.cc/DZbN6J3J/54c7cdd0dac608e45fd4a4eef9fb7aa6.gif")
  await ctx.channel.send(embed=embed)
@bot.command()
async def p_chao(ctx):
  embed = discord.Embed(title="Xiaonovimo¡", color=discord.Color.purple())
  embed.set_image(url="https://i.postimg.cc/Ss8Z8Bcc/tenor.gif")
  await ctx.channel.send(embed=embed)

@bot.listen()
async def on_message(message):
    if "rpg hunt" in message.content.lower():
      await asyncio.sleep(60)
      await message.reply("Momento de hacer hunt xd :crossed_swords: ",mention_author=True)

@bot.listen()
async def on_message(message):
    if "rpg adv" in message.content.lower():
      await asyncio.sleep(3600)
      await message.reply("Momento de hacer adventure xd",mention_author=True)
@bot.listen()
async def on_message(message):
    if "rpg adventure" in message.content.lower():
      await asyncio.sleep(3600)
      await message.reply("Momento de hacer adventure xd",mention_author=True)
@bot.listen()
async def on_message(message):
    if "rpg farm" in message.content.lower():
      await asyncio.sleep(600)
      await message.reply("Momento de hacer farm xd",mention_author=True)
@bot.listen()
async def on_message(message):
    if "rpg daily" in message.content.lower():
      await asyncio.sleep(86400)
      await message.reply("Momento de hacer DAILY xd",mention_author=True)
@bot.listen()
async def on_message(message):
    if "rpg buy ed" in message.content.lower():
      await asyncio.sleep(10800)
      await message.reply("Momento de comprar cajita xd",mention_author=True)
@bot.listen()
async def on_message(message):
    if "rpg tr" in message.content.lower():
      await asyncio.sleep(900)
      await message.reply("Momento de hacer TRAINING xd",mention_author=True)


#Eventos 
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Como juegas ERPG: Usa prefijo \"help\" "))
    print("Bot iniciado")



keep_alive()
bot.add_cog(Music(bot))

bot.run("")
