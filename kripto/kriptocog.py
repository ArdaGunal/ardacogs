import discord
from discord.ext import commands
import requests
import json

class CoinMarketCap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def coinmarketcap(self, ctx, *coins):
        """Displays information about specified coins from CoinMarketCap"""

        # Check if at least one coin is specified
        if not coins:
            await ctx.send("Please specify at least one coin symbol.")
            return

        # Load API key from file
        with open("api_key.txt", "r") as file:
            api_key = file.read().strip()

        # Request data from CoinMarketCap API
        coin_data = {}
        for coin in coins:
            url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={coin.upper()}&CMC_PRO_API_KEY={api_key}'
            response = requests.get(url)
            data = json.loads(response.text)['data'][coin.upper()]
            coin_data[coin.upper()] = {'price': data['quote']['USD']['price'],
                                       'market_cap': data['quote']['USD']['market_cap'],
                                       'volume': data['quote']['USD']['volume_24h'],
                                       'change': data['quote']['USD']['percent_change_24h']}

        # Generate table with data
        table = '```'
        table += f"{'Coin':<10}{'Price':<20}{'Market Cap':<25}{'Volume':<25}{'Change':<15}\n"
        table += f"{'-----':<10}{'-----':<20}{'----------':<25}{'----------':<25}{'------':<15}\n"
        for coin in coins:
            data = coin_data[coin.upper()]
            price = '$' + '{:,.2f}'.format(data['price'])
            market_cap = '$' + '{:,.2f}'.format(data['market_cap'])
            volume = '$' + '{:,.2f}'.format(data['volume'])
            change = '{:,.2f}%'.format(data['change'])
            table += f"{coin.upper():<10}{price:<20}{market_cap:<25}{volume:<25}{change:<15}\n"
        table += '```'

        await ctx.send(table)

def setup(bot):
    bot.add_cog(CoinMarketCap(bot))