# Case Desenvolvedor - ANAC

## Descrição

Este projeto é uma aplicação web desenvolvida em Python utilizando Flask para o backend e Vue.js para o frontend. A aplicação consome dados estatísticos de transporte aéreo da ANAC, processa e filtra essas informações e apresenta os resultados em um gráfico interativo.

## Tecnologias Utilizadas

- **Backend:** Flask (Python)
- **Frontend:** Vue.js
- **Banco de Dados:** PostgreSQL
- **Containers:** Docker

## Estrutura do Projeto

O projeto está dividido em três containers Docker:
1. **Backend (Flask):** Responsável pela autenticação e manipulação dos dados.
2. **Banco de Dados (PostgreSQL):** Armazena os dados filtrados da ANAC.
3. **Frontend (Vue.js):** Interface do usuário.

## Endereços e Portas

A aplicação está hospedada em uma VM no Google Cloud Platform (GCP) com o seguinte IP: `34.30.225.223`.

- **PostgreSQL:** Porta `5432`
- **Backend Flask:** Porta `5000`
- **Frontend Vue.js:** Porta `8080`

Para acessar a VM, utilize a seguinte senha: **'pai amado'**.

## Rotas da API

A API possui os seguintes endpoints:

1. **Autenticação:**
   - `POST /login`
   - **Descrição:** Valida o usuário e a senha.
   - **Usuário Padrão:**
     - **Usuário:** `root`
     - **Senha:** `root#`

2. **Carga de Dados:**
   - `POST /post_anac_statistical`
   - **Descrição:** Alimenta o banco de dados com os dados estatísticos da ANAC.

3. **Filtragem dos Dados:**
   - `POST /post_table_anac_filtered`
   - **Descrição:** Gera uma tabela filtrada a partir dos dados originais, considerando:
     - Companhia aérea: `GOL` (EMPRESA = "GLO")
     - Tipo de voo: `REGULAR` (GRUPO_DE_VOO = "REGULAR")
     - Natureza do voo: `DOMÉSTICA` (NATUREZA = "DOMÉSTICA")
     - Mercado: Agrupamento de origem e destino em ordem alfabética (ex: `SBGRSBSV`).

4. **Consulta de Dados Filtrados:**
   - `GET /get_table_anac_filtered`
   - **Descrição:** Obtém os dados filtrados por paginação para evitar sobrecarga.

## Funcionalidades

- **Autenticação de Usuário:** Acesso seguro com login.
- **Filtragem de Dados:** Selecione os voos com base nos critérios especificados.
- **Gráfico Interativo:** Apresenta o RPK ao longo do tempo.

## Como Executar

1. **Clone o repositório:**
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <NOME_DO_REPOSITORIO>
   ```

2. **Suba os containers Docker:**
   ```bash
   docker-compose up -d
   ```

3. **Acesse a aplicação:**
   - **Login:** `http://34.30.225.223:8080/`
   - **Gráfico:** `http://34.30.225.223:8080/graphic`

## **Importante: Configuração do Arquivo `config.js`**

Antes de rodar a aplicação, é necessário configurar o arquivo `config.js` para que a comunicação entre o frontend (Vue.js) e o backend (Flask) funcione corretamente.

### Passos para configurar:

1. Abra o arquivo `config.js` no diretório do frontend (Vue.js).
2. Altere as variáveis `IP`, `API_PORT`, `PROTOCOL` conforme necessário:
   - `IP`: O endereço IP do seu servidor (pode ser `localhost` ou o IP da VM, por exemplo).
   - `API_PORT`: A porta do backend Flask (normalmente `5000`).
   - `PROTOCOL`: O protocolo a ser utilizado (geralmente `http` ou `https`).
   
### Exemplo de configuração:

```javascript
export const IP = 'localhost';  // Ou o IP da sua VM
export const API_PORT = '5000';  // A porta do Flask
export const PROTOCOL = 'http';  // Ou 'https', se necessário
```

Após realizar essa modificação, salve o arquivo e inicie novamente as três etapas acima.

## Considerações Finais

Este projeto foi desenvolvido para demonstrar habilidades no uso de Flask, Vue.js, PostgreSQL e Docker, além da manipulação de dados estatísticos da ANAC. Ele permite a visualização de dados de transporte aéreo de maneira filtrada e interativa.

---

### **Nota Adicional - Tabelas no PostgreSQL**

Após rodar a aplicação, é necessário criar as seguintes tabelas manualmente no banco de dados PostgreSQL usando o **pgAdmin** ou o comando **psql**:

1. **Tabela ANAC**

```sql
CREATE TABLE ANAC (
    id SERIAL PRIMARY KEY,
    EMPRESA_SIGLA VARCHAR(100),
    EMPRESA_NOME VARCHAR(100),
    EMPRESA_NACIONALIDADE VARCHAR(100),
    ANO VARCHAR(100),
    MES VARCHAR(100),
    AEROPORTO_DE_ORIGEM_SIGLA VARCHAR(100),
    AEROPORTO_DE_ORIGEM_NOME VARCHAR(100),
    AEROPORTO_DE_ORIGEM_UF VARCHAR(100),
    AEROPORTO_DE_ORIGEM_REGIAO VARCHAR(100),
    AEROPORTO_DE_ORIGEM_PAIS VARCHAR(100),
    AEROPORTO_DE_ORIGEM_CONTINENTE VARCHAR(100),
    AEROPORTO_DE_DESTINO_SIGLA VARCHAR(100),
    AEROPORTO_DE_DESTINO_NOME VARCHAR(100),
    AEROPORTO_DE_DESTINO_UF VARCHAR(100),
    AEROPORTO_DE_DESTINO_REGIAO VARCHAR(100),
    AEROPORTO_DE_DESTINO_PAIS VARCHAR(100),
    AEROPORTO_DE_DESTINO_CONTINENTE VARCHAR(100),
    NATUREZA VARCHAR(100),
    GRUPO_DE_VOO VARCHAR(100),
    PASSAGEIROS_PAGOS VARCHAR(100),
    PASSAGEIROS_GRATIS VARCHAR(100),
    CARGA_PAGA_KG VARCHAR(100),
    CARGA_GRATIS_KG VARCHAR(100),
    CORREIO_KG VARCHAR(100),
    ASK VARCHAR(100),
    RPK VARCHAR(100),
    ATK VARCHAR(100),
    RTK VARCHAR(100),
    COMBUSTIVEL_LITROS VARCHAR(100),
    DISTANCIA_VOADA_KM VARCHAR(100),
    DECOLAGENS VARCHAR(100),
    CARGA_PAGA_KM VARCHAR(100),
    CARGA_GRATIS_KM VARCHAR(100),
    CORREIO_KM VARCHAR(100),
    ASSENTOS VARCHAR(100),
    PAYLOAD VARCHAR(100),
    HORAS_VOADAS VARCHAR(100),
    BAGAGEM_KG VARCHAR(100)
);
```

2. **Tabela USERS**

```sql
CREATE TABLE USERS (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    password VARCHAR(100),
    hash TEXT
);
```
### Inserção de Usuário

Após a criação da tabela, você precisa inserir pelo menos um usuário na tabela para que a autenticação funcione. O exemplo a seguir mostra como inserir um usuário com o nome "root" e a senha "root#":

```sql
INSERT INTO USERS (name, password, hash) 
VALUES ('root', 'root#', 'HASH_AQUI');
```

Nota: Substitua 'HASH_AQUI' pelo valor do hash gerado para a senha.
