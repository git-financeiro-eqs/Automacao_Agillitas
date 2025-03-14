
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
