import pyautogui as ptg
from pyperclip import paste
from time import sleep
import pyscreeze
import utils


# Módulo fornecedor de funções utilitárias para validação, correção, ou inserção de dados
# no momento de lançamento da NF na rotina Documento Entrada.
# Nesse momento é onde confrontamos os dados da NF com os dados passados no pedido criado pelo comprador,
# além de inserirmos dados no processo, como a TES.


FAILSAFE = True


def escrever_valor_unit(valor_unit):
    """
    Função auxiliar à função verificar_valor_item. Ela escreve o valor unitário de um item no sistema SIGA,
    após mover o cursor para a posição correta.
    """
    ptg.press("right")
    valor_unit = utils.formatador(valor_unit, casas_decimais="{:.6f}")
    sleep(0.2)
    ptg.write(valor_unit)
    sleep(0.2)
    ptg.press(["right"]*3)


def verificar_valor_do_item(lista, indiceX):
    """
    Verifica se o valor do item no SIGA corresponde ao valor do item na nota fiscal (NF).
    Se não corresponder, tenta corrigir o valor unitário ou quantidade.

    :param lista: Lista contendo os valores dos itens da NF.
    :param indiceX: Índice do item atual na lista.

    :return: Uma tupla contendo um booleano (se o lançamento deve ser cancelado) e uma lista de razões (quant. do item na linha / quantidade total do item na NF) 
             para correção caso o item seja fracionado.
             * Veja o módulo tratamentoItem *. 
             Aqui também temos uma regra de negócio sendo aplicada: alguns itens 
             específicos passam por uma conversão de unidade de medida no pedido. Para que o programa saiba lidar com esses itens, 
             eles foram mapeados e inseridos no código afim de aplicar a devida tratativa para cada caso.
    """
    cancelar_lancamento = False
    razoes = []
    sleep(0.7)
    ptg.press(["right"]*4)
    sleep(0.7)
    ptg.hotkey("ctrl", "c")
    sleep(0.7)
    valor_do_item_no_siga = paste()
    valor_do_item_no_siga = utils.formatador4(valor_do_item_no_siga)
    valor_do_item_na_NF = lista[indiceX][0]
    valor_do_item_na_NF = utils.formatador3(valor_do_item_na_NF)
    if valor_do_item_no_siga != valor_do_item_na_NF:
        ptg.write(lista[indiceX][0])
        sleep(0.8)
        encontrar = utils.encontrar_imagem(r'Imagens\valitenErrado.png')
        if type(encontrar) == pyscreeze.Box:
            ptg.press("enter")
            sleep(0.5)
            encontrar = utils.encontrar_imagem(r'Imagens\valitenErrado.png')
            if type(encontrar) == pyscreeze.Box:
                ptg.press("enter")
            ptg.press("esc")
            ptg.press(["left"]*5)
            sleep(0.2)
            ptg.hotkey("ctrl", "c", interval=0.5)
            quantidade_siga = paste()
            quantidade_siga = utils.formatador4(quantidade_siga)
            quantidade_NF = lista[indiceX][1]
            quantidade_NF = utils.formatador3(quantidade_NF)
            valor_unit_NF = lista[indiceX][2]
            valor_unit_NF = utils.formatador3(valor_unit_NF)
            if quantidade_siga == quantidade_NF:
                escrever_valor_unit(valor_unit_NF)
            else:
                valor_unit_NF = utils.formatador(valor_unit_NF, casas_decimais="{:.6f}")
                cont = 0
                quantidade_total = []
                quantidade_total.append(quantidade_siga)
                ptg.press(["left"]*6)
                sleep(0.2)
                ptg.hotkey("ctrl", "c", interval=0.5)
                cod_item = paste()
                try:
                    while sum(quantidade_total) < quantidade_NF:
                        ptg.press("down")
                        sleep(0.5)
                        ptg.hotkey("ctrl", "c", interval=0.8)
                        item_dividido = paste()
                        cont+=1
                        if item_dividido == cod_item:
                            ptg.press(["right"]*6)
                            ptg.hotkey("ctrl", "c", interval=0.8)
                            qtd_dividida = paste()
                            qtd_dividida = utils.formatador4(qtd_dividida)
                            quantidade_total.append(qtd_dividida)
                            ptg.press("right")
                            ptg.write(valor_unit_NF, interval=0.05)
                            ptg.press(["left"]*8)      
                        else:
                            break
                except TypeError:
                    pass
                if len(quantidade_total) > 10:
                    ptg.press(["up"]*cont, interval=20)
                else:
                    ptg.press(["up"]*cont, interval=0.1)
                sleep(0.5)
                ptg.press(["right"]*7)
                sleep(0.5)
                ptg.write(valor_unit_NF, interval=0.05)
                try:
                    if sum(quantidade_total) != quantidade_NF:
                        cancelar_lancamento = True
                    else:
                        for qtd in quantidade_total:
                            razao = qtd / quantidade_NF
                            razoes.append(razao)
                        ptg.press(["right"]*3)
                except TypeError:
                    cancelar_lancamento = True
        else:
            ptg.press("left")
    return cancelar_lancamento, razoes


