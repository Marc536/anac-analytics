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

## Considerações Finais

Este projeto foi desenvolvido para demonstrar habilidades no uso de Flask, Vue.js, PostgreSQL e Docker, além da manipulação de dados estatísticos da ANAC. Ele permite a visualização de dados de transporte aéreo de maneira filtrada e interativa.

