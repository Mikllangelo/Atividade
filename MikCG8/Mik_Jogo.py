import pygame, random

# Carregando as imagens
imagemNave = pygame.image.load('nave.png')
imagemAsteroide = pygame.image.load('asteroide.png')
imagemRaio = pygame.image.load('raio.png')
imagemFundo = pygame.image.load('magellanic-clouds.png')

# Configurações da janela e variáveis do jogo
LARGURAJANELA = 600
ALTURAJANELA = 600
CORTEXTO = (255, 255, 255)
QPS = 40
TAMMINIMO = 10
TAMMAXIMO = 40
VELMINIMA = 1
VELMAXIMA = 8
ITERACOES = 6
VELJOGADOR = 5
VELRAIO = (0, -15)
LARGURANAVE = imagemNave.get_width()
ALTURANAVE = imagemNave.get_height()
LARGURARAIO = imagemRaio.get_width()
ALTURARAIO = imagemRaio.get_height()

# Função para mover o jogador
def moverJogador(jogador, teclas, dim_janela):
    borda_esquerda = 0
    borda_superior = 0
    borda_direita = dim_janela[0]
    borda_inferior = dim_janela[1]
    
    if teclas['esquerda'] and jogador['objRect'].left > borda_esquerda:
        jogador['objRect'].x -= jogador['vel']
    if teclas['direita'] and jogador['objRect'].right < borda_direita:
        jogador['objRect'].x += jogador['vel']
    if teclas['cima'] and jogador['objRect'].top > borda_superior:
        jogador['objRect'].y -= jogador['vel']
    if teclas['baixo'] and jogador['objRect'].bottom < borda_inferior:
        jogador['objRect'].y += jogador['vel']

# Função para mover elementos (raios e asteroides)
def moverElemento(elemento):
    elemento['objRect'].x += elemento['vel'][0]
    elemento['objRect'].y += elemento['vel'][1]

# Função para terminar o jogo
def terminar():
    pygame.quit()
    exit()

# Função para aguardar entrada do jogador
def aguardarEntrada():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                terminar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    terminar()
                return

# Função para colocar texto na tela
def colocarTexto(texto, fonte, janela, x, y):
    objTexto = fonte.render(texto, True, CORTEXTO)
    rectTexto = objTexto.get_rect()
    rectTexto.topleft = (x, y)
    janela.blit(objTexto, rectTexto)

# Função para verificar colisões entre raios e asteroides
def verificarColisao(raios, asteroides):
    for raio in raios[:]:
        for asteroide in asteroides[:]:
            if raio['objRect'].colliderect(asteroide['objRect']):
                raios.remove(raio)
                asteroides.remove(asteroide)
                return True  # Colisão detectada
    return False

# Função para verificar colisão entre a nave e os asteroides
def verificarColisaoNave(jogador, asteroides):
    for asteroide in asteroides:
        if jogador['objRect'].colliderect(asteroide['objRect']):
            return True  # Colisão detectada
    return False

# Inicializando o pygame e configurando a janela
pygame.init()
relogio = pygame.time.Clock()
janela = pygame.display.set_mode((LARGURAJANELA, ALTURAJANELA))
pygame.display.set_caption('Asteroides Troianos')
pygame.mouse.set_visible(False)
imagemFundoRedim = pygame.transform.scale(imagemFundo, (LARGURAJANELA, ALTURAJANELA))

# Configurando a fonte e sons
fonte = pygame.font.Font(None, 48)
somFinal = pygame.mixer.Sound('final_fx.wav')
somRecorde = pygame.mixer.Sound('record.wav')
somTiro = pygame.mixer.Sound('laser.wav')
pygame.mixer.music.load('trilha_nave.wav')

# Tela de início
colocarTexto('Asteroides Troianos', fonte, janela, LARGURAJANELA / 5, ALTURAJANELA / 3)
colocarTexto('Pressione uma tecla para começar.', fonte, janela, LARGURAJANELA / 20, ALTURAJANELA / 2)
pygame.display.update()
aguardarEntrada()

# Iniciando o jogo
recorde = 0
while True:
    asteroides = []
    raios = []
    pontuacao = 0
    deve_continuar = True
    
    teclas = {'esquerda': False, 'direita': False, 'cima': False, 'baixo': False}
    contador = 0
    pygame.mixer.music.play(-1, 0.0)
    
    posX = LARGURAJANELA / 2
    posY = ALTURAJANELA - 50
    jogador = {'objRect': pygame.Rect(posX, posY, LARGURANAVE, ALTURANAVE), 'imagem': imagemNave, 'vel': VELJOGADOR}

    while deve_continuar:
        pontuacao += 1
        if pontuacao == recorde:
            somRecorde.play()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                terminar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    terminar()
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    teclas['esquerda'] = True
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    teclas['direita'] = True
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    teclas['cima'] = True
                if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    teclas['baixo'] = True
                if evento.key == pygame.K_SPACE:
                    raio = {'objRect': pygame.Rect(jogador['objRect'].centerx, jogador['objRect'].top, LARGURARAIO, ALTURARAIO),
                            'imagem': imagemRaio, 'vel': VELRAIO}
                    raios.append(raio)
                    somTiro.play()

            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    teclas['esquerda'] = False
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    teclas['direita'] = False
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    teclas['cima'] = False
                if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    teclas['baixo'] = False

            if evento.type == pygame.MOUSEMOTION:
                centroX_jogador = jogador['objRect'].centerx
                centroY_jogador = jogador['objRect'].centery
                jogador['objRect'].move_ip(evento.pos[0] - centroX_jogador, evento.pos[1] - centroY_jogador)

            if evento.type == pygame.MOUSEBUTTONDOWN:
                raio = {'objRect': pygame.Rect(jogador['objRect'].centerx, jogador['objRect'].top, LARGURARAIO, ALTURARAIO),
                        'imagem': imagemRaio, 'vel': VELRAIO}
                raios.append(raio)
                somTiro.play()

        # Preenchendo o fundo da janela
        janela.blit(imagemFundoRedim, (0, 0))

        # Exibindo pontuação e recorde
        colocarTexto('Pontuação: ' + str(pontuacao), fonte, janela, 10, 0)
        colocarTexto('Recorde: ' + str(recorde), fonte, janela, 10, 40)

        # Adicionando asteroides
        contador += 1
        if contador >= ITERACOES:
            contador = 0
            tamAsteroide = random.randint(TAMMINIMO, TAMMAXIMO)
            posX = random.randint(0, LARGURAJANELA - tamAsteroide)
            posY = -tamAsteroide
            vel_x = random.randint(-1, 1)
            vel_y = random.randint(VELMINIMA, VELMAXIMA)
            asteroide = {'objRect': pygame.Rect(posX, posY, tamAsteroide, tamAsteroide),
                         'imagem': pygame.transform.scale(imagemAsteroide, (tamAsteroide, tamAsteroide)),
                         'vel': (vel_x, vel_y)}
            asteroides.append(asteroide)

        # Movimentando e desenhando os asteroides
        for asteroide in asteroides:
            moverElemento(asteroide)
            janela.blit(asteroide['imagem'], asteroide['objRect'])

        # Eliminando os asteroides que saem da tela
        for asteroide in asteroides[:]:
            if asteroide['objRect'].top > ALTURAJANELA:
                asteroides.remove(asteroide)

        # Movendo o jogador
        moverJogador(jogador, teclas, (LARGURAJANELA, ALTURAJANELA))
        janela.blit(jogador['imagem'], jogador['objRect'])

        # Movendo e desenhando os raios
        for raio in raios[:]:
            moverElemento(raio)
            janela.blit(raio['imagem'], raio['objRect'])

        # Verificando colisões entre raios e asteroides
        if verificarColisao(raios, asteroides):
            pontuacao += 100  # A cada colisão, ganha pontos

        # Verificando colisão entre a nave e os asteroides
        if verificarColisaoNave(jogador, asteroides):
            somFinal.play()
            colocarTexto('Fim de Jogo', fonte, janela, LARGURAJANELA / 3, ALTURAJANELA / 3)
            pygame.display.update()
            pygame.time.wait(2000)  # Espera 2 segundos antes de terminar o jogo
            deve_continuar = False

        # Atualizando o recorde
        if pontuacao > recorde:
            recorde = pontuacao

        # Atualizando a tela
        pygame.display.update()

        # Controlando o FPS
        relogio.tick(QPS)