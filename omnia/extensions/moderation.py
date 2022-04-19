import disnake
from disnake.ext import commands

from ..omnia import Omnia
from ..fancy_embed import FancyEmbed


async def is_banned(guild: disnake.Guild, member_id: int) -> bool:
    """Checks if a certain member is banned."""

    ban_list = await guild.bans()
    return bool([ban for ban in ban_list if ban.user.id == member_id])


def get_warns_key(ctx: commands.Context, member: disnake.Member) -> str:
    """Gets the warns key for a member."""

    assert ctx.guild is not None
    return f"{ctx.bot.redis_keyspace}.guilds.{ctx.guild.id}.members.{member.id}.warns"


class Moderation(commands.Cog):
    """The cog for moderation. Moderation cog. Moderational cog. Kick ban cog."""

    def __init__(self, bot: Omnia) -> None:
        self.bot = bot

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
                    ctx=ctx,
                    title="🤨 Why?",
                    description="Do you got a problem with me?!",
                    color=disnake.Color.brand_red(),
                )
            )
            return

        await member.kick(reason=reason)
        await ctx.reply(
            embed=FancyEmbed(
                ctx=ctx,
                title=f"✅ Kicked `{member}`",
                description=reason,
                color=disnake.Color.brand_green(),
            )
        )

        await member.send(f"You've been kicked from `{ctx.guild.name}` for `{reason}`.")

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
                    ctx=ctx,
                    title="🤨 Why?",
                    description="Do you got a problem with me?!",
                    color=disnake.Color.brand_red(),
                )
            )
            return

        await member.ban(reason=reason)
        await ctx.reply(
            embed=FancyEmbed(
                ctx=ctx,
                title=f"✅ Banned `{member}`",
                description=reason,
                color=disnake.Color.brand_green(),
            ),
        )

        await member.send(f"You've been banned from `{ctx.guild.name}` for `{reason}`.")

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
                ctx=ctx,
                title=f"✅ Unbanned member with ID `{member_id}` for `{reason}`",
                description="Welcome back!",
                color=disnake.Color.brand_green(),
            ),
        )

    @commands.command(aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, limit: int) -> None:
        """Deletes a certain amount of messages."""

        if not isinstance(ctx.channel, disnake.TextChannel):
            return

        # Account for the message that triggered this command
        limit += 1

        num_purged = len(await ctx.channel.purge(limit=limit))

        reply_message = await ctx.send(
            embed=FancyEmbed(
                ctx=ctx,
                title=f"Deleted {num_purged} messages",
                description=(
                    f"{ctx.author.mention}, I hope you didn't remove any important"
                    + " messages."
                ),
                color=disnake.Color.brand_green(),
            )
        )

        await reply_message.delete(delay=3)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def warn(
        self,
        ctx: commands.Context,
        member: disnake.Member,
        *,
        reason: str = "no reason",
    ) -> None:
        if ctx.guild is None:
            return

        await self.bot.redis_db.lpush(get_warns_key(ctx, member), reason)

        await ctx.reply(
            embed=FancyEmbed(
                ctx=ctx,
                title="✅ Warned",
                description=f"You've warned {member.mention} for `{reason}`.",
                color=disnake.Color.brand_green(),
            )
        )

    @commands.command()
    async def warns(self, ctx: commands.Context, member: disnake.Member) -> None:
        warns = await self.bot.redis_db.lrange(get_warns_key(ctx, member), 0, -1)

        if not warns:
            await ctx.reply(
                embed=FancyEmbed(
                    ctx=ctx,
                    title="🤔 No warns",
                    description=f"{member.mention} has no warns.",
                    color=disnake.Color.brand_green(),
                )
            )
            return

        await ctx.reply(
            embed=FancyEmbed(
                ctx=ctx,
                title=f"Warns for {member}",
                description=(
                    f"This member has a total of {len(warns)} warn(s)\n\n"
                    + "\n".join(warns)
                ),
                color=self.bot.primary_color,
            )
        )

    @commands.command(name="clear-warns")
    @commands.has_permissions(manage_guild=True)
    async def clear_warns(self, ctx: commands.Context, member: disnake.Member) -> None:
        await self.bot.redis_db.delete(get_warns_key(ctx, member))
        await ctx.reply(
            embed=FancyEmbed(
                ctx=ctx,
                title="✅ Cleared warns",
                description="get out of jail ig...",
                color=disnake.Color.brand_green(),
            )
        )


def setup(bot: Omnia) -> None:
    """Loads the `Moderation` cog."""
    bot.add_cog(Moderation(bot))
