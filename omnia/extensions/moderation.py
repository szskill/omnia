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

        if ctx.author == member:
            return await ctx.reply("😔 I'm too nice to kick you.")
        elif member == ctx.guild.me:
            return await ctx.reply(
                embed=disnake.Embed(
                    title="🤨 Why?",
                    description="Do you got a problem with me?!",
                    color=disnake.Color.brand_red(),
                )
            )

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

        if ctx.author == member:
            return await ctx.reply("😔 I'm too nice to ban you.")
        elif member == ctx.guild.me:
            return await ctx.reply(
                embed=disnake.Embed(
                    title="🤨 Why?",
                    description="Do you got a problem with me?!",
                    color=disnake.Color.brand_red(),
                )
            )

        await member.ban(reason=reason)
        await ctx.reply(
            embed=disnake.Embed(
                title=f"✅ Banned `{member}` for `{reason}`",
                color=disnake.Color.brand_green(),
            ),
        )


def setup(bot: commands.Bot) -> None:
    """Loads the `Moderation` cog."""
    bot.add_cog(Moderation())
