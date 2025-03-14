# Arquitetura do Projeto

Este documento descreve a arquitetura do projeto **Automação Agillitas**, explicando a organização dos módulos, suas responsabilidades e como eles interagem entre si.

---

## Visão Geral

O projeto **Automação Agillitas** foi desenvolvido para automatizar o lançamento de RTs (Recibos e Danfes) no sistema ERP Microsiga. A automação é dividida em dois modos principais de operação:

1. **mariquinhaCorrente**: Realiza o lançamento sequencial de RTs pendentes ou parciais.
2. **mariquinhaUnitária**: Realiza o lançamento de uma RT específica, definida pelo operador.

A automação é composta por **10 módulos**, cada um com responsabilidades específicas, que trabalham em conjunto para garantir o funcionamento correto do sistema.

---

## Módulos do Projeto

Abaixo estão os módulos que compõem o sistema, com suas responsabilidades e interações:

<table>
  <thead>
    <tr>
      <th>Módulo</th>
      <th>Responsabilidade</th>
      <th>Funcionalidades</th>
      <th>Interações</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>acaoComum</strong></td>
      <td>Fornece funções compartilhadas pelos módulos <strong>mariquinhaCorrente</strong> e <strong>mariquinhaUnitária</strong>.</td>
      <td>
        <ul>
          <li>Ações comuns, como posicionar o cursor em pontos específicos da interface.</li>
          <li>Funções para filtrar RTs, solicitar XMLs, copiar chaves de acesso e tratar erros.</li>
        </ul>
      </td>
      <td>Utilizado por <strong>mariquinhaCorrente</strong> e <strong>mariquinhaUnitária</strong> para evitar duplicação de código.</td>
    </tr>
    <tr>
      <td><strong>extratorXML</strong></td>
      <td>Extrai e processa os dados dos XMLs das notas fiscais.</td>
      <td>
        <ul>
          <li>Leitura de XMLs para validação de valores e aplicação de TES (154 ou 155).</li>
          <li>Coleta de informações como valores totais, impostos e detalhes dos itens.</li>
        </ul>
      </td>
      <td>Utilizado pelos módulos de lançamento (<strong>mariquinhaCorrente</strong> e <strong>mariquinhaUnitária</strong>) para processar Danfes.</td>
    </tr>
    <tr>
      <td><strong>gui</strong></td>
      <td>Interface gráfica da automação.</td>
      <td>
        <ul>
          <li>Permite ao usuário interagir com a automação, selecionar modos de operação e configurar parâmetros.</li>
        </ul>
      </td>
      <td>Comunica-se com o módulo <strong>main</strong> para iniciar a execução.</td>
    </tr>
    <tr>
      <td><strong>main</strong></td>
      <td>Executa o programa e abre a interface gráfica.</td

                                                          
---

## Diagrama de Arquitetura

Aqui está um diagrama que mostra como os módulos se relacionam:


[main] -> [gui] -> [mariquinhaCorrente] <-> [acaoComum]
[main] -> [gui] -> [mariquinhaUnitária] <-> [acaoComum]
[mariquinhaCorrente] <-> [extratorXML] <-> [operadoresLancamento]
[mariquinhaUnitária] <-> [extratorXML] <-> [operadoresLancamento]
[tratamentoItem] <-> [mariquinhaCorrente] e [mariquinhaUnitária]
[utils] <- Todos os módulos
[mensagens] <- Todos os módulos

---

## Fluxo de Execução

1. O módulo **main** inicia o programa e carrega a interface gráfica (**gui**).
2. O usuário seleciona o modo de operação (**mariquinhaCorrente** ou **mariquinhaUnitária**).
3. Dependendo do modo selecionado, o módulo correspondente inicia o processamento das RTs.
4. Durante o lançamento, os módulos **extratorXML** e **operadoresLancamento** são utilizados para validar e processar os dados.
5. O módulo **tratamentoItem** é acionado caso haja itens fracionados.
6. Todas as mensagens e logs são gerenciados pelos módulos **mensagens** e **utils**.
7. O processo se repete até que todas as RTs sejam processadas.

---

## Detalhes Técnicos

### **mariquinhaCorrente**
- Realiza o lançamento sequencial de RTs pendentes ou parciais.
- Utiliza funções do módulo **acaoComum** para ações comuns, como filtrar RTs e tratar erros.
- Envia e-mails para notificar problemas durante o lançamento.

### **mariquinhaUnitária**
- Realiza o lançamento de uma RT específica, definida pelo operador.
- Utiliza funções do módulo **acaoComum** para ações comuns, como solicitar XMLs e copiar chaves de acesso.
- Envia e-mails para notificar problemas durante o lançamento.

### **utils**
- Fornece funções utilitárias, como formatação de dados, manipulação de strings e envio de e-mails.
- Utilizado por todos os módulos para tarefas genéricas.

---

## Conclusão

A arquitetura do projeto **Automação Agillitas** foi projetada para ser modular e flexível, permitindo a reutilização de código e a fácil manutenção. Cada módulo tem uma responsabilidade clara, e a interação entre eles é bem definida, garantindo um fluxo de trabalho eficiente e confiável.

---
