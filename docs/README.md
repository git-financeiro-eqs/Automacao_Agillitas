# Bot em execução
<br/>
<br/>


https://github.com/user-attachments/assets/61cbee0c-9ee4-4faa-bfd9-d7d2e25f33a6

<br/>
<br/>
Essa primeira parte demonstra a tela inicial da rotina IntAgilitas, é nessa tela que fazemos os filtros de RTs. As RTs que podem ser lançadas pela
Mariquinha são as pendentes e as parciais. A mariquinhaCorrente só lança as parciais, enquanto a mariquinha unitária pode lançar em qualquer uma dessas 
duas possibilidades. No caso deste vídeo demonstrativo, a Mariquinha está sendo executada no modo mariquinhaUnitária, ou seja, ela está lançando uma RT previamente definida pelo operador.
<br/>


https://github.com/user-attachments/assets/17f2fb79-335c-4644-bf2e-05cfa20c291b

<br/>
<br/>
Aqui é como a Mariquinha realiza o lançamento de uma NF. Após ela ter clicado no botão "Solicitar XML", mudando o status do processo para "DS-DISPONIVEL", ela faz uma nova varredura para coletar o Status XML do registro imediato (O que está em azul). Identificando que está como "DS-DISPONIVEL", a Mariquinha inicia o lançamento. Nesse momento em que ela está aguardando a tela de lançamento aparecer, ela também está monitorando o surgimento de possíveis erros que podem acontecer, ou, se a tela de cadastro de fornecedor irá aparecer. Tem alguns fornecedores que não tem em seu cadastro algumas informações cruciais como um código de natureza pré-definida (sempre 2020087), um nome fantasia, e nem a informação se ele é contribuinte ou não, nos casos da falta desses dados, a tela da rotina de cadastro de fornecedores surge para que façamos as inserções. A Mariquinha monitora o possível surgimento dessa tela e, caso ela surja, insere as informações conforme está programado. No vídeo isso não aconteceu, o fornecedor já estava com esses dados cadastrados, então o sistema abriu a tela de lançamento. Assim que a Mariquinha percebe que está na tela de lançamento,
ela começa o seu trabalho verificando se o valor total do item corresponde ao da NF. Assim como no Bot de lançamento de Documentos de Entrada, a Mariquinha também é capaz de ler o XML das notas fiscais. Ela valida o valor total e insere a TES conforme os dados extraídos do XMl. Caso o item tenha algum imposto retido, a Mariquinha usa a TES 155, caso contrario, ela usa a TES 154.
Feito essa etapa nos itens. Ela tecla 'CTRL + S' e salva o lançamento. Aguarda um ultima tela que pode ou não surgir e vai para o próximo lançamento.
<br/>


https://github.com/user-attachments/assets/bb157bce-15f5-4953-884c-38e555d8a2c4

<br/>
<br/>
Aqui a Mariquinha irá iniciar o próximo lançamento dessa RT, que é um registro de Recibo. Registros do tipo Recibo são lançados todos de uma vez. Isso significa que se você lançar um deles, estará lançando todos ao mesmo tempo, como acontece no vídeo. Primeiro, a Mariquinha clicou duas vezes na primeira coluna para filtrar o registro imediato, deixando na posição um registro com status "PENDENTE"; depois, ela verificou a coluna Status XML e identificou que era um registro do tipo Recibo. Registros do tipo Recibo não precisam de nenhum procedimento além do simples clicar no botão "Lancar Nota". Então a Mariquinha, após o clique, aguarda que surja uma tela final para finalizar o lançamento. Aqui, poucas coisas podem dar errado. A possibilidade mais temida é a do Centro de Custo estar bloqueado, mas esse não foi o caso. Depois de finalizado o lançamento de mais um registro, ela clica no cabeçalho da primeira coluna mais uma vez a procura de um registro que esteja com Status "PENDENTE". Como ela acaba não encontrando pois já havia lançado todos, ela então parte para finalizar o Caixa. Caso ela estivesse no modo mariquinhaCorrente em vez do mariquinhaUnitaria, ela reiniciaria todo o processo de filtrar os registros com base no valor, e iniciaria o próximo lançamento.

