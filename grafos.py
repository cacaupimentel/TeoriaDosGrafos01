#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from tkinter import *
from tkinter import filedialog
from collections import defaultdict  # Estratégico p/redimensionar a qnt vertices
import networkx as ntw
import matplotlib.pyplot as matplt


# Para criar um executável
# pip install networkx
# pip install matplotlib


# Procedimentos de instalação
# pip install cx_Freeze
# cxfreeze grafos.py --target-dir c:\grafos


# *******************************************************
# *******  TrabalhaR com Lista de Adjacências  **********
# *******************************************************
# ****************** CLASSE GRAFO ***********************
# *******************************************************


class Grafo(object):

    # Construtor do Objeto Grafo
    def __init__(self):
        self.grafo = defaultdict(set)
        # Dicionáfio para criar Gráfico
        self.dictgrafico = defaultdict(set)
        self.direcao = False
        self.vertices = []
        self.arestas = []
        # Lista de vizinhos
        self.lstvisitados = []
        # Cria um dicionario combinando Todos os vertices não visitados com a marcação 'N', case
        self.naovisitados = {}
        # Criado para teste depois apagar
        self.qntvert = 0

    # -------------------------------------------------------------
    def setDirecao(self, direcao):
        # Redimensiona a lista de vertices
        # self.vertice = defaultdict(set)
        # Se o arquivo for "D"=direcionado, "ND"=Não direcionado
        # O arquivo pode ter tanto grafos direcionados quanto não direcionados
        if isEqual('nd', direcao.lower()):
            self.direcao = False
            print("Tipo Não Direcionado")
        else:
            self.direcao = True
            print("Tipo Direcionado")

    # -------------------------------------------------------------
    def addVertices(self, v):
        # Se não achou
        if not existinlista(v, self.vertices):
            self.vertices.append(v)
        # Ordena
        # self.vertices.sort()

    # -------------------------------------------------------------
    def addAresta(self, vrtini, vrtfim):
        # flag achou a Key v1
        flkey = True
        flkeynd = True
        # Inclui vertices na lista de vertices
        self.addVertices(vrtini)
        self.addVertices(vrtfim)
        # Inclui a lista de arestas
        self.arestas.append([vrtini, vrtfim])
        print(" ")
        print("addArestas: ", vrtini, ",", vrtfim)
        print("---------------------------------------------------------------")
        # procura se v1 ja existir inclui v2 em v1
        for key, value in self.grafo.items():
            print("loop Key: ", key)
            # Se achou vamos incluir na mesma chave
            print("D isEqual ", vrtini, "=", key, isEqual(vrtini, key))
            # if vrtini  key:
            if isEqual(vrtini, key):
                flkey = False
                # pega a lista que está em value
                list_value = value
                print("D Value atual: ", list_value)
                # adiciona a lista de value
                list_value.append(vrtfim)
                print('Add D ', vrtfim, " in key ", vrtini, " = key:", vrtini, list_value)
                # self.grafo.update(dict.fromkeys(vrtini, list_value))
                self.grafo[vrtini] = list_value
                # self.grafo.update(dict.fromkeys(vrtini, list_value))

            # se for não direcionado inverter as chaves
            if not self.direcao:
                print("ND isEqual ", vrtfim, "=", key, isEqual(vrtfim, key))
                if isEqual(vrtfim, key):
                    flkeynd = False
                    # pega a lista que está em value
                    list_valueND = value
                    print("ND Value atual: ", list_valueND)
                    # adiciona a lista de value
                    list_valueND.append(vrtini)
                    self.grafo[vrtfim] = list_valueND
                    print('Add ND Value', vrtini, " in key ", vrtfim, list_valueND)
                    # self.grafo.update(dict.fromkeys(vrtfim, list_valueND))

        # Se não achou inclui a key pela primeira vez
        if flkey:
            print('Insert D key: ', vrtini, "[", vrtfim, "]")
            # self.grafo.update(dict.fromkeys(vrtini, [vrtfim]))
            self.grafo[vrtini] = [vrtfim]

        # Se não achou inclui a key pela primeira vez
        if not self.direcao:
            if flkeynd:
                print('Insert ND key: ', vrtfim, "[", vrtini, "]")
                # elf.grafo.update(dict.fromkeys(vrtfim, [vrtini]))
                self.grafo[vrtfim] = [vrtini]

    # -------------------------------------------------------------
    def list_vertes(self):
        print("List de vertices")
        print(self.vertices)

    # -------------------------------------------------------------
    def imprime_obj(self):
        print("List Arestas")
        print(self.grafo)

    # -------------------------------------------------------------
    def getVertices(self):
        return self.vertices

    # -------------------------------------------------------------
    def getArestas(self):
        return self.arestas

    # -------------------------------------------------------------
    def getdictgrafico(self):
        for key, value in self.grafo.items():
            self.dictgrafico[key] = tuple(value)
        print(self.dictgrafico)
        return self.dictgrafico

    # -------------------------------------------------------------
    def getadjacentes(self, a, b):
        # Testa se são Adjacentes
        adj = False
        # Pega primeiro como chave  os adjacentes
        ad = self.grafo.get(a)
        if ad:
            # Procura nos adjacentes
            for x in self.grafo.get(a):
                if isEqual(b, x):
                    adj = True
        else:
            # Se não chomo chave, procurar nos adjacentes caso dirigido
            if self.direcao:
                # varrer todos adjacentes
                for key, value in self.grafo.items():
                    # Vamos inverter a chave para b para procurar a
                    if isEqual(b, key):
                        # varre o grupo iterno de adjacentes
                        for z in value:
                            # procurar a chave a nos items adjacentes
                            if isEqual(a, z):
                                adj = True
                                break
        return adj

    # -------------------------------------------------------------
    def getgrauentrada(self, v):
        # Grau o numero de vertices adjacentes
        grau = 0
        # varre os adjacentes todos
        for key, value in self.grafo.items():
            # conta adjacentes em v
            for y in value:
                if isEqual(v, y):
                    grau += 1
        return grau

    # -------------------------------------------------------------
    def getGrauSaida(self, v):
        # Grau o numero de vertices adjacentes
        grau = 0
        # retorna os adjacentes de v
        adjs = self.grafo.get(v)
        if adjs:
            grau = len(adjs)
        return grau

    # -------------------------------------------------------------
    def getVizinhos(self, v):
        # Lista de vizinhos
        listV = []
        # Pega os adjacentes
        # Pega primeiro como chave
        ad = self.grafo.get(v)
        if ad:
            # se achou como chave adiciona a lista de adjacentes
            listV = ad
        # Se direcionado, continuar adicionando na lista onde existir
        if self.direcao:
            # varrer todos adjacentes e achar adiciona a chave
            for key, value in self.grafo.items():
                # Vamos inverter a chave para b para procurar a
                for t in value:
                    # procura v está como adjacente de outra chave
                    if isEqual(v, t):
                        # se encontrou a chave é o que interessa, checar
                        # se ela ja existe na lista, se não, inclui
                        if not existinlista(str(key), listV):
                            listV.append(key)
        return listV

    # -------------------------------------------------------------
    def visitaprofundidade(self, prof):

        # Contagem de teste
        self.qntvert += 1
        print(str(self.qntvert) + "visitaprofundidade ", str(prof))

        # Testa se os vertices em p no dicioario nao foram Visitados
        if keyvisitado(prof, self.naovisitados):
            print(str(self.qntvert) + "Volta já visitado ", str(prof))
            return

        else:
            # Marca como visitado
            self.naovisitados[prof] = "V"
            # self.naovisitados.update(dict.fromkeys(prof, "V"))
            # Se não foi visitado, procura se ja está na lista, se não adiciona
            if not existinlista(prof, self.lstvisitados):
                # Adiciona a lista de visitados
                self.lstvisitados.append(prof)

            # condição de retorno, se não achar a key, retorna sem entrar no laço
            adjProf = self.grafo.get(prof)
            print(str(self.qntvert) + "Adjacentes vertice " + str(prof), adjProf)
            # Se tem key(vertice) varre os adjacetes
            if adjProf:
                # Checar os adjacentes do vertice Prof
                for adp in adjProf:
                    # Testa se os vertices em p no dicioario nao foram Visitados
                    if not keyvisitado(adp, self.naovisitados):
                        print(str(self.qntvert) + "Visita Vizinho de " + str(prof) + ": ", adp)
                        # Chama a função recursiva
                        self.visitaprofundidade(adp)
            else:
                print(str(self.qntvert) + "Volta não achou chave ", str(prof))
                return

    # -------------------------------------------------------------
    def visitaArestas(self):
        # Lista de profundidade

        # Lista de vizinhos
        self.lstvisitados = []

        # Cria um dicionario combinando Todos os vertices não visitados com a marcação 'N', case
        self.naovisitados = dict(zip(self.vertices, ['N' for h in range(len(self.vertices))]))

        print(self.naovisitados)
        print("Objeto Grafo")
        self.imprime_obj()
        # Varre os vertices
        for key, value in self.grafo.items():

            # Testa se os vertices em Key no dicioario naovisitados
            if not keyvisitado(key, self.naovisitados):

                # Se não foi visitado, procura se ja está na lista, se não adiciona
                if not existinlista(key, self.lstvisitados):

                    # Joga a key na Lista
                    self.lstvisitados.append(key)

                    # Marcar no dicionario que a Key correspondente ao vertice foi visitado
                    self.naovisitados[key] = "V"
                    # self.naovisitados.update(dict.fromkeys(key, "V"))

                    # Contagem de teste
                    self.qntvert += 1
                    print(str(self.qntvert) + " Visita chave ", str(key))
                    # Varrer os adjacentes
                    for p in value:
                        # Testa se os vertices em p no dicioario nao foram Visitados
                        if not keyvisitado(p, self.naovisitados):
                            # Deixa para marcar como visitado na função
                            # Contagem de teste
                            self.qntvert += 1
                            print(str(self.qntvert) + " Vvizinho de " + str(key) + " na fun: ", str(p))
                            # Acha p como chave e testa todos recursivamente
                            self.visitaprofundidade(p)

        print(self.naovisitados)
        print("FIM Visita")

        return self.lstvisitados

    # o dicionário precisa refletir uma lista de adjacencias
        # DictGrafo = {"1": ["2"],
        #              "2": ["3", "4"],
        #              "3": ["2", "5"],
        #              "4": ["1"],
        #              '5': ['2']}

    def getGrafoFiltrado(self):

        # Dicionario de retorno
        dicRet = dict([])

        # retorna o grafo filtrando caracteres e transformando tudo em inteiro
        for key, value in self.grafo.items():
            # Limpa caracteres da key
            k = int(re.sub('[^0-9]', '', key))
            # cria uma lista para filtras os caracteres dos valores
            vl_lst = []
            #  Varre valores e filtra oscaractes
            for x in value:
                a = int(re.sub('[^0-9]', '', x))    
                vl_lst.append(a)

            # Adiciona os novos key e valores
            dicRet[k] = vl_lst

        return dicRet

