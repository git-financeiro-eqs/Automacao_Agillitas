import pyautogui as ptg
from pyperclip import copy  
from time import sleep
from pathlib import Path
import utils
import pyscreeze
import acaoComum


# Um dos dois módulos principais da automação. Este módulo é responsável por realizar o lançamento
# de uma RT apenas, por isso do nome "Unitaria".


FAILSAFE = True
doc = ''


def lancamento_isolado(rt):
    """
    Essa função tem um funcionamento simples: ela recebe o número de uma RT e realiza o lançamento da mesma
    no sistema SIGA. É muito parecida com a mariquinhaCorrente, com a diferença de que esse módulo é focado
    no lançamento de uma unica RT definida pelo operador.
    """

    pular_processo = []                     
    controle_de_repeticao = []
    dono_da_rt = []
    chave_inconforme = []
    sem_xml = []
    rt_contador = []
    nf_ja_lancada = []
    cond_pag = []
    bloqueado = []
    cnpj_inconclusivo = []
    chave_sefaz =[]
    ncm_problematica = []

    utils.clicar_microsiga()

    sleep(0.5)
    try:
        primeiro_clique = utils.encontrar_centro_imagem(r'Imagens\ReferenciaCliqueInicial.png')
        x, y = primeiro_clique
        ptg.click(x, y)
    except TypeError:
        primeiro_clique = utils.encontrar_centro_imagem(r'Imagens\ReferenciaCliqueInicialSelecionado.png')
        x, y = primeiro_clique
        ptg.click(x, y)
    sleep(0.5)
    ptg.hotkey(["shift", "tab"]*4, interval=0.04)
    ptg.press("t", interval=0.1)
    ptg.click(x, y)
    ptg.hotkey("shift", "tab", interval=0.04)
    ptg.write(rt, interval=0.05)
    ptg.press(["tab"]*2)
    sleep(0.7)
    ptg.press("enter", interval=1.3)
  
    acaoComum.proceder_primario()

    ptg.moveTo(150,100)

    sleep(0.5)

    estado_do_caixa = acaoComum.filtrar_status()

    if type(estado_do_caixa) == tuple:
        x, y = utils.clicar_finalizar()
        finalizar, ainda_tem_processo_pendente = acaoComum.insistir_ate_encontrar(x, y)

        if type(ainda_tem_processo_pendente) == tuple:
            utils.tratar_processos_pendentes()
            if rt_contador:
                utils.enviar_email(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
            return
        
        if type(finalizar) == tuple:
            ptg.press("enter")
        utils.aguardar()
        utils.clicar_botao_sair()
        if rt_contador:
            utils.enviar_email(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
        return
        
    def operar_lancamento(pular_processo):
        estado_do_caixa = False
        global doc

        controlador = acaoComum.verificar_status()

        if controlador == "Lançar recibo":
            estado_do_caixa = acaoComum.clicar_Lancar()
            cc_bloqueado = utils.encontrar_imagem(r'Imagens\ReferenciaCCBloqueado.png')
            if type(cc_bloqueado) == pyscreeze.Box:
                ptg.press("enter", interval=0.5)
                acaoComum.rejeitar_caixa()
                return
            
            recibo_corrigido = utils.encontrar_centro_imagem(r'Imagens\ReferenciaReciboCorrigido.png')
            if type(recibo_corrigido) == tuple:
                ptg.hotkey(["shift", "tab"]*2, interval=0.5)
                ptg.press("enter", interval=0.5)
                sleep(3)
            
            repentina_etapa_final = utils.encontrar_imagem(r'Imagens\ReferenciaFinalPorLancamento.png')

            if type(repentina_etapa_final) == pyscreeze.Box:
                utils.tratar_etapa_final()

            if estado_do_caixa == "NF já lançada":
                controle_de_repeticao.append(chave_de_acesso)
                pular_processo.append(chave_de_acesso)
                ptg.press("tab", interval=0.3)
                ptg.press("enter", interval=0.5)
                if not rt_contador:
                    autor_da_rt, rt = acaoComum.copiar_RT(passos=1)
                    dono_da_rt.append(autor_da_rt)
                    rt_contador.append(rt)
                nf_ja_lancada.append(rt_contador[0])
                acaoComum.pular_processo()
                return operar_lancamento(pular_processo)
            
            if estado_do_caixa == True:
                x, y = utils.clicar_finalizar()
                finalizar, ainda_tem_processo_pendente = acaoComum.insistir_ate_encontrar(x, y)

                if type(ainda_tem_processo_pendente) == tuple:
                    utils.tratar_processos_pendentes()
                    if rt_contador:
                        utils.enviar_email(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                    return
                
                if type(finalizar) == tuple:
                    ptg.press("enter")
                utils.aguardar()
                utils.clicar_botao_sair()
                if rt_contador:
                    utils.enviar_email(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                return
            
            else:
                estado_do_caixa = acaoComum.filtrar_status()

                if type(estado_do_caixa) == tuple:
                    x, y = utils.clicar_finalizar()
                    finalizar, ainda_tem_processo_pendente = acaoComum.insistir_ate_encontrar(x, y)

                    if type(ainda_tem_processo_pendente) == tuple:
                        utils.tratar_processos_pendentes()
                        if rt_contador:
                            utils.enviar_email(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                        return
                    
                    if type(finalizar) == tuple:
                        ptg.press("enter")
                    utils.aguardar()
                    utils.clicar_botao_sair()
                    if rt_contador:
                        utils.enviar_email(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                    return
                
                controle_de_repeticao.clear()
                return operar_lancamento(pular_processo)
            

        elif controlador == "Clicar em Solicitar XML":
            status_nf, inserir_xml = acaoComum.solicitar_XML()

            if type(status_nf) == tuple:
                try:
                    numero_nf = chave_de_acesso[25:34]
                except UnboundLocalError:
                    chave_de_acesso, processo_feito_errado = acaoComum.copiar_chave_acesso()
                    numero_nf = chave_de_acesso[25:34]
                acaoComum.rejeitar_caixa(mensagem = f"NF {numero_nf} foi cancelada pelo fornecedor.")
                return
            
            
            if type(inserir_xml) == tuple:
                chave_de_acesso, processo_feito_errado = acaoComum.copiar_chave_acesso()
                x, y = utils.clicar_2x(r'Imagens\BotaoSolicitarXML.png')

                while True:
                    aguardando = utils.encontrar_centro_imagem(r'Imagens\TelaDeAguarde1.png')
                    falsa_duplicidade = utils.encontrar_centro_imagem(r'Imagens\ErroPossivelDuplicidade.png')
                    xml_manual = utils.encontrar_centro_imagem(r'Imagens\ReferenciaAcaoContingencial.png')
                    if type(aguardando) == tuple:
                        while type(aguardando) == tuple:
                            aguardando = utils.encontrar_centro_imagem(r'Imagens\TelaDeAguarde1.png')
                    elif type(falsa_duplicidade) == tuple or type(xml_manual) == tuple:
                        try:
                            verificador = pular_processo.index(chave_de_acesso)
                            try:
                                verificador = controle_de_repeticao.index(chave_de_acesso)
                                ptg.press(["tab"]*7, interval=0.1)
                                sleep(1)
                                ptg.press("enter", interval=1)
                                utils.repetir_botao()
                                if rt_contador:
                                    utils.enviar_email(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                                return
                            
                            except ValueError:
                                ptg.press("right", interval=0.05)
                                ptg.press("enter")
                                acaoComum.pular_processo()
                                controle_de_repeticao.append(chave_de_acesso)
                                return operar_lancamento(pular_processo)
                            
                        except:
                            caminho = "C:\\Users\\User\\OneDrive - EQS Engenharia Ltda\\Área de Trabalho\\Mariquinha\\xmlFiscalio\\" + chave_de_acesso + ".xml"
                            path = Path(caminho)

                            if not path.exists():
                                ptg.press("right", interval=0.05)
                                ptg.press("enter")
                                pular_processo.append(chave_de_acesso)
                                controle_de_repeticao.append(chave_de_acesso)
                                if not rt_contador:
                                    autor_da_rt, rt = acaoComum.copiar_RT(passos=4)
                                    dono_da_rt.append(autor_da_rt)
                                    rt_contador.append(rt)
                                acaoComum.pular_processo()
                                sem_xml.append(rt_contador[0])
                                return operar_lancamento(pular_processo)
              
                        ptg.press("enter", interval=0.5)
                        ptg.press("tab")
                        copy(caminho)
                        ptg.hotkey("ctrl", "v")
                        sleep(0.7)
                        ptg.hotkey(["shift", "tab"]*2, interval=0.4)
                        ptg.press("enter", interval=2)

                        erro_de_xml = utils.encontrar_imagem(r'Imagens\ErroNaImportacaoDoXML.png')
                        if type(erro_de_xml) == pyscreeze.Box:
                            ptg.press("enter")
                            pular_processo.append(chave_de_acesso)
                            controle_de_repeticao.append(chave_de_acesso)
                            if not rt_contador:
                                autor_da_rt, rt = acaoComum.copiar_RT()
                                dono_da_rt.append(autor_da_rt)
                                rt_contador.append(rt)
                            acaoComum.pular_processo()
                            sem_xml.append(rt_contador[0])
                            return operar_lancamento(pular_processo)
                        estado_do_caixa = acaoComum.filtrar_status()
                        return operar_lancamento(pular_processo)
                    
                    else:
                        clicar_novamente = utils.encontrar_centro_imagem(r'Imagens\ReferenciaXMLPendente.png')
                        if type(clicar_novamente) == tuple:
                            ptg.doubleClick(x,y)
                        else:
                            break

            estado_do_caixa = acaoComum.filtrar_status()
            return operar_lancamento(pular_processo)
        
        
        elif controlador == "Copie a chave de acesso 1" or controlador == "Copie a chave de acesso 2":
            chave_de_acesso, processo_feito_errado = acaoComum.copiar_chave_acesso()

            if processo_feito_errado == True or controlador == "Copie a chave de acesso 2":
                try:
                    verificador = controle_de_repeticao.index(chave_de_acesso)
                except:
                    controle_de_repeticao.append(chave_de_acesso)
                    if not rt_contador:
                        autor_da_rt, rt = acaoComum.copiar_RT(passos=4)
                        dono_da_rt.append(autor_da_rt)
                        rt_contador.append(rt)
                    try:
                        verificador = pular_processo.index(chave_de_acesso)
                    except:
                        chave_inconforme.append(rt_contador[0])
                    pular_processo.append(chave_de_acesso)
                    acaoComum.pular_processo()
                    return operar_lancamento(pular_processo)
            
            try:
                verificador = pular_processo.index(chave_de_acesso)
                try:
                    verificador = controle_de_repeticao.index(chave_de_acesso)
                    ptg.press(["tab"]*7, interval=0.1)
                    sleep(1)
                    ptg.press("enter", interval=1)
                    utils.repetir_botao()
                    if rt_contador:
                        utils.enviar_email(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                    return
                
                except:
                    acaoComum.pular_processo()
                    controle_de_repeticao.append(chave_de_acesso)
                    return operar_lancamento(pular_processo)
                
            except ValueError:
                caminho = "C:\\Users\\User\\OneDrive - EQS Engenharia Ltda\\Área de Trabalho\\Mariquinha\\xmlFiscalio\\" + chave_de_acesso + ".xml"
                path = Path(caminho)

                if not path.exists():
                    pular_processo.append(chave_de_acesso)
                    controle_de_repeticao.append(chave_de_acesso)
                    if not rt_contador:
                        autor_da_rt, rt = acaoComum.copiar_RT(passos=4)
                        dono_da_rt.append(autor_da_rt)
                        rt_contador.append(rt)
                    acaoComum.pular_processo()
                    sem_xml.append(rt_contador[0])
                    return operar_lancamento(pular_processo)
                
                x, y = utils.clicar_2x(r'Imagens\BotaoSolicitarXML.png')

                while True:
                    solicitar_xml = utils.encontrar_imagem(r'Imagens\ReferenciaXMLAindaNaoSolicitado.png')
                    solicitar_xml2 = utils.encontrar_imagem(r'Imagens\ReferenciaXMLAindaNaoSolicitado2.png')
                    if type(solicitar_xml) == pyscreeze.Box or type(solicitar_xml2) == pyscreeze.Box:
                        break

                ptg.press("enter", interval=1)
                ptg.press("tab")
                copy(caminho)
                ptg.hotkey("ctrl", "v")
                sleep(0.7)
                ptg.hotkey(["shift", "tab"]*2, interval=0.4)
                ptg.press("enter", interval=2)

                erro_de_xml = utils.encontrar_imagem(r'Imagens\ErroNaImportacaoDoXML.png')
                if type(erro_de_xml) == pyscreeze.Box:
                    ptg.press("enter")
                    pular_processo.append(chave_de_acesso)
                    controle_de_repeticao.append(chave_de_acesso)
                    if not rt_contador:
                        autor_da_rt, rt = acaoComum.copiar_RT()
                        dono_da_rt.append(autor_da_rt)
                        rt_contador.append(rt)
                    acaoComum.pular_processo()
                    sem_xml.append(rt_contador[0])
                    return operar_lancamento(pular_processo)
                
                estado_do_caixa = acaoComum.filtrar_status()
                return operar_lancamento(pular_processo)
            

        else:
            # controlador == "Lançar DANFE":
            chave_de_acesso, processo_feito_errado = acaoComum.copiar_chave_acesso()
            estado_do_caixa = chave_de_acesso

            if estado_do_caixa == True:
                x, y = utils.clicar_finalizar()
                finalizar, ainda_tem_processo_pendente = acaoComum.insistir_ate_encontrar(x, y)

                if type(ainda_tem_processo_pendente) == tuple:
                    utils.tratar_processos_pendentes()
                    if rt_contador:
                        utils.enviar_email(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                    return
                
                if type(finalizar) == tuple:
                    ptg.press("enter")
                utils.aguardar()
                utils.clicar_botao_sair()
                if rt_contador:
                    utils.enviar_email(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                return
            

            try:
                verificador = pular_processo.index(chave_de_acesso)
                try:
                    verificador = controle_de_repeticao.index(chave_de_acesso)
                    ptg.press(["tab"]*7, interval=0.5)
                    sleep(2)
                    ptg.press("enter", interval=1)
                    utils.repetir_botao()
                    if rt_contador:
                        utils.enviar_email(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                    return
                
                except:
                    acaoComum.pular_processo()
                    controle_de_repeticao.append(chave_de_acesso)
                    return operar_lancamento(pular_processo)
                
            except:
                caminho = "C:\\Users\\User\\OneDrive - EQS Engenharia Ltda\\Área de Trabalho\\Mariquinha\\xmlFiscalio\\" + chave_de_acesso + ".xml"
                path = Path(caminho)
                if not path.exists():
                    controle_de_repeticao.append(chave_de_acesso)
                    pular_processo.append(chave_de_acesso)
                    if not rt_contador:
                        autor_da_rt, rt = acaoComum.copiar_RT(passos=4)
                        dono_da_rt.append(autor_da_rt)
                        rt_contador.append(rt)
                    acaoComum.pular_processo()
                    sem_xml.append(rt_contador[0])
                    return operar_lancamento(pular_processo)
           

            estado_do_caixa = acaoComum.clicar_Lancar()

            if estado_do_caixa == "NF já lançada":
                controle_de_repeticao.append(chave_de_acesso)
                pular_processo.append(chave_de_acesso)
                ptg.press("tab", interval=0.3)
                ptg.press("enter", interval=0.5)
                if not rt_contador:
                    autor_da_rt, rt = acaoComum.copiar_RT(passos=1)
                    dono_da_rt.append(autor_da_rt)
                    rt_contador.append(rt)
                nf_ja_lancada.append(rt_contador[0])
                acaoComum.pular_processo()
                return operar_lancamento(pular_processo)
            
            if estado_do_caixa == True:
                x, y = utils.clicar_finalizar()
                finalizar, ainda_tem_processo_pendente = acaoComum.insistir_ate_encontrar(x, y)

                if type(ainda_tem_processo_pendente) == tuple:
                    utils.tratar_processos_pendentes()
                    if rt_contador:
                        utils.enviar_email(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                    return
                
                if type(finalizar) == tuple:
                    ptg.press("enter")
                utils.aguardar()
                utils.clicar_botao_sair()
                if rt_contador:
                    utils.enviar_email(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                return
            

            else:
                nome_fantasia_forn, itens, indices_e_impostos = acaoComum.extrair_dados_XML(caminho)

                tela_de_lancamento = utils.encontrar_imagem(r'Imagens\ReferenciaDocumentoEntrada.png')
                while type(tela_de_lancamento) != pyscreeze.Box:

                    acaoComum.verificar_cadastro_forn(nome_fantasia_forn)

                    tela_de_lancamento = utils.encontrar_imagem(r'Imagens\ReferenciaDocumentoEntrada.png')
                    utils.lancar_retroativo()

                    tela_de_lancamento = utils.encontrar_imagem(r'Imagens\ReferenciaDocumentoEntrada.png')
                    tela_bloqueio = utils.encontrar_imagem(r'Imagens\ReferenciaBloqueioGenerico.png')
                    if type(tela_bloqueio) == pyscreeze.Box:
                        pular_processo.append(chave_de_acesso)
                        controle_de_repeticao.append(chave_de_acesso)
                        ptg.press("enter", interval=1)
                        utils.aguardar1()
                        cc_bloqueado = utils.encontrar_imagem(r'Imagens\ReferenciaCCBloqueado.png')
                        if type(cc_bloqueado) == pyscreeze.Box:
                            ptg.press("enter", interval=0.5)
                            acaoComum.rejeitar_caixa()
                            return
                        prod_bloq = utils.encontrar_centro_imagem(r'Imagens\ErroProdutoBloqueado.png')
                        erro_condicao_pag = utils.encontrar_centro_imagem(r'Imagens\ErroCondicaoDePagamento.png')
                        if type(prod_bloq) == tuple or type(erro_condicao_pag) == tuple:
                            ptg.press("enter")
                            sleep(0.5)
                            if not rt_contador:
                                autor_da_rt, rt = acaoComum.copiar_RT(passos=1)
                                dono_da_rt.append(autor_da_rt)
                                rt_contador.append(rt)
                        if type(erro_condicao_pag) == tuple:
                            cond_pag.append(rt_contador[0])
                        elif type(prod_bloq) == tuple:
                            bloqueado.append(rt_contador[0])
                        acaoComum.pular_processo()
                        return operar_lancamento(pular_processo)

                    erro_cnpj = utils.encontrar_centro_imagem(r'Imagens\ErroEsquisito.png')
                    if type(erro_cnpj) == tuple:
                        ptg.press("enter", interval=1)
                        utils.aguardar1()

                    tela_de_lancamento = utils.encontrar_imagem(r'Imagens\ReferenciaDocumentoEntrada.png')
                    erro_sefaz = utils.encontrar_imagem(r'Imagens\ErroNFNaoEncontradaNoSefaz.png')
                    chave_divergente = utils.encontrar_imagem(r'Imagens\ChaveNaoConfereNF.png')
                    if type(erro_sefaz) == pyscreeze.Box or type(chave_divergente) == pyscreeze.Box:
                        pular_processo.append(chave_de_acesso)
                        controle_de_repeticao.append(chave_de_acesso)
                        ptg.press("enter", interval=0.5)
                        tela_bloqueio = utils.esperar_aparecer(r'Imagens\ReferenciaBloqueioGenerico.png')
                        ptg.press("enter", interval=1)
                        utils.aguardar1()
                        erro_condicao_pag = utils.encontrar_centro_imagem(r'Imagens\ErroCondicaoDePagamento.png')
                        if type(erro_condicao_pag) == tuple:
                            ptg.press("enter", interval=0.5)
                        erro_generico = utils.encontrar_centro_imagem(r'Imagens\ErroGenerico.png')   
                        if type(erro_generico) == tuple:
                            ptg.press("enter", interval=0.5)
                        if not rt_contador:
                            autor_da_rt, rt = acaoComum.copiar_RT(passos=1)
                            dono_da_rt.append(autor_da_rt)
                            rt_contador.append(rt)
                        acaoComum.pular_processo()
                        if type(erro_cnpj) == tuple:
                            cnpj_inconclusivo.append(rt_contador[0])
                        elif type(erro_condicao_pag) == tuple:
                            cond_pag.append(rt_contador[0])
                        else:
                            chave_sefaz.append(rt_contador[0])
                        return operar_lancamento(pular_processo)


                    tela_de_lancamento = utils.encontrar_imagem(r'Imagens\ReferenciaDocumentoEntrada.png')
                    erro_ncm = utils.encontrar_centro_imagem(r'Imagens\ErroNCM.png')
                    if type(erro_ncm) == tuple:
                        pular_processo.append(chave_de_acesso)
                        controle_de_repeticao.append(chave_de_acesso)
                        ptg.press("esc", interval=0.7)
                        if not rt_contador:
                            autor_da_rt, rt = acaoComum.copiar_RT(passos=1)
                            dono_da_rt.append(autor_da_rt)
                            rt_contador.append(rt)
                        acaoComum.pular_processo()
                        ncm_problematica.append(rt_contador[0])                        
                        return operar_lancamento(pular_processo)
                    
                    tela_de_lancamento = utils.encontrar_imagem(r'Imagens\ReferenciaDocumentoEntrada.png')
                    
                ptg.press(["tab"]*10)
                sleep(0.6)
                ptg.press(["right"]*8) 


                acaoComum.inserir_valores_da_NF_no_siga(indices_e_impostos, itens)

                acaoComum.finalizar_lancamento()


                estado_do_caixa = acaoComum.filtrar_status()

                if type(estado_do_caixa) == tuple:
                    x, y = utils.clicar_finalizar()
                    finalizar, ainda_tem_processo_pendente = acaoComum.insistir_ate_encontrar(x, y)

                    if type(ainda_tem_processo_pendente) == tuple:
                        utils.tratar_processos_pendentes()
                        if rt_contador:
                            utils.enviar_email(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                        return
                    
                    if type(finalizar) == tuple:
                        ptg.press("enter")
                    utils.aguardar()
                    utils.clicar_botao_sair()
                    if rt_contador:
                        utils.enviar_email(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                    return
                
                controle_de_repeticao.clear()
                return operar_lancamento(pular_processo)

    operar_lancamento(pular_processo)
    sleep(1)