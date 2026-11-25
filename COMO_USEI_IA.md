# Como utilizei a Inteligência Artificial no desenvolvimento do projeto

## 1. Ferramentas utilizadas

- **Claude:** utilizado principalmente como tutor durante o desenvolvimento do projeto, auxiliando na compreensão de conceitos de Python, SQL, Git, testes e ETL. Minha utilização foi baseada mais em perguntas, explicações, pseudocódigos e discussão de alternativas. Muitos assuntos de SQL, por exemplo, eu já tinha uma boa base vindo da faculdade, então usei mais como tira dúvidas. Em vez de solicitar soluções completas, no caso da linguagem python, que não tenho tanto conhecimento, eu mostrei o problema e pedi explicações sobre como poderia resolvê-lo, usando bastante pseudocodigo. Depois de entender a lógica, desenvolvia minha própria implementação, testava e mandava pro Claude, sinceramente, sempre havia erros a serem corrijigos. 

## 2. Como defini o escopo de utilização

Tentei usar a IA como uma ferramenta de apoio ao aprendizado, e não como substituta pra fazer o código por mim. Minha abordagem era trabalhar uma funcionalidade por vez, entender primeiro o problema, solicitar explicações ou pseudocódigos e então partir para a implementação.

Em vários momentos, também pedi que a IA apresentasse outras possibilidades além da primeira solução que ela trás. Isso fez com que eu tivesse a liberdade para comparar soluções e daí entender suas vantagens e desvantagens, e só então tomar minhas próprias decisões sobre o que seria mais adequado ao projeto.

## 3. Exemplos de utilização e decisões próprias

### 1. Estrutura da extração de dados

- **O que discuti com a IA:** como organizar a extração de dados da API sem precisar repetir código e deixando a implementação mais fácil de manter.
- **Alternativas discutidas:** conversamos sobre duas possibilidades, criar uma lógica de extração para cada recurso ou desenvolver uma função genérica que pudesse ser reutilizada.
- **Minha decisão:** como eu já tinha me deparado com uma situação parecida em uma atividade da faculdade, na qual trabalhei com funções e reutilização de código, achei que seria interessante seguir por esse caminho. Mesmo assim, preferi começar fazendo a extração apenas para clientes, para entender melhor como funcionavam a API e a paginação. Depois que consegui compreender e testar essa primeira parte, decidi adaptar o código para uma função genérica extrair(rota), que pudesse ser utilizada para diferentes recursos.
- **Como validei:** executei a extração e comparei a quantidade de registros retornados com os resultados esperados. Também testei a função com outras rotas para verificar se a estrutura funcionava corretamente em diferentes situações.

### 2. Estratégia de idempotência do ETL

- **O que discuti com a IA:** como garantir que executar o ETL mais de uma vez não causasse duplicação ou inconsistência nos dados.
- **Alternativas discutidas:** de inicio, a IA sugeriu limpar e recarregar os dados. Para entender se essa seria realmente a melhor opção, pedi que apresentasse outras possibilidades, como INSERT OR IGNORE, upsert e recriação do banco.
- **Minha decisão:** depois de comparar as opções, escolhi limpar e recarregar os dados. Entendi que essa estratégia atendia melhor ao projeto, pois o INSERT OR IGNORE, por exemplo, não atualizaria registros caso alguma informação fosse modificada na origem.
- **Como validei:** executei o ETL mais de uma vez e conferi se os dados continuavam consistentes, sem registros duplicados.

## 4. Sugestões não utilizadas e decisões independentes

### 1. Organização da extração de dados
Durante o desenvolvimento da extração, o Claude sugeriu algumas formas de organizar a busca dos dados na API. 

Uma das opções sugeridas era criar uma função diferente para cada tipo de dado que eu precisava buscar. Porém, preferi não seguir por esse caminho, pois isso poderia gerar repetição de código.

Optei por utilizar uma função genérica, que pudesse atender aos diferentes recursos. Comecei testando a extração de clientes e depois utilizei a mesma estrutura para os outros recursos. Conferi as quantidades retornadas para garantir que estava funcionando corretamente.

### 2. Organização das consultas e dos valores de vendas

Durante o desenvolvimento das consultas SQL, surgiu a possibilidade de utilizar valor_total para calcular as vendas por mês. Entretanto, ao trabalhar com os dados e conferir os valores na reconciliação, percebi que essa coluna apresentava divergências em alguns pedidos. Por isso, preferi utilizar valor_itens, que estava mais alinhada aos cálculos que eu já havia realizado no projeto.

Ao comparar os resultados, identifiquei que 238 pedidos apresentavam diferenças entre o valor total informado e a soma dos itens. Depois, conferi se a soma das vendas mensais correspondia ao total da reconciliação, chegando a R$ 311.228,75 em ambos os casos.


## 5. Falhas, limitações e retrabalho