# Fim
# *******************************************************
# **************** FIM CLASSE GRAFO *********************


# Define o objeto de forma global
objgrafo = Grafo()
graficoobj = Grafo()
# Demais Variáveis
garqgrafo = None
garqplot = None
# Instancianado o tkinter
initela = Tk()
framini = Frame()
framtela = Frame()
tvert_frm = Frame()
lst_frame = Frame()
lst_adj_frm = Frame()
visita_frm = Frame()
framexerc = Frame()
vert_adj_frm = Frame()
grau_vert_frm = Frame()
vizi_vert_frm = Frame()
frm_grafico = Frame()
frm_msggra = Frame()
list_adj_frm = Listbox()
txt_frame = Entry()
txt_visita = Entry()
txt_veradj_ini = Entry()
txt_veradj_fim = Entry()
txt_tdvvertices = Entry()
txt_grauver_in = Entry()
txt_viziver_in = Entry()
txt_grafico = Entry()
mostraarplot = StringVar()


# *******************************************************
# ************* MANIPULANDO GRÁFICO *********************
# *******************************************************


def ler_arq_tipo_grafico():
    global frm_msggra
    # fonte de leitura https://diegomariano.com/networkx/
    # Verifica se o arquivo não foi digitado e chama
    grfile = filedialog.askopenfilename(initialdir="./",
                                        title="Abrir Arquivo Gráfico",
                                        filetypes=(("Todos", "*.*"),
                                                   ("Texto", "*.csv")))
    if grfile is not None:
        # Cria uma mensagem na tel para informar qual arquivo escolheu
        # cria_msng(frm_msggra, "Arquivo Gráfico plotado: " + grfile, 0, 3)
        mostraarplot.set("Arquivo Gráfico plotado: " + grfile)
        # ler com a própria biblioteca
        arqgrafico = ntw.read_edgelist(grfile, delimiter=",")
        # plota o grafo
        ntw.draw(arqgrafico, with_labels=True, node_size=1000)
        matplt.show()


