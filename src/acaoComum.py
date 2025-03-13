import pyautogui as ptg
from time import sleep
from tkinter import messagebox
from pyperclip import paste, copy
import utils
import operadoresLancamento
import tratamentoItem
import xmltodict
import pyscreeze
import extratorXML


# Este módulo serve pra Fornecer as funções que podem ser usadas tanto pela mariquinhaUnitaria, 
# quanto pela mariquinhaCorrente, que são os dois principais módulos da automação.
# Como eu precisava que a Mariquinha conseguisse lançar muitas RTs de maneira contínua, 
# mas também conseguisse lançar apenas uma RT específica quando necessário, precisei pensar em uma solulução
# que me desse essa flexibilidade. Não tive nenhuma idéia melhor que essa. criei dois módulos, 
# que, embora sejam muito parecidos, não são a mesma coisa, pelo menos não fazem exatamente a mesma coisa.
# Mas devido toda essa semelhança, eu resolvi criar um módulo que contivesse as funções que são comuns a ambos os módulos.


FAILSAFE = True

def proceder_primario():
    """
    Executa o procedimento primário da automação, que inclui:
    - Localizar e clicar na referência da coluna de valor para filtrar da maior para a menor.
    - Verificar o status do processo e, quando identificado que já não há mais
      RTs para lançar, finalizar então o trabalho.
    """
    aguarde = utils.encontrar_centro_imagem(r'Imagens\TelaDeAguarde2.png')
    while type(aguarde) == tuple:
        aguarde = utils.encontrar_centro_imagem(r'Imagens\TelaDeAguarde2.png')
    encontrar = utils.encontrar_imagem(r'Imagens\ReferenciaColunaValorTelaInicial.png')
    cont = 0
    while type(encontrar) != pyscreeze.Box:
        encontrar = utils.encontrar_imagem(r'Imagens\ReferenciaColunaValorTelaInicial.png')
        cont+=1
        if cont == 2:
            ptg.press("enter")
            break 

    sleep(1)

    while True:
        try:
            clique_status = utils.encontrar_centro_imagem(r'Imagens\ReferenciaColunaValorTelaInicial.png')  
            x, y = clique_status
            break
        except TypeError:
            clique_status = utils.encontrar_centro_imagem(r'Imagens\status.png')  
            x, y = clique_status
            break
        except:
            pass

    for _ in range(5):
        ptg.doubleClick(x, y, interval=0.07)
    sleep(1)
    ptg.press("enter", interval=1)

    trabalho_acabou = utils.encontrar_centro_imagem(r'Imagens\ReferenciaFinal.png')
    if type(trabalho_acabou) == tuple:
        messagebox.showinfo("Trabalho finalizado", "Trabalho finalizado com sucesso!")
        raise Exception("Trabalho finalizado com sucesso!")



def insistir_ate_encontrar(x, y):
    """
    Insiste em encontrar as referências de finalização de caixa ou processo pendente.
    Enquanto nenhum dos dois dados que determinam se a automação deve dar o caixa como finalizado ou
    constatar que não conseguirá lançar mais nenhum registro daquela RT não forem encontrados
    essa função mantém a automação em um loop de busca.
    """
    cont = 0
    finalizar = utils.encontrar_centro_imagem(r'Imagens\ReferenciaFinalizarCaixa.png')
    ainda_tem_processo_pendente = utils.encontrar_centro_imagem(r'Imagens\ReferenciaCaixaInacabado.png')
    if type(finalizar) != tuple and type(ainda_tem_processo_pendente) != tuple:
        while type(finalizar) != tuple and type(ainda_tem_processo_pendente) != tuple:
            finalizar = utils.encontrar_centro_imagem(r'Imagens\ReferenciaFinalizarCaixa.png')
            ainda_tem_processo_pendente = utils.encontrar_centro_imagem(r'Imagens\ReferenciaCaixaInacabado.png')
            cont+=1
            if cont == 4:
                ptg.moveTo(150,100)
                ptg.doubleClick(x,y)
                sleep(1)
    return finalizar, ainda_tem_processo_pendente


