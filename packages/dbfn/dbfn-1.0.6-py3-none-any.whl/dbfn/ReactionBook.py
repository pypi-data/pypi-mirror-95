from discord import Embed

# Exceptions
class InvaildArgType(TypeError):
    def __init__(self, name, types):
        self.name = name
        self.types = " or ".join([str(i) for i in types])
    def __str__(self):
        return "%s must be given as a %s" % (self.name, self.types)
class InvaildLineSize(ValueError):
    def __str__(self):
        return "lines must be between 1 - 20"
class InvalidPageLength(ValueError):
    def __str__(self):
        return "pages can not be left empty"
class InvalidMode(ValueError):
    def __str__(self):
        return "must be set to 'arrows', 'numbers', 'colours' or 'custom'"
class TooManyPages(ValueError):
    def __str__(self):
        return "the mode 'numbers' is limited to 9 pages"

# Functions
def validate(name, var, types):
    if None in types and var == None:
        return
    if type(var) not in types:
        raise InvaildArgType(name, types)

def switch(val, check):
    try:
        if not check[2]:
            if val: return False
            return True
    except: return val

# Bot Functions
class reactionbook:

    def __init__(self, bot, ctx, TITLE=None, LINES=8):
        """ Initiates the book

            ____ARGS____

            bot is infomation from you bot and is used to manage reactions

            ctx is the context and is used to send the reactivebook to the
            channel

            ____KWARGS_____

            TITLE is the message displayed on the top of the first page

            LINES is the number of lines on each page, by default it is
            set to 8
        """

        validate("TITLE", TITLE, [str, None])
        validate("LINES", LINES, [int])
        if 1 > LINES or LINES > 20:
            raise InvaildLineSize()

        self.bot = bot
        self.ctx = ctx
        self.TITLE = TITLE
        self.LINES = LINES
        
        self.pagelines = 0
        self.booklines = 0
        self.pages = []

    def createpages(self, LIST, LINE="%l", ELSE_LINE=None, SUBHEADER=None,
                     EMPTY=None, NEW_PAGE=True, ITEM_PER_PAGE=False, **checks):
        """ Iterates through LIST which is a list/tuple. The list/tuple
            itself can contain a string or another list/tuple. A use of this
            would be if you had a list of users and then each user had sub
            data like a name, id, etc.

            A brief rundown of all the args and kwargs:

            ____ARGS____
            
            LIST is an array which contains all the lines/line objects. You
            can provide a string and it converted into a list by spliting it
            into lines

            ____KWARGS____

            If LIST contains all the lines, LINE shows how each line it to
            be displayed
            %l will become the line or line object
            %i will become the all the items in the line object, if the line
            object is a dictionary
            %0 will become the first item in the line object, so following
            that logic %1 will become the second, and so on, this function
            does not support sets, but if the line object is a dictionary and
            contains a list/tuple it will
            %lt will become the total lines, i.e. the total number of lines
            %lc will become the current lines, i.e. the total number of lines on
            the current page
            In addition any text can be included
            
            ELSE_LINE is the line that will be displayed if the checks fail
            
            SUBHEADER is the first line of the first page, and won't show if
            there are no lines

            EMPTY is the message given if there are no items in the array or
            if every check fails

            CHECKS and SUBCHECKS
             - All CHECKS must be True, while only one of the SUBCHECKS has
               to be
             - Each check has three parts: the line or line object to be
               checked, the statement to compare it against, and whether the
               result should be True or False
             - First arg, the item to check. If it is a line to be checked,
               set this to 0, otherwise, you can either provide the position
               of the item in the line object or a modified item (if you
               want to run it through a function)
             - Second arg, the item to compared to. This value will be
               compared the line or the result from the first arg
             - Third arg, this is optional and by default is set to True.
               If this is set to True, the check will only be pass True if
               this result is True, if this is set to False, the check will
               only pass if the result is False
             - If you need to use bot or ctx in your statement, use self.bot
               and self.ctx
        """

        # Checks
        CHECKS = ["", "", ""]
        SUBCHECKS = ["", "", ""]
        CHECKS[0] = checks.get("check1", None)       
        CHECKS[1] = checks.get("check2", None)       
        CHECKS[2] = checks.get("check3", None)     
        SUBCHECKS[0] = checks.get("subcheck1", None) 
        SUBCHECKS[1] = checks.get("subcheck2", None) 
        SUBCHECKS[2] = checks.get("subcheck3", None)

        # Validates args
        if type(LIST) == str:
            LIST = LIST.split("\n")
        validate("LIST", LIST, [list, tuple, set, dict])
        validate("LINE", LINE, [str])
        validate("ELSE_LINE", ELSE_LINE, [str, None])
        validate("SUBHEADER", SUBHEADER, [str, None])
        validate("EMPTY", EMPTY, [str, None])
        validate("NEW_PAGE", NEW_PAGE, [bool])
        for value in CHECKS:
            validate("CHECKS", value, [tuple, list, None])
        for value in SUBCHECKS:
            validate("SUBCHECKS", value, [tuple, list, None])

        newpage = True
        pages = self.pages
        plines = self.pagelines
        blines = self.booklines
        if NEW_PAGE: plines = 0

        # CHECKS and SUBCHECKS
        def check(self, items):            
            val = [True, True, True]
            subval = [False, False, False]
            if SUBCHECKS[0] == None:
                if SUBCHECKS[1] == None:
                    if SUBCHECKS[2] == None:
                        subval = [True, True, True]

            def fcheck(self, check, items):
                check = check.replace("%l", str(items))
                if type(LIST) == dict:
                    items = LIST[items]
                    check = check.replace("%i", str(items))
                if type(items) in [list, tuple]:
                    i = 0
                    for item in items:
                        check = check.replace("%" +  str(i), str(item))
                        i += 1
                try: return eval(check)
                except: return check

            i = 0
            for CHECK in CHECKS:
                if CHECK:
                    if type(items) == int:
                        val[i] = (items[CHECK[0]] == CHECK[1])
                    else:
                        val[i] = (fcheck(self, CHECK[0], items) == CHECK[1])
                    val[i] = switch(val[i], CHECK)
                i += 1
            checks = val[0] and val[1] and val[2]

            i = 0
            for SUBCHECK in SUBCHECKS:
                if SUBCHECK:
                    if type(items) == int:
                        subval[i] = (items == SUBCHECK[1])
                    else:
                        subval[i] = (fcheck(self, SUBCHECK[0], items) ==
                                     SUBCHECK[1])
                    subval[i] = switch(subval[i], SUBCHECK)
                i += 1
            subchecks = subval[0] or subval[1] or subval[2]

            return checks and subchecks

        # Formats the line
        def formatline(page, items):
            page = page.replace("%l", str(items))
            if type(LIST) == dict:
                items = LIST[items]
                page = page.replace("%i", str(items))
            if type(items) in [list, tuple]:
                i = 0
                for item in items:
                    page = page.replace("%" +  str(i), str(item))
                    i += 1
            page = page.replace("%lt", str(blines))
            page = page.replace("%lc", str(plines))
            return page

        # Create pages
        for items in LIST:
            if newpage:
                pages.append("")
                if SUBHEADER:
                    pages[-1] += SUBHEADER + "\n"
                newpage = False

            if check(self, items):
                plines += 1
                blines += 1
                pages[-1] += formatline(LINE, items) + "\n"
            elif ELSE_LINE:
                plines += 1
                blines += 1
                pages[-1] += formatline(ELSE_LINE, items) + "\n"
            else: continue

            if ITEM_PER_PAGE or plines == self.LINES:
                plines = 0
                newpage = True

        if not blines:
            if not len(pages):
                if SUBHEADER:
                    pages[-1] += SUBHEADER  + "\n"
            pages[-1] += EMPTY

        self.pagelines = plines
        self.booklines = blines

    # Creates and manages a book
    async def createbook(self, HEADER=None, SHOW_RESULTS=False, TIMEOUT=60,
                         MODE="arrows", FOOTER_IMG=None, COLOUR=0x0,
                         **reactions): # TODO CUSTOM CHANNEL
        """ Publishes the book and manages interactions:

            ____KWARGS____
            
            HEADER is the first line under the TITLE for every page
            
            SHOW_RESULTS, whether or not to display how many lines each page
            is displaying out of the total number or lines, setting this will
            remove HEADER

            TIMEOUT is the amount of time in seconds before the book becomes
            non responsive, by default it is set to a minute

            MODE is the type of reactions that will be displayed, arrows,
            numbers, colours, or custom

            The rest of kwargs should be fairly straightforward, with more
            functionality being added soon
        """

        # Validates args
        validate("HEADER", HEADER, [str, None])
        validate("SHOW_RESULTS", SHOW_RESULTS, [bool])
        validate("TIMEOUT", TIMEOUT, [int])
        validate("MODE", MODE, [str])
        validate("FOOTER_IMG", FOOTER_IMG, [str, None])
        validate("COLOUR", COLOUR, [int])
        if not self.pages:
            raise InvalidPageLength()

        pagenum = 1
        pagemax = len(self.pages)
        TITLE = self.TITLE
        pages = self.pages

        if not TITLE:
            TITLE = ""
        if not FOOTER_IMG:
            FOOTER_IMG = ""

        # MODE + EMOJIS
        if MODE == "arrows":
            LEFT_EMOJI = reactions.get("left_emoji", "⬅️")
            RIGHT_EMOJI = reactions.get("right_emoji", "➡")
        elif MODE == "numbers":
            if len(pages) > 10:
                raise TooManyPages()
            ONE_EMOJI = reactions.get("one_emoji", "1️⃣")
            TWO_EMOJI = reactions.get("two_emoji", "2️⃣")
            THREE_EMOJI = reactions.get("three_emoji", "3️⃣")
            FOUR_EMOJI = reactions.get("four_emoji", "4️⃣")
            FIVE_EMOJI = reactions.get("five_emoji", "5️⃣")
            SIX_EMOJI = reactions.get("six_emoji", "6️⃣")
            SEVEN_EMOJI = reactions.get("seven_emoji", "7️⃣")
            EIGHT_EMOJI = reactions.get("eight_emoji", "8️⃣")
            NINE_EMOJI = reactions.get("nine_emoji", "9️⃣")
            TEN_EMOJI = reactions.get("ten_emoji", "🔟")
            numbers = [ONE_EMOJI, TWO_EMOJI, THREE_EMOJI, FOUR_EMOJI,
                       FIVE_EMOJI, SIX_EMOJI, SEVEN_EMOJI, EIGHT_EMOJI,
                       NINE_EMOJI, TEN_EMOJI]
        # elif MODE == "colours":
            # pass
        # elif MODE == "custom":
            # pass
        else:
            raise InvalidMode()
        
        def getresults(pagenum):
            message = "Showing {} - {} results out of {}\n\n"
            minresults = (pagenum - 1) * self.LINES + 1
            if pagenum == len(pages):
                maxresults = self.booklines
            else:
                maxresults = minresults + self.LINES - 1
            return message.format(minresults, maxresults, self.booklines)

        def page():
            return f"{HEADER}{pages[pagenum - 1]}"

        def footer():
            return f"Page {pagenum}/{pagemax}"

        if not pages:
            maxpage = 1
        if SHOW_RESULTS:
            HEADER = getresults(pagenum)
        elif HEADER:
            HEADER += "\n\n"
        else:
            HEADER = ""

        # Publishes the book
        embed = Embed(title=TITLE, description=page(), colour=COLOUR)
        embed.set_footer(text=footer(), icon_url=FOOTER_IMG)
        msg = await self.ctx.send(embed=embed)

        # Add reactions
        if MODE == "arrows":
            await msg.add_reaction(LEFT_EMOJI)
            await msg.add_reaction(RIGHT_EMOJI)
        elif MODE == "numbers":
            for i in range(0, len(pages)):
                await msg.add_reaction(numbers[i])
        elif MODE == "colours":
            pass # TODO
        elif MODE == "custom":
            pass # TODO

        def check(reaction, user):
            if MODE == "arrows":
                emoji = (str(reaction.emoji) in [LEFT_EMOJI, RIGHT_EMOJI])
            elif MODE == "numbers":
                emoji = (str(reaction.emoji) in numbers)
            elif MODE == "colours":
                pass # TODO
            elif MODE == "custom":
                pass # TODO

            author = (user == self.ctx.author)
            message = (reaction.message.id == msg.id)

            return emoji and author and message

        wait = self.bot.wait_for
        async def forreaction():
            return await wait("reaction_add", timeout=TIMEOUT, check=check)
        
        # Manages the book
        while True:
            try:
                # Waits for and checks reactions
                reaction, user = await forreaction()
                try: await msg.remove_reaction(reaction, user)
                except: pass

                # Reaction logic
                if MODE == "arrows":
                    if str(reaction.emoji) == LEFT_EMOJI:
                        pagenum -= 1
                        if pagenum < 1:
                            pagenum = len(pages)
                    elif str(reaction.emoji) == RIGHT_EMOJI:
                        pagenum += 1
                        if pagenum > len(pages):
                            pagenum = 1
                elif MODE == "numbers":
                    if str(reaction.emoji) == ONE_EMOJI:
                        pagenum = 1
                    elif str(reaction.emoji) == TWO_EMOJI:
                        pagenum = 2
                    elif str(reaction.emoji) == THREE_EMOJI:
                        pagenum = 3
                    elif str(reaction.emoji) == FOUR_EMOJI:
                        pagenum = 4
                    elif str(reaction.emoji) == FIVE_EMOJI:
                        pagenum = 5
                    elif str(reaction.emoji) == SIX_EMOJI:
                        pagenum = 6
                    elif str(reaction.emoji) == SEVEN_EMOJI:
                        pagenum = 7
                    elif str(reaction.emoji) == EIGHT_EMOJI:
                        pagenum = 8
                    elif str(reaction.emoji) == NINE_EMOJI:
                        pagenum = 9
                    elif str(reaction.emoji) == TEN_EMOJI:
                        pagenum = 10
                elif MODE == "colours":
                    pass # TODO
                elif MODE == "custom":
                    pass # TODO

                if SHOW_RESULTS: HEADER = getresults(pagenum)
                embed = Embed(title=TITLE, description=page(), colour=COLOUR)
                embed.set_footer(text=footer(), icon_url=FOOTER_IMG)
                await msg.edit(embed=embed)
            except:
                if SHOW_RESULTS: HEADER = getresults(pagenum)
                embed = Embed(title=TITLE, description=page(), colour=COLOUR)
                embed.set_footer(text=f"Request timed out", icon_url=FOOTER_IMG)
                try: await msg.edit(embed=embed)
                except: pass
                break