def abre_arqgrafico():
    print("abre o arquivo do grafico")
    global txt_grafico
    global garqplot
    global graficoobj

    graficoobj = Grafo()
    txt_grafico.delete(0, END)
    # Verifica se o arquivo não foi digitado e chama
    garqplot = filedialog.askopenfilename(initialdir="./",
                                          title="Abrir Arquivo Gráfico",
                                          filetypes=(("Todos", "*.*"),
                                                     ("Texto", "*.csv")))
    txt_grafico.insert(0, garqplot)

    # Joga para um objeto grafo
    ler_arq_grafico(frm_grafico)


def ler_arq_grafico(tela):

    global garqplot
    global graficoobj
    print("02-Lendo Arq Gráfico ", garqplot)
    stipografo = ""
    qntlin = 0

    # Verifica se o Arquivo existe
    if os.path.isfile(garqplot):
        # Faz a leitura do arquivo para a estrutura
        garq = open(garqplot, "r")
        # Lendo o arquivo
        for linha in garq:
            # Limpa a linha
            glimlinha = " ()[] \n "
            glimlinha = ''.join(filter(lambda sl: sl not in glimlinha, linha))
            print("Linha limpa", glimlinha)
            # Se for Primeira linha guarda ND
            if qntlin > 0:
                # Cada linha é uma aresta com 2 vértices e
                lstval = glimlinha.split(",")
                print(lstval[0], lstval[1])
                graficoobj.addAresta(lstval[0], lstval[1])

            else:
                stipografo = glimlinha
                graficoobj.setDirecao(stipografo)
                print("Tipo: ", str(stipografo))

            qntlin += 1
            print("Qnt. ", str(qntlin))
            print("Limpo ", glimlinha)
            print("Sujo ", linha)
    else:
        cria_msng(tela, "Arquivo não encontrado!", 1, 3)


def salva_grafico():
    print("salva o layout do grafico em arquivo")
    # gravando um grafo como arquivo csv
    # fonte de leitura https://diegomariano.com/networkx/
    global graficoobj
    global garqplot

    if graficoobj.direcao:
        pgr = ntw.DiGraph()
    else:
        pgr = ntw.Graph()

    # nome do arquivo
    nomegraf = garqplot[:-3] + "_layout_gafro.csv"
    # separador
    gsep = ","
    # se True, grava dados do peso das arestas
    gpeso = False
    # codificação
    gcoding = 'utf-8'

    ntw.write_edgelist(pgr, nomegraf, delimiter=gsep, data=gpeso, encoding=gcoding)

    # Mostra onde foi salvo o arquivo do
    mostraarplot.set("Arquivo Layout salvo em: " + nomegraf)


def plotgraficoGrafo():

    global graficoobj

    if graficoobj.direcao:
        plotgraficoGrafoD()
    else:
        plotgraficoGrafoND()