Apesar de ter ajudado bastante durante o desenvolvimento, nem sempre as orientações da IA estavam de acordo com o que já existia no projeto. Por isso, precisei conferir as sugestões antes de fazer alterações.

Um exemplo aconteceu durante a configuração do .gitignore. A IA sugeriu adicionar a linha __pycache__/ para ignorar essa pasta, mas ela já estava presente no arquivo. Acabei duplicando a linha e quanfo fui corrigir, removi as duas ocorrências sem perceber. Só notei o problema quando a pasta voltou a aparecer como modificada no VS Code. Depois, restaurei a configuração.

Também enfrentei alguns erros durante a programação, como problemas na formatação de datas, na paginação da API e na indentação de funções. Em alguns casos, o código até executava, mas os resultados não eram os esperados. Isso aconteceu, por exemplo, quando utilizei pages em vez de page no endereço da API. Como o parâmetro estava incorreto, a API continuava retornando a primeira página, sem apresentar um erro evidente. Percebi o problema ao comparar o endereço utilizado com o comando que havia testado no terminal.

Outra dificuldade foi entender que nem sempre a ausência de erros significa que o resultado está correto. Durante o desenvolvimento, precisei comparar contagens, conferir valores e executar os testes para identificar problemas que não apareciam apenas ao rodar o programa.

Essas situações reforçaram alguns cuidados importantes:

- Não confiar automaticamente em uma resposta, mesmo quando parece correta.
- Conferir o código existente antes de aplicar uma alteração sugerida.
- Executar testes para verificar se a solução realmente funciona.
- Comparar os resultados obtidos com os dados esperados.

## 6. IA como ferramenta de aprendizado

Desde o início do projeto, deixei claro no meu primeiro prompt que queria utilizar a IA como uma orientadora e não como alguém que desenvolvesse o trabalho por mim. 

Pedi que ela agisse como uma espécie de professora, explicando os conteúdos, me dando analogias e que em hipotese alguma me mandasse o código completo. Queria entender o que estava fazendo e conseguir desenvolver as funcionalidades por conta própria.

Ela me ajudou bastante com Python e ETL, que eram áreas em que eu ainda tinha/tenho algumas dificuldades. Já em SQL, eu tinha uma base melhor, então a IA acabou sendo mais um apoio para tirar dúvidas que surgiam durante o desenvolvimento.

Também precisei de bastante orientação em Git e GitHub, principalmente com os comandos e a configuração do ambiente, além dos testes com pytest, que eu ainda não dominava muito bem. Nesses momentos, a IA me explicava o que cada comando fazia e como utilizá-lo.

No geral, utilizei a IA para esclarecer dúvidas, entender erros e com muito, mas muito pseudocodigo. Muitas vezes, pedia primeiro uma explicação ou codigo parecido sem relação como conteúdo (que fosse mais simples) pra de fato entender a lógica, tentava fazer a implementação sozinha. Quando algo não funcionava (aconteceu muito) voltava a pedir ajuda.

Acredito que essa foi a parte mais importante da utilização da IA no projeto, ter um apoio durante o aprendizado, de fato um orientador que eu podia consultar a qualquer momento, mas sem deixar de participar ativamente do desenvolvimento.

**Conclusão:** 

Desde o início, ficou muito claro que a IA deveria me ajudar durante todo o desenvolvimento, mas que em hipótese alguma, fazer o projeto por mim. Essa orientação foi considerada desde o primeiro prompt no Claude, quando coloquei que queria usar a IA como orientadora, para que explicasse os conteúdos, apresentasse diferentes possibilidades e principalmente me ajudasse a entender os problemas finais, sem simplesmente entregar o código pronto.

Durante o projeto a IA apresentou diferentes caminhos e soluções que eu poderia seguir. Mas para escolher entre eles, eu precisava entender como cada um funcionava e qual fazia mais sentido para o que eu precisava naquele momento. Muitas vezes, ela explicava a lógica por trás de uma função ou de um comando e, a partir dessa explicação, eu conseguia desenvolver minha própria implementação, trabalhando também a minha autonomia.

Esse processo me ajudou bastante, principalmente em conteúdos que eu ainda não dominava, como Python e ETL. Também passei a compreender melhor os comandos de Git e GitHub. No início, tinha bastante dificuldade e precisava consultar a IA com frequência, mas, de tanto repetir os comandos e entender para que cada um servia, fui conseguindo fazer, meio que aprendendo ali na repetição. c

Com a prática e as explicações, também comecei a reconhecer melhor os erros apresentados no terminal, entender o que eles significavam e identificar como poderia corrigir

Acredito que a IA não contribuiu apenas para a conclusão do projeto, mas principalmente para o meu aprendizado. Hoje sinto que tenho mais autonomia para trabalhar com esses conteúdos, interpretar problemas, compreender o código e buscar soluções, em vez de simplesmente utilizar aquilo que a IA me apresenta. Sei que ainda tenho muito a aprender, mas consigo perceber o quanto evoluí em relação ao que sabia antes de começar o projeto.