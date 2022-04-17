import disnake
from disnake.ext import commands

from ..fancy_embed import FancyEmbed


async def is_banned(guild: disnake.Guild, member_id: int) -> bool:
    """Checks if a certain member is banned."""

    ban_list = await guild.bans()
    return bool([ban for ban in ban_list if ban.user.id == member_id])


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
                embed=FancyEmbed(
                    title="🤨 Why?",
                    description="Do you got a problem with me?!",
                    color=disnake.Color.brand_red(),
                )
            )
            return

        await member.kick(reason=reason)
        await ctx.reply(
            embed=FancyEmbed(
                title=f"✅ Kicked `{member}`",
                description=reason,
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
                embed=FancyEmbed(
                    title="🤨 Why?",
                    description="Do you got a problem with me?!",
                    color=disnake.Color.brand_red(),
                )
            )
            return

        await member.ban(reason=reason)
        await ctx.reply(
            embed=FancyEmbed(
                title=f"✅ Banned `{member}`",
                description=reason,
                color=disnake.Color.brand_green(),
            ),
        )

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(
        self,
        ctx: commands.Context,
        member_id: int,
        *,
        reason: str = "no reason",
    ) -> None:
        """Unbans a member from a server."""

        member_snowflake = disnake.Object(member_id)

        if ctx.guild is None:
            return

        if member_id == ctx.author.id:
            await ctx.reply("You're not banned. _Yet._")
            return
        elif not await is_banned(ctx.guild, member_id):
            await ctx.reply("That member's not banned. Yet??? 🤔")
            return
        elif member_id == ctx.guild.me.id:
            await ctx.reply("Thanks, but I'm still here.")
            return

        await ctx.guild.unban(member_snowflake, reason=reason)

        await ctx.reply(
            embed=FancyEmbed(
                title=f"✅ Unbanned member with ID `{member_id}` for `{reason}`",
                description="Welcome back!",
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

        # Account for the message that triggered this command
        limit += 1

        num_purged = len(await ctx.channel.purge(limit=limit))

        await ctx.send(
            embed=FancyEmbed(
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