def plotgraficoGrafoND():

    global graficoobj

    grfimp = ntw.Graph()

    # Adiciona vértices
    print(graficoobj.getVertices())

    for g in graficoobj.getArestas():
        # expressão regular com numero
        a = int(re.sub('[^0-9]', '', g[0]))
        b = int(re.sub('[^0-9]', '', g[1]))
        grfimp.add_edge(a, b)

    options = {
        "font_size": 12,
        "node_size": 1000,
        "node_color": "white",
        "edgecolors": "black",
        "with_labels": True,
        "linewidths": 2,
        "width": 2,
    }

    ntw.draw_networkx(grfimp, pos=ntw.spring_layout(grfimp), **options)

    # Set margins for the axes so that nodes aren't clipped
    # Tipo de eixo para grafos 
    ax = matplt.gca()
    # Distancia dos grafos
    ax.margins(0.20)
    # # Tiras os eixos do grafos
    matplt.axis("off")
    matplt.show()


def plotgraficoGrafoD():

    global graficoobj

    # Adiciona vértices
    dictNodes = []
    for g in graficoobj.getArestas():
        # expressão regular com numero
        a = int(re.sub('[^0-9]', '', g[0]))
        b = int(re.sub('[^0-9]', '', g[1]))

        dictNodes.append((a, b))

    print(dictNodes)

    grfimpress = ntw.DiGraph(dictNodes)

    # G = ntw.DiGraph([(0, 3), (1, 3), (2, 4), (3, 5), (3, 6), (4, 6), (5, 6)])

    # group nodes by column
    # Grau = 1

    dicGraf = graficoobj.getGrafoFiltrado()
    print("grafo passado") 
    left_nodes = grauList("l", dicGraf)  # [0, 1, 2]
    # Grau = 4, 3
    middle_nodes = grauList("m", dicGraf)  # [3, 4]
    # Grau = 2
    right_nodes = grauList("r", dicGraf)  # [5, 6]

    # set the position according to column (x-coord)
    pos = {n: (0, i) for i, n in enumerate(left_nodes)}
    pos.update({n: (1, i + 0.5) for i, n in enumerate(middle_nodes)})
    pos.update({n: (2, i + 0.5) for i, n in enumerate(right_nodes)})

    # No final fica assim
    # print("[(0, 3), (1, 3), (2, 4), (3, 5), (3, 6), (4, 6), (5, 6)")
    # pos = dict({0: (0, 0), 1: (0, 1), 2: (0, 2), 3: (1, 0.5), 4: (1, 1.5), 5: (2, 0.5), 6: (2, 1.5)})
    #           {0: (0, 0), 1: (0, 1), 2: (0, 2), 3: (1, 0.5), 4: (1, 1.5), 5: (2, 0.5), 6: (2, 1.5)}

    print(pos)

    options = {
        "font_size": 12,
        "node_size": 700,
        "arrowstyle": "->",
        "arrowsize": 10,
        "node_color": "white",
        "edgecolors": "black",
        "with_labels": True,
        "linewidths": 2,
        "width": 2,
    }

    ntw.draw_networkx(grfimpress, pos=ntw.spring_layout(grfimpress), **options)

    # Set margins for the axes so that nodes aren't clipped
    # Tipo de eixo para grafos
    ax = matplt.gca()
    # Distancia dos grafos
    ax.margins(0.05)
    # Tiras os eixos do grafos
    matplt.axis("off")
    matplt.show()


def grauList(t, d):
    # Dicionario com grau de entrada e saida
    di_Sai_Ent = dict([])

    # Dicionario de somas de entradas e saidas

    # Varre o objeto
    for key, value in d.items():
        # print(key, value)

        saidas = len(value)
        entradas = 0
        total = entradas + saidas

        # testa se a chave ja existe
        tmp = di_Sai_Ent.get(int(key))
        if tmp:
            # print(" Achou key", key, tmp)
            saidas = saidas + tmp[0]
            entradas = entradas + tmp[1]
            total = entradas + saidas

        # Adiciona o key: [entrada = 1, saida = 0]
        di_Sai_Ent[int(key)] = [saidas, entradas, total]
        # print(" - add key", key,[saidas, entradas, total] )

        # Adiciona uma chave como saida =1  para cada entrada de Key
        for x in value:

            saidas = 0
            entradas = 1
            total = entradas + saidas

            # testa se a chave ja existe
            tmp = di_Sai_Ent.get(int(x))
            if tmp:
                # print(" - Achou sub key", x , tmp)
                saidas = saidas + tmp[0]
                entradas = entradas + tmp[1]
                total = entradas + saidas

            # Para cada valor em value adiciona como Key com 1 emtrada e 0 saida
            di_Sai_Ent[int(x)] = [saidas, entradas, total]
            # print("   - add sub key", x,[saidas, entradas, total] )

    print(di_Sai_Ent)

    # Agrupa por totais
    lstMiddle = []
    lstLeft = []
    lstRight = []

    # S[0] e E[1]
    # Seáração de quem tem entras e saida ficam no meio
    # Quem tem somente saidas ficam a esquerda
    # quem tem entras e saidas zeradas ficam para direita
    for key, value in di_Sai_Ent.items():

        # Testa quem tem entras e saidas para ficar no meio
        if int(value[0]) > 0 and int(value[1]) > 0:
            # incluir chave no lista middle
            lstMiddle.append(int(key))


        # Testa tem saidas = 0  fica adireita
        if isEqual(int(value[0]), 0):
            # incluir chave no lista middle
            lstRight.append(int(key))


        # Testa quem tem entradas = 0 fica para esquerda
        if isEqual(int(value[1]), 0):
            # incluir chave no lista middle
            lstLeft.append(int(key))


    print("Middle", lstMiddle)
    print("Left", lstLeft)
    print("Right", lstRight)

    lstRet = []
    if isEqual(t, "m"):
        lstRet = lstMiddle
    if isEqual(t, "r"):
        lstRet = lstRight
    if isEqual(t, "l"):
        lstRet = lstLeft

    return lstRet


