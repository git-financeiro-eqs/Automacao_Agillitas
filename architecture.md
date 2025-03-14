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

### 1. **acaoComum**
- **Responsabilidade**: Fornece funções compartilhadas pelos módulos **mariquinhaCorrente** e **mariquinhaUnitária**.
- **Funcionalidades**:
  - Ações comuns, como posicionar o cursor em pontos específicos da interface.
  - Funções para filtrar RTs, solicitar XMLs, copiar chaves de acesso e tratar erros.
- **Interações**:
  - Utilizado por **mariquinhaCorrente** e **mariquinhaUnitária** para evitar duplicação de código.

### 2. **extratorXML**
- **Responsabilidade**: Extrai e processa os dados dos XMLs das notas fiscais.
- **Funcionalidades**:
  - Leitura de XMLs para validação de valores e aplicação de TES (154 ou 155).
  - Coleta de informações como valores totais, impostos e detalhes dos itens.
- **Interações**:
  - Utilizado pelos módulos de lançamento (**mariquinhaCorrente** e **mariquinhaUnitária**) para processar Danfes.

### 3. **gui**
- **Responsabilidade**: Interface gráfica da automação.
- **Funcionalidades**:
  - Permite ao usuário interagir com a automação, selecionar modos de operação e configurar parâmetros.
- **Interações**:
  - Comunica-se com o módulo **main** para iniciar a execução.

### 4. **main**
- **Responsabilidade**: Executa o programa e abre a interface gráfica.
- **Funcionalidades**:
  - Inicializa a automação e carrega a interface gráfica.
- **Interações**:
  - Depende do módulo **gui** para exibir a interface ao usuário.

### 5. **mariquinhaCorrente**
- **Responsabilidade**: Realiza o lançamento sequencial de RTs.
- **Funcionalidades**:
  - Processa RTs parciais de forma contínua.
  - Utiliza funções do módulo **acaoComum** para ações compartilhadas.
- **Interações**:
  - Comunica-se com **extratorXML** para processar Danfes e com **operadoresLancamento** para validações.

### 6. **mariquinhaUnitária**
- **Responsabilidade**: Realiza o lançamento de uma única RT.
- **Funcionalidades**:
  - Processa uma RT específica, definida pelo usuário.
  - Utiliza funções do módulo **acaoComum** para ações compartilhadas.
- **Interações**:
  - Comunica-se com **extratorXML** para processar Danfes e com **operadoresLancamento** para validações.

### 7. **mensagens**
- **Responsabilidade**: Contém mensagens de apresentação e instruções para o usuário.
- **Funcionalidades**:
  - Exibe mensagens informativas e de erro durante a execução.
- **Interações**:
  - Utilizado por todos os módulos que precisam exibir informações ao usuário.

### 8. **operadoresLancamento**
- **Responsabilidade**: Fornece funções utilitárias para conferência e validação dos valores da NF.
- **Funcionalidades**:
  - Compara valores da NF com os valores apresentados na tela de lançamento do SIGA.
- **Interações**:
  - Utilizado pelos módulos **mariquinhaCorrente** e **mariquinhaUnitária** durante o lançamento.

### 9. **tratamentoItem**
- **Responsabilidade**: Trata itens que foram fracionados durante o lançamento.
- **Funcionalidades**:
  - Aplica razão e proporção aos valores de itens fracionados.
- **Interações**:
  - Utilizado pelos módulos de lançamento para garantir a precisão dos valores.

### 10. **utils**
- **Responsabilidade**: Fornece funções utilitárias para todos os módulos do sistema.
- **Funcionalidades**:
  - Funções genéricas, como formatação de dados, cálculos e manipulação de strings.
- **Interações**:
  - Utilizado por todos os módulos que precisam de funcionalidades comuns.

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
