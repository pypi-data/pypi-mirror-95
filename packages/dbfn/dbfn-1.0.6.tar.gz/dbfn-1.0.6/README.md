The Discord Bot Functions Module contains functions to enhance and simplify your python Discord Bot.

**Instalation**
```
pip install dbfn
```

**Usage and examples**
At the moment it only contains one function: Reaction Books, which allows the user to create interactable embeds

An example of a basic book
```python
from dbfn import reactionbook

# (inside a cog)
async def function(self, ctx):

	book = reactionbook(self.bot, ctx)
	book.createpages("This page only has one line")
	book.createpages(["This page only has...", "...two"])
	await book.createbook(TITLE="Example book", MODE="numbers")
```