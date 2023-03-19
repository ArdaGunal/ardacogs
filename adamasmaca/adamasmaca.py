import random
import redbot.core.commands as commands

class Adamasmaca(commands.Cog):
    """Adam Asmaca Oyunu"""

    def __init__(self, bot):
        self.bot = bot
        self.words = []

    @commands.group()
    async def adamasmaca(self, ctx):
        """Adam asmaca oyunu"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @adamasmaca.command(name="kelimeekle")
    async def kelime_ekle(self, ctx, kelime):
        """Kelime ekleme"""
        if kelime in self.words:
            await ctx.send("Bu kelime zaten eklenmiş.")
        else:
            self.words.append(kelime)
            await ctx.send("Kelime eklendi.")

    @adamasmaca.command(name="puanlar")
    async def puanlar(self, ctx):
        """Puanları listeleme"""
        scores = await self.bot.get_cog("Scores").get_scores()
        if not scores:
            await ctx.send("Henüz hiç puan yok.")
        else:
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            msg = "Puanlar:\n"
            for i, score in enumerate(sorted_scores):
                user_id = score[0]
                points = score[1]
                user = await self.bot.fetch_user(user_id)
                msg += f"{i+1}. {user.name}: {points}\n"
            await ctx.send(msg)

    @adamasmaca.command(name="oyun")
    async def oyun(self, ctx):
        """Adam asmaca oyunu"""
        if not self.words:
            await ctx.send("Lütfen önce bir kelime listesi ekleyin.")
            return

        kelime = random.choice(self.words).lower()
        guessed = set()
        lives = 6

        def is_valid_guess(guess):
            if len(guess) != 1:
                return False
            if guess in guessed:
                return False
            if not guess.isalpha():
                return False
            return True

        def get_display_word():
            displayed_word = ""
            for letter in kelime:
                if letter in guessed:
                    displayed_word += letter + " "
                else:
                    displayed_word += "_ "
            return displayed_word.strip()

        async def end_game():
            displayed_word = get_display_word()
            if "_" not in displayed_word:
                await ctx.send(f"Tebrikler! Kelimeyi buldunuz: **{kelime.capitalize()}**")
                await self.bot.get_cog("Scores").add_score(ctx.author.id, 6)
            else:
                await ctx.send(f"Malesef kaybettiniz. Kelime **{kelime.capitalize()}** olacaktı.")
            return

        while lives > 0:
            displayed_word = get_display_word()
            msg = f"Kelime: **{displayed_word}**\nKalan canlar: {lives}\nHarf tahmin etmek için bir harf yazın."

            if guessed:
                guessed_str = ", ".join(sorted(guessed))
                msg += f"\nDaha önce tahmin edilen harfler:
