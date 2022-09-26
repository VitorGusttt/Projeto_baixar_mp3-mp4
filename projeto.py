from inspect import formatannotation
from tokenize import Name
import PySimpleGUI as sg 
from pytube import YouTube, Playlist

#importa o tema
sg.theme('DarkBlue2')

#cria a janela inicial
janela_link = [
    [sg.Text('Insira o Link aqui: '), sg.Push(), sg.Input(size=(30,1), key = 'link')],
    [sg.Push(), sg.Push(), sg.Button('Pesquisar')],
    [sg.Push(), sg.Text('', key='titulo'), sg.Push()]
]

#cria a janela secundaria
janela_Formato = [
    [sg.Text('Selecione o caminho: '), sg.Input(key = 'texto'), sg.FolderBrowse('Selecionar destino', key = 'path'), sg.Button('Ok')],
    [sg.Text('Selecione o Formato dsejado: '),sg.Push() ,sg.Button('MP3'),sg.Button('MP4'), sg.Push()],
    [sg.Push(), sg.Button('Baixar'), sg.Push()]
    

]
#juntar as 2
janela_final = [
    [sg.Column(janela_link), sg.VSeparator(), sg.Column(janela_Formato)],

]
#criando a janela
tela = sg.Window('Vitor Project', layout= janela_final, element_justification='c')

#executando ela
while True:
    #receber os valores lidos
    evento, valor = tela.read()    
    
    #fechar
    if evento == sg.WIN_CLOSED:
        break
    
    #se nao fechar pega o link assim q pesquisar for clicado
    elif evento == 'Pesquisar':
        #se nao tiver valor no link, avisa
        if valor['link'] == '':
            sg.popup('Insira um link ae')
        
        #se tiver, continua
        else:
            #vai tentar pegar o link do video solos, se for uma playlist, ele vai a playlist, para evitar erro
            try:
                linkYt = YouTube(valor['link'])
                tela['titulo'].update(linkYt.title)
                print('video')
            except:
                linkPlaylist = Playlist(valor['link'])
                tela['titulo'].update(linkPlaylist.title)
                print('playlist')
    
    #selecionar caminho
    elif evento == 'Ok':
        caminho = valor['path']
        if caminho == '':
            sg.popup('Insira um caminho')

    #formato 
    elif evento == 'MP3':
        formato = 'Mp3'

    elif evento == 'MP4':
        formato = 'Mp4'

    #baixar
    elif evento == 'Baixar':

        #se for mp4 tenta tal coisa
        if formato == 'Mp4':
            try:
                linkYt.streams.get_highest_resolution().download(caminho)
            except:
                linkPlaylist = Playlist(valor['link'])
                caminho = valor['path']
                for videos in linkPlaylist.videos:
                    videos.streams.get_highest_resolution().download(caminho)
            sg.popup('Seu Download terminou!!')

        elif formato == 'Mp3':
            try:
                linkYt.streams.get_audio_only().download(caminho)
            except:
                linkPlaylist = Playlist(valor['link'])
                caminho = valor['path']
                for videos in linkPlaylist.videos:
                    videos.streams.get_audio_only().download(caminho)
            sg.popup('Seu Download terminou!!')

tela.close()