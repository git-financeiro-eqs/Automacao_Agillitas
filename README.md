# Automacao Agillitas

Automação desenvolvida para realizar o lançamento de RTs (Caixas - Demonstrativo de despesas de um operador) no sistema ERP Microsiga. Dentro de uma RT podem ter Recibos e DANFEs, e a automação é preparada para lançar ambos os casos, além de tratar qualquer imprevisto no decorrer desse processo.

---

## 📌 Funcionalidades

- **Lançamento Automático de RTs:** A automação filtra e lança RTs pendentes e parciais.
- **Leitura e Extração de Dados do XML:** A Mariquinha identifica o tipo de registro e processa de acordo com as regras de negócio.
- **Tratamento de Erros e Cadastros Pendentes:** Caso o fornecedor não tenha informações cruciais cadastradas, a automação insere os dados necessários.
- **Diferenciação de Itens com e sem Imposto Retido:** Baseado na leitura do XML, a TES utilizada é ajustada automaticamente.
- **Monitoramento de Status e Finalização do Processo:** A automação verifica o status do lançamento e conclui o processo de acordo com os critérios do sistema.

---

## 🛠 Tecnologias Utilizadas

Este projeto foi desenvolvido utilizando:

- **Python** 🐍
- **PyAutoGUI** - Automação de interface gráfica
- **Pyperclip** - Manipulação da área de transferência
- **OpenCV** - Processamento de imagens
- **xmltodict** - Manipulação de XML

---

## ⚙️ **Pré-requisitos**  
Antes de rodar o projeto, certifique-se de ter instalado:  
- **Python 3.x**    
- **ERP TOTVS Microsiga** instalado e acessível 
<br/>

## 📥 **Instalação**  

1. **Clone este repositório**  
   ```sh
   https://github.com/git-financeiro-eqs/Automacao_Agillitas.git
   ```
   
2. **Crie um ambiente virtual (opcional, mas recomendado)**  
   ```sh
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```
   
3. **Instale as dependências**  
   ```sh
   pip install -r requirements.txt
   ```
<br/>  

---

## 🚀 **Como Executar**  

1. Certifique-se de que o **ERP Microsiga está acessível e já logado**. O Microsiga precisa estar aberto na tela principal da rotina **IntAgillitas**.  
2. Coloque os **arquivos XML** das notas na pasta configurada como **repositório**.
   
   2.1. Configure o repositório de XMLs:  
        - Crie uma pasta para armazenar os XMLs das notas fiscais.  
        - Atualize o caminho da pasta no código, se necessário.  
        - É preciso sempre inserir os XMLs na pasta repositório, essa é a unica forma de alimentar a automação.
          Essa tarefa pode ser feita uma vez por mês, pegando os XMLs do mês anterior e os salvando na pasta chamada xmlFiscalio.
          Eu utilizo o software Fiscal.io para realizar a busca e o Download dos arquivos XMLs desejados.
   
4. **Execute o script principal**:  
   ```sh
   python main.py
   ```
5. As demais ações o próprio Bot irá te ensinar.
<br/>

## **Observações**  

1. A automação envia a RT que, por algum motivo não foi completamente lançada, por E-mail para o grupo Gestão de Caixas.

2. *Para um melhor entendimento do funcionamento do Bot, deixei um vídeo na pasta *docs* dele em ação.

---

🚀 **Automação para tornar os lançamentos mais eficientes e sem erros!**
