# Arquitetura do Projeto

Este documento descreve a arquitetura do projeto **Automação Agillitas**, explicando a organização dos módulos, suas responsabilidades e como eles interagem entre si.

---

## Visão Geral

O projeto **Automação Agillitas** foi desenvolvido para automatizar o lançamento de RTs (Recibos e Danfes) no sistema ERP Microsiga. A automação é dividida em dois modos principais de operação:

1. **mariquinhaCorrente**: Realiza o lançamento sequencial de RTs pendentes.
2. **mariquinhaUnitária**: Realiza o lançamento de uma RT específica, definida pelo operador, podendo até lançar RTs baixadas parcialmente.

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
      <td>Executa o programa e abre a interface gráfica.</td>
      <td>
        <ul>
          <li>Inicializa a automação e carrega a interface gráfica.</li>
        </ul>
      </td>
      <td>Depende do módulo <strong>gui</strong> para exibir a interface ao usuário.</td>
    </tr>
    <tr>
      <td><strong>mariquinhaCorrente</strong></td>
      <td>Realiza o lançamento sequencial de RTs.</td>
      <td>
        <ul>
          <li>Processa RTs pendentes de forma contínua.</li>
          <li>Utiliza funções do módulo <strong>acaoComum</strong> para ações compartilhadas.</li>
        </ul>
      </td>
      <td>Comunica-se com <strong>extratorXML</strong> para processar Danfes e com <strong>operadoresLancamento</strong> para validações.</td>
    </tr>
    <tr>
      <td><strong>mariquinhaUnitária</strong></td>
      <td>Realiza o lançamento de uma única RT.</td>
      <td>
        <ul>
          <li>Processa uma RT específica, definida pelo usuário, podendo ser parcial ou não.</li>
          <li>Utiliza funções do módulo <strong>acaoComum</strong> para ações compartilhadas.</li>
        </ul>
      </td>
      <td>Comunica-se com <strong>extratorXML</strong> para processar Danfes e com <strong>operadoresLancamento</strong> para validações.</td>
    </tr>
    <tr>
      <td><strong>mensagens</strong></td>
      <td>Contém mensagens de apresentação e instruções para o usuário.</td>
      <td>
        <ul>
          <li>Manual de uso.</li>
        </ul>
      </td>
      <td>Apresentado assim que o executável da automação é clicado</td>
    </tr>
    <tr>
      <td><strong>operadoresLancamento</strong></td>
      <td>Fornece funções utilitárias para conferência e validação dos valores da NF.</td>
      <td>
        <ul>
          <li>Compara valores da NF com os valores apresentados na tela de lançamento do SIGA.</li>
        </ul>
      </td>
      <td>Utilizado pelos módulos <strong>mariquinhaCorrente</strong> e <strong>mariquinhaUnitária</strong> durante o lançamento.</td>
    </tr>
    <tr>
      <td><strong>tratamentoItem</strong></td>
      <td>Trata itens que foram fracionados durante o lançamento.</td>
      <td>
        <ul>
          <li>Aplica razão e proporção aos valores de itens fracionados.</li>
        </ul>
      </td>
      <td>Utilizado pelos módulos de lançamento para garantir a precisão dos valores.</td>
    </tr>
    <tr>
      <td><strong>utils</strong></td>
      <td>Fornece funções utilitárias para todos os módulos do sistema.</td>
      <td>
        <ul>
          <li>Funções genéricas, formatação de dados, log em E-mail e manipulação de strings, além de movimentações repetitivas.</li>
        </ul>
      </td>
      <td>Utilizado por todos os módulos que precisam de funcionalidades comuns.</td>
    </tr>
  </tbody>
</table>

                                                          
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

## Conclusão

A arquitetura do projeto **Automação Agillitas** foi projetada para ser modular e flexível, permitindo a reutilização de código e a fácil manutenção. Cada módulo tem uma responsabilidade clara, e a interação entre eles é bem definida, garantindo um fluxo de trabalho eficiente e confiável.

---