# *******************************************************
# ****************** FIM GRÁFICO ************************
# *******************************************************
# *******************************************************
# ************* MANIPULANDO ARQUIVO *********************
# *******************************************************


def limpa_objetos():
    global objgrafo
    global graficoobj
    global garqgrafo
    global garqplot
    global initela
    global list_adj_frm
    global txt_frame
    global txt_veradj_ini
    global txt_veradj_fim
    global txt_grauver_in
    global txt_viziver_in
    global txt_tdvvertices
    global txt_grauver_in
    global txt_viziver_in
    global txt_grafico
    global mostraarplot
    # Instancia
    objgrafo = Grafo()
    graficoobj = Grafo()

    # Demais Variáveis
    garqgrafo = None
    garqplot = None

    # Precisa limpar os objetos da tela
    list_adj_frm.delete(0, END)
    txt_frame.delete(0, END)
    txt_veradj_ini.delete(0, END)
    txt_veradj_fim.delete(0, END)
    txt_grauver_in.delete(0, END)
    txt_viziver_in.delete(0, END)
    txt_tdvvertices.delete(0, END)
    txt_grauver_in.delete(0, END)
    txt_viziver_in.delete(0, END)
    txt_grafico.delete(0, END)
    mostraarplot.set("")


def abre_arquivo():

    global txt_frame

    nfile = filedialog.askopenfilename(initialdir="./",
                                       title="Abrir Arquivo",
                                       filetypes=(("Todos", "*.*"),
                                                  ("Texto", "*.txt")))
    # Precisa limpar os objetos
    limpa_objetos()

    if nfile == "":
        cria_msng(framtela, "Escolha um arquivo!", 0, 1)
    else:
        txt_frame.insert(0, nfile)
        print("01-Abriu Arq ", nfile)
        ler_arquivo(framtela, nfile)


def ler_arquivo(tela, n_arq):
    nrq = None
    print("02-Lendo Arq ", n_arq)
    global garqgrafo
    global objgrafo
    stipografo = ""
    qntlin = 0

    # Verifica se o Arquivo existe
    if os.path.isfile(n_arq):
        # Faz a leitura do arquivo para a estrutura
        garqgrafo = open(n_arq, "r")
        # Lendo o arquivo
        for linha in garqgrafo:
            # Limpa a linha
            slimlinha = " ()[] \n "
            slimlinha = ''.join(filter(lambda sl: sl not in slimlinha, linha))
            print("slimlinha")
            # Se for Primeira linha guarda ND
            if qntlin > 0:
                # Cada linha é uma aresta com 2 vértices e
                lstval = slimlinha.split(",")
                print(lstval[0], lstval[1])
                objgrafo.addAresta(lstval[0], lstval[1])

            else:
                stipografo = slimlinha
                objgrafo.setDirecao(stipografo)
                print("Tipo: ", str(stipografo))

            qntlin += 1
            print("Qnt. ", str(qntlin))
            print("Limpo ", slimlinha)
            print("Sujo ", linha)
    else:
        cria_msng(tela, "Arquivo não encontrado!", 1, 3)

    # Mostra na tela
    mostra_estruturaarq()
    print("FIM Leitura ")
    return nrq


def mostra_estruturaarq():
    # vai no objeto e pega linha a linha
    if objgrafo.direcao:
        stipo = "GRAFO DIRECIONADO"
    else:
        stipo = "GRAFO NÃO DIRECIONADO"

    print(objgrafo.direcao)
    # Coloca mensagem na tela do Frame
    cria_msng(lst_frame, stipo, 1, 2, 150)

    # Mostra todos os vértices do Grago
    todosverticestela()

    # Mostra a visita a todos os vértices em profundidade
    visitavertprofund()

    for key, velue in objgrafo.grafo.items():
        strmost = str(key) + " : " + str(velue)
        print(key, velue)
        list_adj_frm.insert(END, strmost.replace("'", "").replace('"', ""))


# Fução para criar uma mensagem na tela
def cria_msng(telmae, smsn, nrow, ncol, nwdt=120):
    omsn = Message(telmae,
                   text=smsn,
                   width=nwdt)

    omsn.grid(row=nrow, columnspan=ncol, sticky='we')


# Função verifica se o vertice foi visitado
def keyvisitado(kviz, dicviz):
    # Flag
    flvisitado = True

    # Pega no dicionario a chave
    valor = dicviz.get(kviz)
    if isEqual('N',  valor):
        flvisitado = False

    return flvisitado


# Função para procurar se ja existe item na lista
def existinlista(it, lst):
    achou = False
    # Procurar se o vertice ja existe
    for fnd in lst:
        if isEqual(it, fnd):
            achou = True
            break

    return achou


# Função para verificar se dois vértices são adjacentes garqgrafo
def vert_adjacentes():
    print("Adjacentes")
    # Captura os vértices digitados
    vrtum = txt_veradj_ini.get()
    vrtdois = txt_veradj_fim.get()

    # Verifica se os vértices estão preenchidos
    if (vrtum == "") and (vrtdois == ""):
        smsgm = "Digite os vértices!"
    elif garqgrafo is None:
        smsgm = "Arquivo não escolhido!"
    else:
        # verifica no objeto se são
        if objgrafo.getadjacentes(vrtum, vrtdois):
            smsgm = str(vrtum) + " e " + str(vrtdois) + " SÃO adjacentes"
        else:
            smsgm = str(vrtum) + " e " + str(vrtdois) + " NÃO SÃO adjacentes"

    # Coloca mensagem na tela do Frame
    cria_msng(vert_adj_frm, smsgm, 2, 4, 150)
    print(objgrafo.getadjacentes(vrtum, vrtdois))