def definir_TES(ctrl_imposto):
    """
    Define e insere o Tipo de Entrada/Saída (TES) com base no 
    indicador da modalidade de impostos presente na variável ctrl_imposto.
    Para o caso dos lançamentos do Agillitas são apenas duas opções:
    154 - Com impostos
    155 - Sem impostos

    :param ctrl_imposto: Controle de impostos aplicados ao item.
    """
    if ctrl_imposto != "Nenhum imposto":
        tes = "154"
    else:
        tes = "155"
    if tes == "154":
        ptg.press(["left"]*9)
        ptg.press("enter", interval=0.3)
        ptg.write(tes)
        ptg.press(["right"]*9)
        natureza = "2020087"
        ptg.write(natureza)
        ptg.press("enter", interval=0.3)
        ptg.press(["left"]*6)
    else:
        ptg.press(["left"]*4)


def inserir_ICMS(icms_no_item, bc_icms, aliq_icms):
    ptg.press(["right"]*7)
    sleep(0.5)
    ptg.press("enter")
    bc_icms = utils.formatador2(bc_icms)
    ptg.write(bc_icms)
    ptg.press(["right"]*8)
    sleep(0.5)
    ptg.press("enter")
    ptg.write(aliq_icms)
    sleep(0.5)
    ptg.press(["left"]*9)
    sleep(0.5)
    ptg.press("enter")
    icms_no_item = utils.formatador2(icms_no_item)
    ptg.write(icms_no_item)


def inserir_ICMSST(icmsST_no_item, base_icms_ST, aliq_icms_ST, passosST=8):
    ptg.press(["right"]*passosST)
    sleep(0.5)
    ptg.press("enter")
    base_icms_ST = utils.formatador2(base_icms_ST)
    ptg.write(base_icms_ST)
    sleep(0.5)
    ptg.press("right")
    sleep(0.5)
    ptg.press("enter")
    icmsST_no_item = utils.formatador2(icmsST_no_item)
    ptg.write(icmsST_no_item)
    ptg.press(["left"]*12)    


def inserir_IPI(ipi_no_item, base_ipi, aliq_ipi, passosIPI=12):
    ptg.press(["right"]*passosIPI)
    sleep(0.5)
    ptg.press("enter")
    base_ipi = utils.formatador2(base_ipi)
    ptg.write(base_ipi)
    ptg.press(["right"]*5)
    sleep(0.5)
    ptg.press("enter")
    ptg.write(aliq_ipi)
    ptg.press(["left"]*6)
    sleep(0.5)
    ptg.press("enter")
    ipi_no_item = utils.formatador2(ipi_no_item)
    ptg.write(ipi_no_item)
    ptg.press(["left"]*14)


def zerar_imposto(passos_ida=7, passos_volta=8):
    ptg.press(["right"]*passos_ida)
    ptg.press("enter")
    ptg.press("backspace")
    ptg.press("enter")
    ptg.press(["left"]*passos_volta)


def corrigir_passos_horizontal(cont, item):
    if len(item) > 1:
        ptg.press(["right"]*4)
        sleep(1)
        if cont == len(item):
            ptg.press(["left"]*4)


    