def solicitar_XML():
    """
    Solicita o XML da nota fiscal e trata possíveis erros como NF cancelada ou duplicidade.

    Returns:
        tuple: Retorna informações sobre a NF cancelada e o XML manual, se aplicável.
    """
    x, y = utils.clicar_2x(r'Imagens\BotaoSolicitarXML.png')
    nf_cancelada = ""
    falsa_duplicidade = ""
    sleep(0.5)
    while True:
        nf_cancelada = utils.encontrar_centro_imagem(r'Imagens\ErroNFCanceladaPeloFornecedor.png')
        falsa_duplicidade = utils.encontrar_centro_imagem(r'Imagens\ErroPossivelDuplicidade.png')
        xml_manual = utils.encontrar_centro_imagem(r'Imagens\ReferenciaAcaoContingencial.png')
        if type(nf_cancelada) == tuple or type(falsa_duplicidade) == tuple or type(xml_manual) == tuple:
            ptg.press("right", interval=0.05)
            ptg.press("enter")
            sleep(0.5)
            break
        aguardando = utils.encontrar_centro_imagem(r'Imagens\TelaDeAguarde1.png')
        if type(aguardando) == tuple:
            while type(aguardando) == tuple:
                aguardando = utils.encontrar_centro_imagem(r'Imagens\TelaDeAguarde1.png')
        else:
            clicar_novamente = utils.encontrar_centro_imagem(r'Imagens\ReferenciaXMLPendente.png')
            if type(clicar_novamente) == tuple:
                ptg.doubleClick(x,y)
            else:
                break
    sleep(1)
    if type(falsa_duplicidade) == tuple:
        inserir_xml = falsa_duplicidade
    elif type(xml_manual) == tuple:
        inserir_xml = xml_manual
    else:
        inserir_xml = None
    return nf_cancelada, inserir_xml



def verificar_status():
    """
    Verifica o status do registro atual e retorna o controle correspondente.
    O Controlador é uma string que indica qual ação deve ser tomada a partir do status do registro.
    """
    sleep(0.3)
    status_registro1 = utils.encontrar_centro_imagem(r'Imagens\ReferenciaXMLPendente.png')
    if type(status_registro1) == tuple:
        controlador = "Clicar em Solicitar XML"
    else:
        status_registro2 = utils.encontrar_centro_imagem(r'Imagens\ReferenciaChaveDanfeNaoDisponivel.png')
        if type(status_registro2) == tuple:
            controlador = "Copie a chave de acesso 1"
        else:
            status_registro3 = utils.encontrar_centro_imagem(r'Imagens\RegistroDisponivelParaLancamento.png')
            if type(status_registro3) == tuple:
                controlador = "Lançar DANFE"
            else:
                status_registro4 = utils.encontrar_centro_imagem(r'Imagens\RegistroTipoRecibo.png')
                if type(status_registro4) == tuple:
                    controlador = "Lançar recibo"
                else:
                    status_registro5 = utils.encontrar_centro_imagem(r'Imagens\ReferenciaXMLPendente2.png')
                    if type(status_registro5) == tuple:
                        controlador = "Clicar em Solicitar XML"
                    else:
                        status_registro6 = utils.encontrar_centro_imagem(r'Imagens\RegistroSemChaveInformada.png')
                        if type(status_registro6) == tuple:
                            controlador = "Copie a chave de acesso 2"
                        else:
                            messagebox.showerror("Erro!", "Status não mapeado.")
                            raise Exception("Status não mapeado.")
    return controlador



