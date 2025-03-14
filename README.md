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

## 📦 Instalação

Para rodar a automação, instale as dependências do projeto utilizando:

```sh
pip install -r requirements.txt
```

---

## 📝 Arquivo `requirements.txt`

O projeto utiliza as seguintes bibliotecas:

```
MouseInfo==0.1.3
numpy==2.2.3
opencv-python==4.11.0.86
pillow==11.1.0
PyAutoGUI==0.9.54
PyGetWindow==0.0.9
PyMsgBox==1.0.9
pyperclip==1.9.0
PyRect==0.2.0
PyScreeze==1.0.1
pytweening==1.2.0
xmltodict==0.14.2
```

---

## 📌 Como Usar

1. Inicie a automação e selecione o modo desejado.
2. A Mariquinha iniciará o processamento dos registros pendentes.
3. Caso seja necessário, insira informações solicitadas pelo sistema.
4. Acompanhe o lançamento das RTs e NF pelo log do processo.

---

## 🛠 Manutenção e Melhorias

Caso precise modificar o código ou adicionar novas funcionalidades, basta editar os módulos principais e atualizar as regras de negócio conforme necessário.

---

## 📞 Contato

Para dúvidas ou sugestões, entre em contato com o desenvolvedor.

---

🚀 **Automação para tornar os lançamentos mais eficientes e sem erros!**