def grau_vertices():

    grvert = txt_grauver_in.get()
    msggrau = ""
    # Verifica se foi digitado um vértice
    if garqgrafo is None:
        msggrau = "Arquivo não escolhido!"
    elif grvert == "":
        msggrau = "Digite um vértice!"
    else:
        grauentra = objgrafo.getgrauentrada(grvert)
        print("Grau Vértice", grauentra)
        msggrau = "Grau Vértice " + str(grvert) + " é " + str(grauentra)
        # Verifica se a direção
        if objgrafo.direcao:
            grausaida = objgrafo.getGrauSaida(grvert)
            msggrau = "Grau Vértice " + str(grvert) + " é " + str(grauentra + grausaida) + \
                      " de Entrada " + str(grauentra) + " e de Saída " + str(grausaida)
            print("Grau de Saida", grausaida)

    # imprime na tela
    cria_msng(grau_vert_frm, msggrau, 2, 3)
    print(msggrau)


def vizinho_vertices():
    print("Vizinhos do Vertice")
    vrtviz = txt_viziver_in.get()
    lstvizi = ""
    if vrtviz == "":
        lstvizi = "Digite um vértice!"
    elif garqgrafo is None:
        lstvizi = "Arquivos não escolhido!"
    else:
        # Formata para string
        lstvz = objgrafo.getVizinhos(vrtviz)
        lstvizi = "( "
        bflag = True
        for viz in lstvz:
            if bflag:
                lstvizi += str(viz)
                bflag = False
            else:
                lstvizi += ", " + str(viz)
        lstvizi += " )"

    # imprime na tela
    cria_msng(vizi_vert_frm, lstvizi, 2, 2)
    print(lstvizi)


# Funçao de comparação de strings
def isEqual(a, b):
    # Premissa de que sejam iguais
    igual = True

    # Primeiro obtem tamanhos
    a = str(a)
    b = str(b)

    lena = len(a)
    lenb = len(b)
    if lena > lenb or lenb > lena:
        igual = False

    # print('len a', lenA)
    # print('len b', lenB)
    # se passo dos comandos testar
    if igual:
        # ja que os tamanhos são iguais vamos verrer caracter
        # por caracter pelo tamnho de A
        for i in range(lena):
            # print(a[i:i+1], " = ", b[i:i+1])
            if a[i:i+1] != b[i:i+1]:
                # print("Diferente")
                igual = False
                break

    return igual


def visitavertprofund():
    print("Visitados em Profundidade")
    lstvisita = objgrafo.visitaArestas()
    # Formata para uma string
    strlstvisit = "( "
    bflag = True
    for viz in lstvisita:
        if bflag:
            strlstvisit += str(viz)
            bflag = False
        else:
            strlstvisit += ", " + str(viz)

    strlstvisit += " )"

    # imprime na tela
    txt_visita.insert(0, strlstvisit)
    # cria_msng(visita_frm, strlstvisit, 1, 3, 250)
    print(lstvisita)


def todosverticestela():
    print("Lista Todos os Vértices")
    lstvert = objgrafo.getVertices()
    # Formata para uma string
    strlstvert = "( "
    bflag = True
    for viz in lstvert:
        if bflag:
            strlstvert += str(viz)
            bflag = False
        else:
            strlstvert += ", " + str(viz)

    strlstvert += " )"

    # imprime na tela
    txt_tdvvertices.insert(0, strlstvert)
    # cria_msng(tvert_frm, strlstvert, 1, 3, 250)
    print(strlstvert)


# Fim
# *******************************************************
# ******************* FIM ARQUIVO ***********************
# *******************************************************
# ****************** USANDO MENU ************************
# *******************************************************
# Frame herda o construtor da class Frame que é um dict
# o Frame herda do Widget que herda BaseWidget
# Já possui um método destroy em BaseWidget
# Pode-se definir as propriedades: background, bd, bg, borderwidth,
# class, colormap, container, cursor, height, highlightbackground,
# highlightcolor, highlightthickness, relief, takefocus, visual,
# height, width


def primeiro_frame(nborda):
    global framini
    framini = Frame(initela, height=50, width=250, bd=nborda, relief=SOLID, padx=7, pady=7)
    lblinicial = Label(framini, text="MATRIZES ADJACENTES", fg="#aaaaaa", font="Arial 13 bold")
    lblinicial.pack(side='top')
    framini.grid(row=0, columnspan=2, sticky='we')


