import nextcord
from nextcord.ext import commands
from requests import get
from bs4 import BeautifulSoup
from utils.objects import Embed
from pandas import read_html

class LiveStream(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stream_embeds = {}
        
    @commands.command()
    async def stream(self, ctx):
        embed, links = await self.get_matches()
        await ctx.reply(embed=embed)

        def check(m):
            c = m.content
            return m.author == ctx.author and m.channel == ctx.channel and c.isdigit() and int(c) <= len(links)

        msg = await self.bot.wait_for("message", check=check)
        link = links[int(msg.content) - 1]
        embed = self.stream_embeds.get(link)
        if embed is None:
            embed = await self.get_streams(link, 10)
            self.stream_embeds[link] = embed
        print(embed)
        await ctx.reply(embed=embed)

    async def get_matches(self):
        html = BeautifulSoup(get("https://reddit.soccerstreamshd.com/").text, 'html.parser')
        i = 1
        matches = ""
        links = []
        for div in html.find('div', {"class": "ibox"}).find('div').find_all('div', recursive=False):
            if div.find('span', {"class": "live-status"}):
                matches += f"{i}. " + ' '.join(div.text.split()).replace("LIVE", "-") + "\n"
                links.append(div.find('a').get('href'))
                i += 1
        embed = Embed(title="Live Matches", description=matches)
        return embed, links

    async def get_streams(self, url, n):
        html = BeautifulSoup(get(url).text, 'html.parser')
        embed = Embed(title=html.find('title').text.splitlines()[0])
        for row in html.find('table').find('tbody').find_all('tr', limit=n):
            td = row.find_all('td')
            channel = td[0].text.strip()
            link_lang_quality = td[0].find('a').get('href') + '\n' + td[1].text + ', ' + td[4].text
            embed.add_field(name=channel, value=link_lang_quality, inline=False)
        return embed

def setup(bot):
    bot.add_cog(LiveStream(bot))
