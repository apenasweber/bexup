# Sistema de Veículos

Este sistema é composto por duas APIs principais que interagem com o serviço da FIPE para obter informações sobre veículos. O sistema também utiliza filas para processamento assíncrono.

## Rodando a aplicação

1.  `git clone git@github.com:apenasweber/bexup.git`
2.  `cd bexup`
3.  Renomeie `".env-example"` para `".env"`
4.  Com make você pode rodar os testes unitários: `make test`. Você pode também usar make up para subir a aplicação e make down para derrubar a aplicação.
5.  Após usar o `make up` , acesse [http://localhost:8000/docs](http://localhost:8000/docs) para testar os endpoints manualmente.
6.  Clique no endpoint /login
7.  Clique em "Try it out"
8.  Insira username(username) e password(password) e clique em EXECUTE.
9.  Você vai receber o token, copie-o.
10. No topo da página, do lado direito, clique em "Authorize" e cole o token ali.
11. Agora você pode usar todos os endpoints autenticados (20 minutos de expiração do token).

## API-1

### Descrição:

A API-1 é responsável por:

- Acionar a carga inicial dos dados de veículos.
- Buscar as marcas no serviço da FIPE.
- Disponibilizar endpoints para buscar marcas, modelos e observações armazenadas no banco de dados.
- Salvar dados alterados dos veículos.

### Endpoints:

- **GET `/car-brands`**: Retorna as marcas de veículos a partir do serviço FIPE.
- **POST `/enqueue-brand/`**: Coloca uma marca específica na fila para processamento pela API-2.
- **POST `/trigger-load-vehicles`**: Dispara o carregamento dos veículos, colocando as marcas em uma fila.
- **POST `/load-vehicles`**: Carrega todos os dados dos veículos (marcas, modelos, anos e valores) a partir do serviço FIPE.

## API-2

### Descrição:

A API-2 é responsável por:

- Processar as marcas recebidas da fila.
- Buscar os códigos e modelos dos veículos no serviço da FIPE com base nas marcas recebidas.
- Salvar no banco de dados NoSQL as informações de código, marca e modelo dos veículos encontrados.

### Endpoints:

- **POST `/process-brand/`**: Processa uma marca específica, obtém detalhes do veículo para essa marca e salva os detalhes em um banco de dados MongoDB.

## Autenticação:

Ambas as APIs utilizam JWT (JSON Web Tokens) para autenticação. Há um endpoint de login na API-1 que emite tokens para autenticação.

## Banco de Dados:

O sistema utiliza dois bancos de dados:

- **PostgreSQL**: Armazena marcas, modelos e outras informações relacionadas a veículos.
- **MongoDB**: Armazena detalhes específicos das marcas processadas pela API-2.

# Boas Práticas no Projeto

Neste projeto, foram adotadas várias boas práticas de programação e design de software. Aqui está um resumo das principais práticas usadas em diferentes partes do projeto:

## Configurações e Ambiente

- **Arquivo `.env`**: Usado para armazenar configurações sensíveis e específicas do ambiente, como chaves secretas e URLs de banco de dados.
- **Pydantic para Configurações**: Utilizando a biblioteca Pydantic para gerenciar configurações da aplicação, o que oferece validação de tipo e fácil acesso às configurações em toda a aplicação.

## Docker e Containerização

- **Imagem Base Leve**: Usando a versão `3.8-alpine` do Python, que é uma imagem leve e específica.
- **Limpando Cache**: Removendo o cache após a instalação de pacotes para reduzir o tamanho da imagem.
- **Conexões Duráveis**: Ao interagir com o RabbitMQ, garantindo que as mensagens e filas sejam duráveis para resistir a reinicializações do broker.

## Estrutura de Código e Design

- **Organização de Pastas e Arquivos**: Estrutura de diretório clara e modularizada, facilitando a localização e manutenção de componentes específicos.
- **Uso de ORM (SQLAlchemy)**: Permite uma abstração do banco de dados e facilita operações CRUD.
- **Modelagem de Dados**: Modelos claros para usuários e veículos com atributos bem definidos.
- **Hashing de Senhas**: Armazenando senhas como hashes (usando um algoritmo forte) para segurança.
- **Gestão de Dependências**: Usando o padrão de injeção de dependências do FastAPI para gerenciar recursos como sessões de banco de dados.
- **Gerenciamento de Filas**: Uso do RabbitMQ para gerenciamento de mensagens e filas, com funções claramente definidas para enfileiramento e desenfileiramento.

## Segurança

- **Autenticação e Autorização**: Implementando autenticação JWT e utilizando middlewares para proteger endpoints.
- **Gerenciamento de Segredos**: Usando variáveis de ambiente e `.env` para gerenciar segredos.

## Logging e Monitoramento

- **Uso do Módulo `logging`**: Substituindo `print` statements por logs adequados, facilitando o monitoramento e a depuração.