def segundo_frame(nbord, nbordint):
    global framtela
    global txt_frame
    global lst_frame
    global lst_adj_frm
    global list_adj_frm
    framtela = Frame(initela, height=350, width=250, bd=nbord, relief=SOLID, padx=7, pady=7)
    # Cria os principais componente
    lbl_frame = Label(framtela, text="Arquivo: ")
    txt_frame = Entry(framtela, width=110)
    bnt = Button(framtela, text="Abrir", command=lambda: abre_arquivo())
    # Desenho dos objetos no Frame
    lbl_frame.grid(row=0, column=0)
    txt_frame.grid(row=0, column=1)
    bnt.grid(row=0, column=2)
    # coloca o foco no text
    txt_frame.focus()

    # Cria frame para mostra a lista de adjacência lida do arquivo
    lst_frame = Frame(framtela, height=150, width=250, bd=nbordint, relief=SOLID)
    # Cria um label para informar a leitura
    lbl_lst_fr = Label(lst_frame, text="Estrutura de Dados (Lista Adjacência)")
    # Desenho dos objetos no Frame
    lbl_lst_fr.grid(row=0, column=0)
    # Desenha
    lst_frame.grid(row=1, columnspan=2, sticky='we')

    # Cria frame para a lista de adjacência lida do arquivo
    lst_adj_frm = Frame(framtela, height=150, width=250, bd=nbordint, relief=SOLID)
    # Inclui um texto para a lista de adjacência
    list_adj_frm = Listbox(lst_adj_frm, width=115)
    # Desenho dos objetos no Frame
    list_adj_frm.grid(row=1, column=2)
    # Desenha
    lst_adj_frm.grid(row=2, columnspan=2, sticky='we')

    # Desenha
    framtela.grid(row=1, column=0)


def terceiro_frame(nborda):
    global tvert_frm
    global txt_tdvvertices
    # Apresentar Todos os Vértices do Grafo
    # Cria frame para a lista os vértices lida do arquivo
    tvert_frm = Frame(initela, height=150, width=250, bd=nborda, relief=SOLID, padx=3, pady=3)
    # Inclui um texto para a lista de adjacência
    lbl_tvert = Label(tvert_frm, text="Lista de todos os Vértices do Grafo: ")
    txt_tdvvertices = Entry(tvert_frm, width=125)
    # lbl_tvertni = Label(tvert_frm, text=" ")
    # Desenho dos objetos no Frame
    lbl_tvert.grid(row=0, columnspan=3, sticky='we')
    # lbl_tvertni.grid(row=2, column=0)
    txt_tdvvertices.grid(row=1, columnspan=3, sticky='we')
    # Desenha
    tvert_frm.grid(row=2, columnspan=3, sticky='we')


def quarto_frame(nbord):
    global visita_frm
    global txt_visita
    # Apresentar a visita a todas a todas as arestas
    # Cria frame para a lista de adjacência lida do arquivo
    visita_frm = Frame(initela, height=150, width=250, bd=nbord, relief=SOLID, padx=3, pady=3)
    # Inclui um texto para a lista de adjacência
    lbl_visita = Label(visita_frm, text="Visita os Vértices em Profundidade: ")
    txt_visita = Entry(visita_frm, width=125)
    # lbl_visitani = Label(visita_frm, text=" ")
    # Desenho dos objetos no Frame
    lbl_visita.grid(row=0, columnspan=3, sticky='we')
    # lbl_visitani.grid(row=1, column=0)
    txt_visita.grid(row=2,  columnspan=3, sticky='we')
    # Desenha
    visita_frm.grid(row=3, columnspan=3, sticky='we')


def quinto_frame(nborda, nbordint):
    global framexerc
    global vert_adj_frm
    global txt_veradj_ini
    global txt_veradj_fim
    global grau_vert_frm
    global txt_grauver_in
    global vizi_vert_frm
    global txt_viziver_in
    framexerc = Frame(initela, height=350, width=250, bd=nborda, relief=SOLID, padx=7, pady=7)
    # Cria frame p/verificar adjacência de 2 vértices
    vert_adj_frm = Frame(framexerc, height=150, width=150, bd=nbordint, relief=SOLID, padx=5, pady=5)
    # Inclui um texto para a lista de adjacência
    lbl_veradj = Label(vert_adj_frm, text="Verificar se dois Vértices são Adjacentes")
    lbl_veradj_ini = Label(vert_adj_frm, text="Vértices 01:")
    txt_veradj_ini = Entry(vert_adj_frm, width=5)
    lbl_veradj_fim = Label(vert_adj_frm, text="Vértices 02:")
    txt_veradj_fim = Entry(vert_adj_frm, width=5)
    # lbl_veradjin = Label(vert_adj_frm, text=" ")
    bnt_veradj = Button(vert_adj_frm, text="Verificar", command=lambda: vert_adjacentes())
    # Desenho dos objetos no Frame
    lbl_veradj.grid(row=0, columnspan=4, sticky='we')
    lbl_veradj_ini.grid(row=1, column=0)
    txt_veradj_ini.grid(row=1, column=1)
    lbl_veradj_fim.grid(row=1, column=2)
    txt_veradj_fim.grid(row=1, column=3)
    # lbl_veradjin.grid(row=2, column=0)
    bnt_veradj.grid(row=1, column=4)
    # Desenha
    vert_adj_frm.grid(row=0, column=0)

    # Cria frame p/verificar adjacência de 2 vértices
    grau_vert_frm = Frame(framexerc, height=150, width=110, bd=nbordint, relief=SOLID, padx=10, pady=10)
    # Inclui um texto para a lista de adjacência
    lbl_grauver = Label(grau_vert_frm, text="Calcular o Grau de um Vértice")
    lbl_grauver_in = Label(grau_vert_frm, text="Vértices:")
    txt_grauver_in = Entry(grau_vert_frm, width=5)
    # lbl_grauverin = Label(grau_vert_frm, text=" ")
    bnt_grauver = Button(grau_vert_frm, text="Calcular", command=lambda: grau_vertices())
    # Desenho dos objetos no Frame
    lbl_grauver.grid(row=0, columnspan=3, sticky='we')
    lbl_grauver_in.grid(row=1, column=0)
    txt_grauver_in.grid(row=1, column=1)
    # lbl_grauverin.grid(row=2, column=0)
    bnt_grauver.grid(row=1, column=2)
    # Desenha
    grau_vert_frm.grid(row=0, column=1)

    # Cria frame p/listar os vértices adjacentes de um vértice
    vizi_vert_frm = Frame(framexerc, height=150, width=100, bd=nbordint, relief=SOLID, padx=10, pady=10)
    # Inclui um texto para a lista de adjacência
    lbl_viziver = Label(vizi_vert_frm, text="Localizar os Vizinhos de um Vértice")
    lbl_viziver_in = Label(vizi_vert_frm, text="Vértices:")
    txt_viziver_in = Entry(vizi_vert_frm, width=5)
    # lbl_viziverin = Label(vizi_vert_frm, text=" ")
    bnt_viziver = Button(vizi_vert_frm, text="Localizar", command=lambda: vizinho_vertices())
    # Desenho dos objetos no Frame
    lbl_viziver.grid(row=0, columnspan=3, sticky='we')
    lbl_viziver_in.grid(row=1, column=0)
    txt_viziver_in.grid(row=1, column=1)
    # lbl_viziverin.grid(row=2, column=0)
    bnt_viziver.grid(row=1, column=2)
    # Desenha
    vizi_vert_frm.grid(row=0, column=2)

    framexerc.grid(row=4, column=0)


