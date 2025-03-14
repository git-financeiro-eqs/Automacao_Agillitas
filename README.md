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

## 🚀 Demonstração da Automação em Execução

### 📌 Tela Inicial da Rotina IntAgilitas

A tela inicial onde são feitos os filtros de RTs. A automação pode operar em dois modos:
- **MariquinhaCorrente**: Lança apenas as RTs parciais.
- **MariquinhaUnitária**: Lança RTs pendentes e parciais, conforme definido pelo operador.

![Tela Inicial](https://github.com/user-attachments/assets/61cbee0c-9ee4-4faa-bfd9-d7d2e25f33a6)

### 📌 Lançamento de uma Nota Fiscal (NF)

Após solicitar o XML, a automação verifica o status e inicia o lançamento. Durante esse processo:
- Monitora erros e possíveis telas emergentes.
- Insere dados ausentes no cadastro do fornecedor, se necessário.
- Valida o valor total e seleciona a TES apropriada.
- Salva o lançamento e aguarda a próxima etapa.

![Lançamento de NF](https://github.com/user-attachments/assets/17f2fb79-335c-4644-bf2e-05cfa20c291b)

### 📌 Lançamento de um Recibo

No caso de registros do tipo Recibo:
- A automação identifica o tipo do registro e clica no botão "Lançar Nota".
- Aguarda a tela de confirmação para finalizar o lançamento.
- Se estiver no modo **MariquinhaCorrente**, reinicia o processo e busca novos registros.

![Lançamento de Recibo](https://github.com/user-attachments/assets/bb157bce-15f5-4953-884c-38e555d8a2c4)

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
   git clone https://github.com/git-financeiro-eqs/Automacao_Documento_de_Entrada.git
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


## 📌 Como Usar

1. Inicie a automação e selecione o modo desejado.
2. A Mariquinha iniciará o processamento dos registros pendentes.


🚀 **Automação para tornar os lançamentos mais eficientes e sem erros!**