def filtrar_status():
    """
    Filtra os registros de uma RT para que se efetue o lançamento
    através da coluna status. Além de verificar se já não há mais nenhum
    registro disponível para lançamento.
    """
    caixa_finalizado = ''
    try:
        x, y = utils.encontrar_centro_imagem(r'Imagens\ReferenciaStatus.png')
    except TypeError:
        x, y = utils.encontrar_centro_imagem(r'Imagens\ReferenciaStatusNegrito.png')
    ptg.doubleClick(x, y)
    sleep(1.5)
    ptg.doubleClick(x, y)
    sleep(1.5)
    caixa_finalizado = utils.encontrar_centro_imagem(r'Imagens\ReferenciaRegistroLancado.png')
    if type(caixa_finalizado) == tuple:
        ptg.doubleClick(x, y)
        caixa_finalizado = utils.encontrar_centro_imagem(r'Imagens\ReferenciaRegistroLancado.png')
        sleep(0.5)
    return caixa_finalizado


def pular_processo():
    _ = filtrar_status()
    sleep(0.5)
    ptg.press("down", interval=0.7)


def clicar_Lancar():
    """
    Clica no botão lançar nota para as DANFES ou Recibos.
    Além de verificar em um novo momento se já não há mais nenhum
    registro disponível para lançamento.
    """
    sleep(0.5)
    x, y = utils.clicar_2x(r'Imagens\BotaoLancarNota.png')
    ptg.doubleClick(x,y)
    sleep(0.3)

    utils.lancar_retroativo()
    aguarde1, aguarde2 = utils.aguardar2()
    if type(aguarde1) == tuple or type(aguarde2) == tuple:
        while True:
            aguarde3, aguarde4 = utils.aguardar2()
            if type(aguarde3) != tuple and type(aguarde4) != tuple:
                utils.lancar_retroativo()
                aguarde3, aguarde4 = utils.aguardar2()
                if type(aguarde3) != tuple and type(aguarde4) != tuple:
                    break
    else:
        utils.lancar_retroativo()
        aguarde1, aguarde2 = utils.aguardar2()
        if type(aguarde1) != tuple and type(aguarde2) != tuple:
            ptg.doubleClick(x,y)
    sleep(1)

    caixa_finalizado = utils.encontrar_centro_imagem(r'Imagens\ReferenciaRegistroJaLancado2.png')
    nf_ja_lancada = utils.encontrar_centro_imagem(r'Imagens\ReferenciaNFjaLancada.png')
    if type(caixa_finalizado) == tuple:
        caixa_finalizado = True
    elif type(nf_ja_lancada) == tuple:
        caixa_finalizado = "NF já lançada"
    else:
        caixa_finalizado = False
    return caixa_finalizado



def copiar_chave_acesso():
    """
    Copia a chave de acesso da nota fiscal e verifica se o processo foi feito corretamente.

    Returns:
        tuple: Retorna a chave de acesso e um booleano indicando se o processo foi feito corretamente.
    """
    processo_feito_errado = False
    x, y = utils.clicar_2x(r'Imagens\BotaoCopiarChaveDeAcesso.png')
    sleep(1)
    encontrar_chave_de_acesso = utils.encontrar_imagem(r'Imagens\ReferenciaAbriuChaveDeAcesso.png')
    caixa_finalizado = utils.encontrar_imagem(r'Imagens\ReferenciaRegistroJaLancado2.png')
    while type(encontrar_chave_de_acesso) != pyscreeze.Box:
        if type(caixa_finalizado) == pyscreeze.Box:
            caixa_finalizado = True
            chave_de_acesso = caixa_finalizado
            return chave_de_acesso, processo_feito_errado
        if type(encontrar_chave_de_acesso) != pyscreeze.Box:
            encontrar_chave_de_acesso = utils.encontrar_imagem(r'Imagens\ReferenciaAbriuChaveDeAcesso.png')
            ptg.doubleClick(x, y)
            caixa_finalizado = utils.encontrar_imagem(r'Imagens\ReferenciaRegistroJaLancado2.png')
    sleep(0.5)
    ptg.hotkey("ctrl", "c")
    chave_de_acesso = paste()
    chave_de_acesso = chave_de_acesso.replace(" ", "")
    if len(chave_de_acesso) != 44:
        processo_feito_errado = True
    sleep(0.5)
    ptg.press("esc")
    sleep(2)
    return chave_de_acesso, processo_feito_errado



