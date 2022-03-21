import tekore

from discord import Embed

from settings import SPOTIFY_ID, SPOTIFY_SECRET


class SpotifyCommands:
    def __init__(self):
        self.token = tekore.request_client_token(SPOTIFY_ID, SPOTIFY_SECRET)
        self.client = tekore.Spotify(self.token, asynchronous=True)

    async def get_track(self, ctx, query: str = None):
        if query is None:
            await ctx.send("No search query specified")
            return

        tracks, = await self.client.search(query, limit=5)
        embed = Embed(title="Track search results", color=0x1DB954)
        embed.set_thumbnail(url="https://i.imgur.com/890YSn2.png")
        embed.set_footer(text="Requested by " + ctx.author.display_name)

        for t in tracks.items:
            artist = t.artists[0].name
            url = t.external_urls["spotify"]

            message = "\n".join([
                "[Spotify](" + url + ")",
                ":busts_in_silhouette: " + artist,
                ":cd: " + t.album.name
            ])
            embed.add_field(name=t.name, value=message, inline=False)

        await ctx.send(embed=embed)
