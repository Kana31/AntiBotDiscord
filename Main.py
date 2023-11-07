
#  Anti 1.1 For Kana A.

import discord
from discord.ext import commands
import os

# Define as intenções do bot
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

# Cria uma instância do bot com intenções e um prefixo personalizado
bot = commands.Bot(command_prefix='-', intents=intents)

# Evento que ocorre quando o bot está pronto
@bot.event
async def on_ready():
    """
    Este evento é acionado quando o bot está pronto e online.
    """
    print(f'Anti está online como {bot.user.name}')



## Lista dos comandos--------------------------------------------------------------------- ##


# Comando simples para cumprimentar o autor da mensagem
@bot.command()
async def ola(ctx):
    """
    Este comando cumprimenta o autor da mensagem.
    """
    await ctx.send(f'Olá, Bostinha Chamada(o) {ctx.author.mention}! :3')

# Comando para definir o bot como sua namorada
@bot.command()
async def namoracmg(ctx):
    """
    Este comando permite definir o bot como sua namorada.
    """
    resposta = "Desculpe! Mas já tenho o meu namorado que é o Kana ❤️"
    await ctx.send(resposta)

# Comando para excluir um canal de voz com o nome especificado
@bot.command()
@commands.has_permissions(administrator=True)
async def delete(ctx, nome_canal):
    """
    Exclui um canal de voz com o nome especificado se ele existir.
    """
    guild = ctx.guild

    # Obtenha o canal de voz com o nome especificado
    channel = discord.utils.get(guild.voice_channels, name=nome_canal)

    # Verifique se o canal existe
    if channel:
        # Exclua o canal
        await channel.delete()
        await ctx.send(f'Canal de voz "{nome_canal}" excluído com sucesso!')
    else:
        # Informe ao usuário que o canal não existe
        await ctx.send(f'Não há nenhum canal de voz com o nome "{nome_canal}".')

# Comando para excluir todos os canais de voz que contenham as primeiras iniciais que o usuário dizer para o bot
@bot.command()
@commands.has_permissions(administrator=True)
async def deleteall(ctx, iniciais):
    """
    Exclui todos os canais de voz que contenham as primeiras iniciais que o usuário dizer para o bot.
    """
    guild = ctx.guild

    # Obtenha todos os canais de voz do servidor
    voice_channels = guild.voice_channels

    # Crie uma lista vazia para armazenar os nomes dos canais excluídos
    deleted_channels = []

    # Percorra todos os canais de voz
    for channel in voice_channels:
        # Verifique se o nome do canal começa com as iniciais fornecidas
        if channel.name.startswith(iniciais):
            # Adicione o nome do canal à lista de canais excluídos
            deleted_channels.append(channel.name)
            # Exclua o canal
            await channel.delete()

    # Verifique se algum canal foi excluído
    if deleted_channels:
        # Informe ao usuário quais canais foram excluídos
        await ctx.send(f'Os seguintes canais de voz foram excluídos: {", ".join(deleted_channels)}')
    else:
        # Informe ao usuário que nenhum canal foi encontrado com as iniciais fornecidas
        await ctx.send(f'Não há nenhum canal de voz que comece com "{iniciais}".')


# Adicione um comando de ajuda para listar todos os comandos disponíveis
@bot.command()
async def ajuda(ctx):
    """
    Exibe uma lista de comandos disponíveis.
    """
    help_message = "Comandos disponíveis:\n"
    for command in bot.commands:
        help_message += f"/{command.name}: {command.help}\n"
    await ctx.send(help_message)

# Comando para criar um canal de voz com o nome especificado
@bot.command()
@commands.has_permissions(administrator=True) # Verificar se o usuário tem permissão de administrador
async def canal(ctx, nome_canal):
    """
    Cria um canal de voz com o nome especificado e o bloqueia para os outros membros.
    """
    guild = ctx.guild

    # Crie um canal de voz com o nome especificado
    await guild.create_voice_channel(nome_canal)

    # Obtenha o canal recém-criado
    new_channel = discord.utils.get(guild.voice_channels, name=nome_canal)

    # Defina as permissões para bloquear o canal
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(connect=False)
    }
    await new_channel.edit(overwrites=overwrites)

    await ctx.send(f'Canal de voz "{nome_canal}" criado e bloqueado com sucesso!')

@bot.command()
@commands.has_permissions(administrator=True) # Verificar se o usuário tem permissão de administrador
async def on(ctx):
    """
    Cria um canal "Server On"
    """
    # Obter o servidor atual
    guild = ctx.guild
    # Verificar se já existe um canal de voz chamado "Server On" ou "Server Off"
    channel = discord.utils.get(guild.voice_channels, name="Server On") or discord.utils.get(guild.voice_channels, name="Server Off")
    # Se não existir, criar um novo canal de voz bloqueado chamado "Server On"
    if not channel:
        channel = await guild.create_voice_channel(name="Server On")
        await channel.set_permissions(guild.default_role, connect=False)
        await ctx.send(f"Canal de voz {channel.mention} criado com sucesso.")
    # Se existir, mas tiver o nome "Server Off", renomeá-lo para "Server On"
    elif channel.name == "Server Off":
        await channel.edit(name="Server On")
        await ctx.send(f"Canal de voz {channel.mention} renomeado com sucesso.")
    # Se existir e já tiver o nome "Server On", enviar uma mensagem de erro
    else:
        await ctx.send(f"Já existe um canal de voz {channel.mention}.")

# Definir um comando para renomear o canal de voz existente chamado "Server On" para "Server Off"
@bot.command()
@commands.has_permissions(administrator=True) # Verificar se o usuário tem permissão de administrador
async def off(ctx):

    """
    Define um Canal chamada " Server Off
    """
    # Obter o servidor atual
    guild = ctx.guild
    # Verificar se existe um canal de voz chamado "Server On"
    channel = discord.utils.get(guild.voice_channels, name="Server On")
    # Se existir, renomeá-lo para "Server Off"
    if channel:
        await channel.edit(name="Server Off")
        await ctx.send(f"Canal de voz {channel.mention} renomeado com sucesso.")
    # Se não existir, cria um novo canal de voz chamado "Server Off"
    else:
        await ctx.send("Não existe um canal de voz chamado 'Server On'.")

# Definir um tratamento de erro para quando alguém que não é um administrador tenta usar os comandos
@bot.event
async def on_command_error(ctx, error):
    # Se o erro for causado por falta de permissão de administrador, enviar uma mensagem de erro
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para usar esse comando.")
    # Caso contrário, propagar o erro
    else:
        raise error


# Tratamento de erros
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Esse comando não existe. Use /ajuda para ver os comandos disponíveis.")
    else:
        # Adicione um tratamento de erros genérico para outros tipos de erros
        await ctx.send(f"Ocorreu um erro ao executar o comando: {error}")

# Substitua o token por uma variável de ambiente
TOKENBOT = 'MTE2Nzk3NDcwODM3ODA5NTcyNg.GiyLKG.PvQdIW8vm_7fhknBoDrsCyUh6jyCFHiUn-ptkI'
if TOKENBOT:
    bot.run(TOKENBOT)
else:
    print("Token não encontrado. Verifique se você configurou a variável de ambiente DISCORD_BOT_TOKEN.")