def rejeitar_caixa(mensagem="Centro de Custo Bloqueado.", tipo="Programado"):
    """
    Rejeita o caixa atual com uma mensagem específica. A mensagem que será passada para o campo
    de rejeição depende do tipo de rejeição, que pode ser "Programado" ou "Independente".
    Programado é quando a função de rejeição foi acionada pela própria lógica da automação.
    O caso onde isso acontece é quando o sistema acusa que o CC de um dos registros está bloqueado.
    Independente é quando a função de rejeição foi acionada manualmente pelo usuário através
    da interface da Mariquinha.
    """
    if tipo == "Independente":
        utils.clicar_microsiga()
    abriu = utils.encontrar_centro_imagem(r'Imagens\BotaoRejeitarCaixa.png')
    while type(abriu) != tuple:
        utils.clicar_microsiga()
        abriu = utils.encontrar_centro_imagem(r'Imagens\BotaoRejeitarCaixa.png')

    sleep(0.5)
    while True:
        x, y = utils.clicar_2x(r'Imagens\status.png')
        sleep(1.5)
        aux = 0
        repetir_clique = utils.encontrar_centro_imagem(r'Imagens\ReferenciaRegistroLancado.png')
        if type(repetir_clique) != tuple:
            while type(repetir_clique) != tuple and aux < 3:
                ptg.doubleClick(x, y)
                ptg.moveTo(150,100)
                aux+=1
                repetir_clique = utils.encontrar_centro_imagem(r'Imagens\ReferenciaRegistroLancado.png')
        sleep(0.5)
        if aux != 3:
            x, y = utils.clicar_2x(r'Imagens\BotaoCancelar.png')
            tela_de_lancamento = utils.esperar_aparecer(r'Imagens\ReferenciaDocumentoEntrada.png')
            ptg.hotkey("ctrl", "s", interval=0.5)
            aguarde1, aguarde2 = utils.aguardar2()
            if type(aguarde1) == tuple or type(aguarde2) == tuple:
                while True:
                    aguarde3, aguarde4 = utils.aguardar2()
                    if type(aguarde3) != tuple and type(aguarde4) != tuple:
                        break
        else:
            break
    x, y = abriu
    ptg.doubleClick(x,y)
    campo_mensagem = utils.encontrar_centro_imagem(r'Imagens\CampoObservacaoRejeicao.png')

    while type(campo_mensagem) != tuple:
        sleep(0.6)
        x, y = utils.clicar_2x(r'Imagens\BotaoRejeitarCaixa.png')
        sleep(0.7)
        campo_mensagem = utils.encontrar_centro_imagem(r'Imagens\CampoObservacaoRejeicao.png')

    ptg.moveTo(150,100)

    copy(mensagem)
    ptg.hotkey("ctrl", "v")
    ptg.press("tab")
    ptg.press("enter")
    aguarde = utils.encontrar_imagem(r'Imagens\TelaDeAguarde1.png')
    aux_cont = 0
    while type(aguarde) != pyscreeze.Box:
        aguarde = utils.encontrar_imagem(r'Imagens\TelaDeAguarde1.png')
        aux_cont+=1
        if aux_cont == 0:
            break
    sleep(2)


def copiar_RT(passos=2):
    sleep(1)
    ptg.hotkey(["shift", "tab"]*passos)
    ptg.hotkey("ctrl", "c", interval=2)
    dono_da_rt = paste()
    ptg.hotkey(["shift", "tab"]*2)
    ptg.hotkey("ctrl", "c", interval=2)
    rt = paste()
    rt = rt.replace(" ", "")
    return dono_da_rt, rt



