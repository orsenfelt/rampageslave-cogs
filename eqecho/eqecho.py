## Python imports
import pymysql
import discord
import json
import aiohttp

## Redbot imports
from redbot.core import commands
from redbot.core.utils.chat_formatting import box




class EQEcho(commands.Cog):

	def __init__(self):
        self.serverid = "740650364575023127"
        self.channelid = "740650365078339667"

	@commands.command(name="search", brief="Search database for *items*, *spells*, *npcs* or *zones*")
	async def search(self, ctx, *, query):
			
		# Set aside the author of the query
		author = ctx.author

		# Do the search
		raw_response = self.index.search(query, {'hitsPerPage' : 10})
		
		# If there's no results, return
		if raw_response['nbHits'] < 1:
			await author.send("No results found for :: **{}**".format(query))
			return
		
		# Otherwise we continue
		# Loop each result and format it
		embed = discord.Embed(color=0xEE2222, title='Search results for :: **{}**'.format(query), description='If you would like to see the full results for this search you can visit http://pantheon101.com/search?q={}'.format(query))
		embed.set_footer(text='Search powered by Algolia')
		
		for each in raw_response['hits']:
			embed.add_field(name='{}/**{}**'.format(each['type'],each['dbid']), value='[{}](http://pantheon101.com/{}/{}/{})'.format(each['name'], each['type'], each['dbid'], each['slug']), inline=False)
		
		# Send it
		await author.send(embed=embed)


	@commands.command(name="item", brief="Get information for a specific item")
	async def item(self, ctx, dbid):
	
		# Set aside the author of the query
		author = ctx.author
		
		# Prepare API url
		url = self.api_base_url + "item/{}".format(dbid)
		
		# Fetch the item
		async with self.aiohttp.request('GET', url, headers={'Accept': 'text/plain'}) as r:
			result = await r.json()
			
			embed = discord.Embed(color=0xEE2222, title='**{}**'.format(result['name']), description='[View the item on Pantheon101]({})'.format(result['url']))
			
			# Loop the json to clean it up
			for each in result:
				if (each == "id") or (result[each] == 0) or (each == "0.00") or (each == "slug") or (each == "name") or (each == "content") or (each == "icon_path") or (each == "url"):
					continue
					
				if each[:3] == "is_":
					if result[each] == 1:
						result[each] = "✅"
				
				# Add the Field
				embed.add_field(name='**{}**'.format(each), value='{}'.format(result[each]), inline=True)
			
			# Send it
			await author.send(embed=embed)
		
		