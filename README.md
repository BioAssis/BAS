# BAS - Bioprecess Assistant Software

Este repositório online foi desenvolvido a fim de disponibilizar a documentação e as instruções da criação do software online BAS, além disso, qualquer usuário pode utilizar o BAS de forma local, fazendo o download desse repositório e seguindo as instruções dispostas abaixo. O site oficial do software aqui proposto, pode ser acessado clicando em [BAS - Bioprocess Assistant Software](https://baslnbr.streamlit.app).

## Instalação:
Para instalar o BAS de forma local, basta clonar esse repositório para uma pasta conhecida e posteriormente realizar os seguintes passos abaixo, recomenda-se que os passos a seguir sejam realizados dentro de um novo ambiente virtual. o BAS utiliza o *python- versão 3.12.2*, especificada no arquivo `runtime.txt`, certifique-se de utilizar a mesma versão do Python para a criação do novo ambiente virtual para evitar problemas de compatibilidade.
  - Atualizar e instalar as bibliotecas necessaárias:
    ```bash
    pip install -r requirements.txt
    ```

Após instaladas as bibliotecas necessárias, para inicializar o software, entre na pasta "BAS", do repositório clonado, e utilize a seguinte linha de código:
  - Iniciar o BAS:
    ```bash
    streamlit run Pagina_Inicial.py
    ```

## Introdução:

O BAS é um software desenvolvido por alunos da ILUM - Escola de Ciências - voltado para o suporte em bioprocessos com foco no tratamento e extração de informações de perfis de crescimento microbiano, a partir de dados produzidos em larga escala pelo equipamento *Growth Profile*. Esse Git disponibiliza os documentos referentes à construção tanto da interface quanto das função usadas em cada uma das mecânicas que o BAS apresenta. 

## Objetivos: 

O BAS foi desenvolvido com o objetivo principal de propor a acessibiblidade tanto econômica, disponibilizando o código-fonte e todo o site públicamente, quanto interativa, criando uma interface limpa, desenvolvida a fim de direcionar o uso do software, com uma linha de execução direta e clara. Não só isso, o BAS foi criado com o intúito de aumentar rastreabilidade dos resultados, gerando e armazenando informações capazes aumentar a reprodutibilidade das conclusões obtidas. 

## Execução: 

Caso queira utilizar o BAS, para fins de teste da ferramenta ou por curiosidade, esse repositório oferece um conjunto de dados de exemplo, conjunto esse disponibilizado pelo Laboratório Nacional de Biorrenováveis (LNBr), o qual descreve o crescimento de diferentes cepas da levêdura *Saccharomyces cerevisiae*, dados esses, gerados pelo próprio *Growth Profiler*. 

  - Dados para teste: [Dado_Exemplo](https://github.com/BioAssis/BAS/raw/78dd27fbabf2e9686b8a4159adeab77470470cab/Exemplo_dados/Dados_teste_BAS.xlsx)

Após baixar dos dados acima, clique em [BAS - Bioprocess Assistant Software](https://baslnbr.streamlit.app), para acessar o site online e conhecer a ferramenta.

## Criadores e Idealizadores:
Tanto a interface gráfica quanto as funções utilizadas para qualquer manipulação de dados dentro BAS foram criadas pelos estudantes: 
  - Beatriz Borges Ribeiro, email: beatriz23028@ilum.cnpem.br.
    Aluna do 4° Semestre do Curso de Bacharel em Ciência e Tecnologia, Ilum - Escola de Ciências.
    
  - Daniel Bravin Martins, email: daniel23020@ilum.cnpem.br.
    Aluno do 4° Semestre do Curso de Bacharel em Ciência e Tecnologia, Ilum - Escola de Ciências.

A idéia e proposta do projeto foram criadas pelos pesquisadores/doutores:
  - Isabela Lobos de Mesquita Sampaio. Email: isabelle.sampaio@lnbr.cnpem.br Pesquisadora do LNBr
  - João H. Colombelli Manfrão Netto. Email: joao.netto@lnbr.cnpem.br  Pesquisador do LNBr

Uma versão, teste de conceito, foi produzida por um ex-estágio do LNBr, (nome do rapaz), a qual foi de extrema importância para a conclusão e síntese desse trabalho. 