def extrair_dados_XML(caminho):
    """
    Extrai os dados de um arquivo XML. Há diferentes possibilidades de árvores XML
    que podemos encontrar. O XML nada mais é do que um conjunto de chaves e valores, e chaves que
    comportam mais chaves. Ele pode ter mais de um item, e, tendo mais de um item,
    a abordagem para extrair seus dados é uma (que segue a linha [const_item], que nada mais é do que acessar item por item
    através de seu indice. Ex: 0, 1, 2...), enquanto quando há apenas um item no XML a abordagem é outra.
    """
    try:
        with open(caminho) as fd:
            doc = xmltodict.parse(fd.read())
    except UnicodeDecodeError:
        with open(caminho, encoding='utf-8') as fd:
            doc = xmltodict.parse(fd.read())
    except:
        with open(caminho, encoding='utf-8') as fd:
            doc = xmltodict.parse(fd.read(), attr_prefix="@", cdata_key="#text")

    processador = extratorXML.ProcessadorXML(doc)
    nome_fantasia_forn = processador.coletar_nome_fantasia()

    const_item = 0
    while True:
        try:
            coletor_xml = doc["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]
            impostos_xml = doc["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]
            valores_do_item = processador.coletar_dados_XML(coletor_xml, impostos_xml)
            break
        except KeyError:
            try:
                coletor_xml = doc["enviNFe"]["NFe"]["infNFe"]["det"]["prod"]
                impostos_xml = doc["enviNFe"]["NFe"]["infNFe"]["det"]["imposto"]
                valores_do_item = processador.coletar_dados_XML(coletor_xml, impostos_xml)
                break
            except KeyError:
                try:
                    coletor_xml = doc["NFe"]["infNFe"]["det"]["prod"]
                    impostos_xml = doc["NFe"]["infNFe"]["det"]["imposto"]
                    valores_do_item = processador.coletar_dados_XML(coletor_xml, impostos_xml)
                    break
                except TypeError:
                    try:
                        coletor_xml = doc["NFe"]["infNFe"]["det"][const_item]["prod"]
                        impostos_xml = doc["NFe"]["infNFe"]["det"][const_item]["imposto"]
                        valores_do_item = processador.coletar_dados_XML(coletor_xml, impostos_xml)
                        const_item += 1
                    except IndexError:
                        break
            except TypeError:
                try:
                    coletor_xml = doc["enviNFe"]["NFe"]["infNFe"]["det"][const_item]["prod"]
                    impostos_xml = doc["enviNFe"]["NFe"]["infNFe"]["det"][const_item]["imposto"]
                    valores_do_item = processador.coletar_dados_XML(coletor_xml, impostos_xml)
                    const_item += 1
                except IndexError:
                    break
        except TypeError:
            try:
                coletor_xml = doc["nfeProc"]["NFe"]["infNFe"]["det"][const_item]["prod"]
                impostos_xml = doc["nfeProc"]["NFe"]["infNFe"]["det"][const_item]["imposto"]
                valores_do_item = processador.coletar_dados_XML(coletor_xml, impostos_xml)
                const_item += 1
            except IndexError:
                break

    itens, indices_e_impostos = processador.trabalhar_dados_XML(valores_do_item)

    return nome_fantasia_forn, itens, indices_e_impostos



def verificar_cadastro_forn(nome_fantasia_forn):
    """
    Essa função verifica se o Siga forçou a abertura da rotina de cadastro de fornecedor
    para os casos em que o fornecedor não tem uma natureza, um nome fantasia,
    nem um tipo de contribuição definidos no sistema.
    """
    cadastro_fornecedor = utils.encontrar_imagem(r'Imagens\ReferenciaTelaCadastroDeFornecedor.png')
    if type(cadastro_fornecedor) == pyscreeze.Box:
        sem_nome_fantasia = utils.encontrar_imagem(r'Imagens\ForncedorSemNomeFantasia.png')
        if type(sem_nome_fantasia) == pyscreeze.Box:
            ptg.press(["tab"]*2)
            ptg.write(nome_fantasia_forn, interval=0.1)
            ptg.press("tab", interval=1)
        ptg.hotkey("alt", "a", interval=1)
        ptg.press(["tab"]*5)
        natureza = "2020087"
        ptg.write(natureza, interval=0.1)
        ptg.press("tab", interval=1)
        ptg.hotkey("alt", "f", interval=1)
        ptg.hotkey(["shift", "tab"]*3, interval=0.4)
        sleep(0.5)
        ptg.press("space", interval=0.5)
        ptg.press(["up"]*2)
        ptg.press("enter", interval=0.5)
        ptg.hotkey("ctrl", "s", interval=0.5)



def inserir_valores_da_NF_no_siga(indices_e_impostos, itens):
    """
    Função que realiza o trabalho de inserir os valores dos itens da nota fiscal no sistema SIGA
    com base no que o indicador ctrl_imposto, que indica quanto dos três impostos
    essenciais cada item daquela NF tem, determina.
    """
    for i, ctrl_imposto in enumerate(indices_e_impostos):

        verificador, item_fracionado = operadoresLancamento.verificar_valor_do_item(itens, i)
        if verificador == True:

            # Circunstância indesejada:
            # Caso o valor do item não corresponda de nenhuma maneira ao total do item na NF,
            # a +TI deve ser contatada imediatamente, pois, a rotina IntAgillitas foi configurada por eles,
            # para puxar exatamente o mesmo valor do item que consta no xml. Então,
            # se o valor não corresponder diretamente, nem estiver fracionado, a +TI deve
            # ser acionada.

            messagebox.showerror("Erro!", "Contate a +TI imediatamente.")
            raise Exception("Contate a +TI imediatamente.")
        tratamento_item = tratamentoItem.TratadorItem(item_fracionado, itens, i, ctrl_imposto)
        item = tratamento_item.tratar_item()
        cont = 0

        match ctrl_imposto:
            case "Nenhum imposto":
                ptg.press(["left"]*4)    
                                    
            case "Apenas o ICMS":
                for lista in item:
                    icms_no_item, bc_icms, aliq_icms, icmsST_no_item, ipi_no_item = lista
                    operadoresLancamento.definir_TES(ctrl_imposto)
                    operadoresLancamento.inserir_ICMS(icms_no_item, bc_icms, aliq_icms)
                    ptg.press(["left"]*9)
                    ptg.press("down")
                    cont+=1
                    operadoresLancamento.corrigir_passos_horizontal(cont, item)
                ptg.press("up")
                                        
            case "Apenas o ICMSST":
                for lista in item:
                    icms_no_item, icmsST_no_item, base_icms_ST, aliq_icms_ST, ipi_no_item = lista
                    operadoresLancamento.definir_TES(ctrl_imposto)
                    operadoresLancamento.zerar_imposto()
                    operadoresLancamento.inserir_ICMSST(icmsST_no_item, base_icms_ST, aliq_icms_ST, passosST=9)
                    ptg.press("down")
                    cont+=1
                    operadoresLancamento.corrigir_passos_horizontal(cont, item)
                ptg.press("up")
                                        
            case "Apenas o IPI":
                for lista in item:
                    icms_no_item, icmsST_no_item, ipi_no_item, base_ipi, aliq_ipi = lista
                    operadoresLancamento.definir_TES(ctrl_imposto)
                    operadoresLancamento.inserir_IPI(ipi_no_item, base_ipi, aliq_ipi)
                    operadoresLancamento.zerar_imposto()
                    ptg.press("down")
                    cont+=1
                    operadoresLancamento.corrigir_passos_horizontal(cont, item)
                ptg.press("up")
                                        
            case "Apenas ICMSST e IPI":
                for lista in item:
                    icms_no_item, icmsST_no_item, base_icms_ST, aliq_icms_ST, ipi_no_item, base_ipi, aliq_ipi = lista
                    operadoresLancamento.definir_TES(ctrl_imposto)
                    operadoresLancamento.zerar_imposto()
                    operadoresLancamento.inserir_ICMSST(icmsST_no_item, base_icms_ST, aliq_icms_ST, passosST=9)
                    operadoresLancamento.inserir_IPI(ipi_no_item, base_ipi, aliq_ipi, passosIPI=0)
                    ptg.press("down")
                    cont+=1
                    operadoresLancamento.corrigir_passos_horizontal(cont, item)
                ptg.press("up")
                                        
            case "Apenas ICMS e IPI":
                for lista in item:
                    icms_no_item, base_icms, aliq_icms, icmsST_no_item, ipi_no_item, base_ipi, aliq_ipi = lista
                    operadoresLancamento.definir_TES(ctrl_imposto)
                    operadoresLancamento.inserir_ICMS(icms_no_item, base_icms, aliq_icms)
                    operadoresLancamento.inserir_IPI(ipi_no_item, base_ipi, aliq_ipi, passosIPI=3)
                    ptg.press("down")
                    cont+=1
                    operadoresLancamento.corrigir_passos_horizontal(cont, item)
                ptg.press("up")
                                        
            case "Apenas ICMS e ICMSST":
                for lista in item:
                    icms_no_item, base_icms, aliq_icms, icmsST_no_item, base_icms_ST, aliq_icms_ST, ipi_no_item = lista
                    operadoresLancamento.definir_TES(ctrl_imposto)
                    operadoresLancamento.inserir_ICMS(icms_no_item, base_icms, aliq_icms)
                    operadoresLancamento.inserir_ICMSST(icmsST_no_item, base_icms_ST, aliq_icms_ST, passosST=0)
                    ptg.press("down")
                    cont+=1
                    operadoresLancamento.corrigir_passos_horizontal(cont, item)
                ptg.press("up")
                                        
            case "Todos os impostos":
                for lista in item:
                    icms_no_item, base_icms, aliq_icms, icmsST_no_item, base_icms_ST, aliq_icms_ST, ipi_no_item, base_ipi, aliq_ipi = lista
                    operadoresLancamento.definir_TES(ctrl_imposto)
                    operadoresLancamento.inserir_ICMS(icms_no_item, base_icms, aliq_icms)
                    operadoresLancamento.inserir_ICMSST(icmsST_no_item, base_icms_ST, aliq_icms_ST, passosST=0)
                    operadoresLancamento.inserir_IPI(ipi_no_item, base_ipi, aliq_ipi, passosIPI=12)
                    ptg.press("down")
                    cont+=1
                    operadoresLancamento.corrigir_passos_horizontal(cont, item)
                ptg.press("up")
                           

        if len(indices_e_impostos) > 1:
            ptg.press("down")
        if i+1 == len(indices_e_impostos):
            ptg.press("up")
        sleep(2)



def finalizar_lancamento():
    """
    Realiza a tarefa de finalizar o lançamento de cada registro de uma RT.
    """
    ptg.hotkey("ctrl", "s", interval=1.5)

    erro_cnpj = utils.encontrar_centro_imagem(r'Imagens\ErroCNPJ.png')
    if type(erro_cnpj) == tuple:
        ptg.press("enter")
        campo_sped = utils.encontrar_centro_imagem(r'Imagens\CampoSPED.png')
        x, y = campo_sped
        sleep(1)
        ptg.doubleClick(x,y)
        sleep(1)
        ptg.write("NF", interval=0.3)
        ptg.press("tab")
        ptg.hotkey("ctrl", "s", interval=1)

    while True:
        sem_tela_final = utils.encontrar_centro_imagem(r'Imagens\ReferenciaSemTelaFinal.png')
        repentina_etapa_final = utils.encontrar_centro_imagem(r'Imagens\ReferenciaFinalPorLancamento.png')
        aguarde = utils.encontrar_centro_imagem(r'Imagens\TelaDeAguarde2.png')
        if type(aguarde) == tuple:
            sleep(0.5)
            continue
        if type(repentina_etapa_final) == tuple:
            utils.tratar_etapa_final()
            break
        elif type(sem_tela_final) == tuple:
            break

    repentina_etapa_final = utils.encontrar_centro_imagem(r'Imagens\ReferenciaFinalPorLancamento.png')
    if type(repentina_etapa_final) == tuple:
        utils.tratar_etapa_final()
        