def sexto_frame(nborda, nbordint):
    # Chamada do Gráfico
    global frm_grafico
    global txt_grafico

    frm_grafico = Frame(initela, height=250, width=300, bd=nborda, relief=SOLID, padx=5, pady=5)

    # Frame do título
    frm_lblinigra = Frame(frm_grafico, height=100, width=270, bd=nbordint, relief=SOLID, padx=5, pady=5)
    lblinicgra = Label(frm_lblinigra, text="*** PLOTAGEM DOS GRAFOS ***", fg="#aaaaaa", font="Arial 13 bold")
    lblinicgra.pack(side='top')
    frm_lblinigra.grid(row=1, columnspan=3, sticky='we')

    # Frame de busca do arquivo
    frm_arqgrafico = Frame(frm_grafico, height=100, width=270, bd=nbordint, relief=SOLID, padx=5, pady=5)
    lbl_grafico = Label(frm_arqgrafico, text="Arquivo Gráfico: ")
    txt_grafico = Entry(frm_arqgrafico, width=80)
    bntabregrafico = Button(frm_arqgrafico, text="Abrir (*.txt)", command=lambda: abre_arqgrafico())
    # Desenho dos objetos no Frame
    lbl_grafico.grid(row=0, column=0)
    txt_grafico.grid(row=0, column=1)
    bntabregrafico.grid(row=0, column=2)
    frm_arqgrafico.grid(row=2, columnspan=3, sticky='we')

    # Frame para organizar os botões de tarefa do gráfico
    frm_bntgrafico = Frame(frm_grafico, height=100, width=270, bd=nbordint, relief=SOLID, padx=5, pady=5)
    lbl_bntgraf = Label(frm_bntgrafico, text="                     ")
    bnt_grafico = Button(frm_bntgrafico, text="Plotar Gráfico (*.txt)", command=lambda: plotgraficoGrafo())
    lbl_bntgrafi = Label(frm_bntgrafico, text="                    ")
    bntsalvagrafico = Button(frm_bntgrafico, text="Salvar Layout(*.csv)", command=lambda: salva_grafico())
    lbl_bntgra = Label(frm_bntgrafico, text="                      ")
    bnt_pltgrafarq = Button(frm_bntgrafico, text="Plotar de Arquivo Layout(*.csv)", command=lambda: ler_arq_tipo_grafico())
    lbl_bntgraf.grid(row=0, column=0)
    bnt_grafico.grid(row=0, column=1)
    lbl_bntgrafi.grid(row=0, column=2)
    bntsalvagrafico.grid(row=0, column=3)
    lbl_bntgra.grid(row=0, column=4)
    bnt_pltgrafarq.grid(row=0, column=5)
    frm_bntgrafico.grid(row=3, columnspan=3, sticky='we')

    # Frame de mensagens
    frm_msggra = Frame(frm_grafico, height=50, width=270, bd=nbordint, relief=SOLID, padx=5, pady=5)
    lbl_bntgraf = Label(frm_msggra, textvariable=mostraarplot)
    lbl_bntgraf.pack(side='top')
    frm_msggra.grid(row=4, columnspan=3, sticky='we')

    frm_grafico.grid(row=5, column=0)


# Instancianado o tkinter Montando a tela

initela.title("Atividade 01 - Teoria dos Grafos")
primeiro_frame(0)
segundo_frame(0, 0)
terceiro_frame(0)
quarto_frame(0)
quinto_frame(0, 1)
sexto_frame(1, 0)


# Definindo o tamanho da Tela e posição, mas ajustável
initela.geometry("800x690+50+2")
# Icone gratuito
initela.iconbitmap("Imagens/Laurent-Baumann-Neige-File-Server.ico")

# Visualiza
initela.mainloop()

# Fim
# *******************************************************
# *************** FIM MENUS ********************
# *******************************************************