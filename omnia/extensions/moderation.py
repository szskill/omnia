import disnake
from disnake.ext import commands


class Moderation(commands.Cog):
    """The cog for moderation. Moderation cog. Moderational cog. Kick ban cog."""

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(
        self,
        ctx: commands.Context,
        member: disnake.Member,
        *,
        reason: str = "no reason",
    ) -> None:
        """Kicks a member from a server."""

        if ctx.guild is None:
            return

        if ctx.author == member:
            await ctx.reply("😔 I'm too nice to kick you.")
            return
        elif member == ctx.guild.me:
            await ctx.reply(
                embed=disnake.Embed(
                    title="🤨 Why?",
                    description="Do you got a problem with me?!",
                    color=disnake.Color.brand_red(),
                )
            )
            return

        await member.kick(reason=reason)
        await ctx.reply(
            embed=disnake.Embed(
                title=f"✅ Kicked `{member}` for `{reason}`",
                color=disnake.Color.brand_green(),
            )
        )

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(
        self,
        ctx: commands.Context,
        member: disnake.Member,
        *,
        reason: str = "no reason",
    ) -> None:
        """Bans a member from a server."""

        if ctx.guild is None:
            return

        if ctx.author == member:
            await ctx.reply("😔 I'm too nice to ban you.")
            return
        elif member == ctx.guild.me:
            await ctx.reply(
                embed=disnake.Embed(
                    title="🤨 Why?",
                    description="Do you got a problem with me?!",
                    color=disnake.Color.brand_red(),
                )
            )
            return

        await member.ban(reason=reason)
        await ctx.reply(
            embed=disnake.Embed(
                title=f"✅ Banned `{member}` for `{reason}`",
                color=disnake.Color.brand_green(),
            ),
        )

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, limit: int) -> None:
        """Deletes a certain amount of messages."""

        if not isinstance(ctx.channel, disnake.TextChannel):
            return

        # The message that triggered this command will also be counted, so we need to
        # account for that as well
        limit += 1

        num_purged = len(await ctx.channel.purge(limit=limit))

        await ctx.send(
            embed=disnake.Embed(
                title=f"Deleted {num_purged} messages",
                description=(
                    f"{ctx.author.mention}, I hope you didn't remove any important"
                    + " messages."
                ),
                color=disnake.Color.brand_green(),
            )
        )


def setup(bot: commands.Bot) -> None:
    """Loads the `Moderation` cog."""
    bot.add_cog(Moderation())
