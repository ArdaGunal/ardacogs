import redbot.core
import random

class Tahmin(discord.Client):
    async def on_ready(self):
        print(f'Giriş yapıldı: {self.user.name}')
    
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith('!startgame'):
            await self.start_game(message)
            
    async def start_game(self, message):
        word = input("Kelimeyi girin: ").lower().strip()
        max_attempts = int(input("Max tahmin sayısı girin: "))
        underscores = "_" * len(word)
        embed = discord.Embed(title=f"Tahmin Oyunu Başladı! Kelime: {underscores}", color=0xff0000)
        await message.author.send(embed=embed)
        attempts = 0
        guessed = []
        while attempts < max_attempts:
            guess = await self.get_guess(message.author, word, guessed)
            if guess == word:
                embed = discord.Embed(title="Tebrikler, Kazandınız!", description=f"Kelime: {word}", color=0x00ff00)
                await message.channel.send(embed=embed)
                return
            elif guess in word:
                underscores = self.update_word(guess, word, underscores)
                embed = discord.Embed(title=f"Doğru Tahmin! Kelime: {underscores}", color=0x00ff00)
                await message.author.send(embed=embed)
            else:
                attempts += 1
                guessed.append(guess)
                embed = discord.Embed(title=f"Yanlış Tahmin! Kalan Hak: {max_attempts-attempts}", color=0xff0000)
                await message.author.send(embed=embed)
        embed = discord.Embed(title="Kaybettiniz!", description=f"Kelime: {word}", color=0xff0000)
        await message.channel.send(embed=embed)
            
    async def get_guess(self, user, word, guessed):
        def check(msg):
            return msg.author == user and msg.content.isalpha() and len(msg.content) == 1 and msg.content not in guessed
        message = await self.wait_for('message', check=check)
        return message.content.lower()
    
    def update_word(self, guess, word, underscores):
        new_word = ""
        for i in range(len(word)):
            if guess == word[i]:
                new_word += guess
            else:
                new_word += underscores[i]
        return new_word
