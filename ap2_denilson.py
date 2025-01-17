# -*- coding: utf-8 -*-
"""AP2 Denilson

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1K_F-QuMRF0OUpsyfH7LjhFyUy9fyOBk_
"""

#Nome: Janaina Vicente dos Santos RA: 2302926

# Commented out IPython magic to ensure Python compatibility.
# %%sh
# sudo pip install spark
# sudo pip install pyspark

"""# importando as bibliotecas"""

#Pandas, podemos transformar um dataframe do pandas em um dataframe do spark e o contrário também
import pandas as pd

#Importando o spark e o pyspark
import spark,pyspark

#Importando as bibliotecas do pyspark.sql
from pyspark.sql import *

#Importando funções sql do spark
#documentação https://spark.apache.org/docs/latest/api/sql/index.html
from pyspark.sql import functions as f

#Importando os tipos de dados do spark
#documentação https://spark.apache.org/docs/latest/sql-ref-datatypes.html
from pyspark.sql import types as t


#Biblioteca datetime
from datetime import datetime, date

"""#Criando uma Sessão do Spark (Spark Session)"""

from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local").appName("AP2 DataEng").getOrCreate()

"""#Importando objeto Row (linha)
 #Criando um dataframe
"""

#Importando objeto Row (linha)
from pyspark.sql import Row

#Criando um dataframe
df = spark.createDataFrame(
    [
    Row(a=1, b=2., c=['string1','string2'], d=date(2000, 1, 1), e=datetime(2000, 1, 1, 12, 0)),
    Row(a=2, b=3., c=['string1','string2'], d=date(2000, 2, 1), e=datetime(2000, 1, 2, 12, 0)),
    Row(a=4, b=5., c=['string1','string2'], d=date(2000, 3, 1), e=datetime(2000, 1, 3, 12, 0))
]
)

from pyspark.sql import SparkSession

# sessão Spark
spark = SparkSession.builder.master("local").appName("Carregamento de Arquivos CSV").getOrCreate()

# Carregar arquivos CSV e criar DataFrames
df_motorista = spark.read.csv("/content/motorista.csv", header=True, inferSchema=True)
df_carro = spark.read.csv("/content/carro.csv", header=True, inferSchema=True)
df_corrida = spark.read.csv("/content/corrida.csv", header=True, inferSchema=True)

# exibindo os DataFrames
df_motorista.show()
df_carro.show()
df_corrida.show()

"""Quantos motoristas temos do sexo feminino? (Exibir o sexo e a quantidade)

"""

# Número de motoristas do sexo feminino
resultado = df_motorista.groupBy("SEXO").count().filter(df_motorista["SEXO"] == "F")

# resultado
resultado.show()

"""Qual a montadora tem mais carros cadastrados pelos motoristas? (Exibir a montadora e a quantidade de motoristas que cadastraram os seus carros)

"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def montadora_com_mais_carros(df_carro):
    # carros por montadora e contar a quantidade de carros para cada montadora
    contagem_carros_por_montadora = df_carro.groupBy("MONTADORA").count()

    # Montadora com a maior quantidade de carros
    montadora_max_carros = contagem_carros_por_montadora.orderBy(col("count").desc()).first()

    return montadora_max_carros

# Função
montadora_max_carros = montadora_com_mais_carros(df_carro)

# Montadora com a maior quantidade de carros
print("A montadora com mais carros cadastrados é:", montadora_max_carros["MONTADORA"])
print("Quantidade de carros cadastrados:", montadora_max_carros["count"])

"""Tabela  com resultado"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def montadora_com_mais_carros(df_carro):
    # Carros por montadora e contar a quantidade de carros para cada montadora
    contagem_carros_por_montadora = df_carro.groupBy("MONTADORA").count()

    # Tabela de contagem de carros por montadora
    print("Tabela de contagem de carros por montadora:")
    contagem_carros_por_montadora.show()

    # Montadora com a maior quantidade de carros
    montadora_max_carros = contagem_carros_por_montadora.orderBy(col("count").desc()).first()

    return montadora_max_carros

# Chamada da função
montadora_max_carros = montadora_com_mais_carros(df_carro)

# Montadora com a maior quantidade de carros
print("A montadora com mais carros cadastrados é:", montadora_max_carros["MONTADORA"])
print("Quantidade de carros cadastrados:", montadora_max_carros["count"])

"""Qual a corrida mais longa e qual o valor pago por km (atentar que não é o valor cobrado, mas quanto o motorista cobrou por km rodado) ? (Exibir o nome do motorista que fez a corrida, km, e o valor pago por KM rodado)

"""

from pyspark.sql.functions import col

def corrida_mais_longa_valor_por_km(df_corrida):
    # Distância total da corrida (km)
    df_corrida = df_corrida.withColumn("DISTANCIA_TOTAL", col("KM"))

    # Valor pago por quilômetro rodado para cada corrida
    df_corrida = df_corrida.withColumn("VALOR_POR_KM", col("VALOR") / col("DISTANCIA_TOTAL"))

    # Corrida mais longa
    corrida_mais_longa = df_corrida.orderBy(col("DISTANCIA_TOTAL").desc()).first()

    # Informações da corrida mais longa
    print("Corrida mais longa:")
    print("ID do motorista:", corrida_mais_longa["ID_MOTORISTA"])
    print("Distância da corrida (km):", corrida_mais_longa["DISTANCIA_TOTAL"])
    print("Valor pago por km rodado:", corrida_mais_longa["VALOR_POR_KM"])

    return corrida_mais_longa

# Função
corrida_mais_longa = corrida_mais_longa_valor_por_km(df_corrida)

"""Mostrado na tabela o resultado da função anterior"""

def mostrar_tabela_corrida_mais_longa(df_corrida, corrida_mais_longa):
    # DataFrame para mostrar apenas a corrida mais longa
    df_corrida_mais_longa = df_corrida.filter(df_corrida["ID_CORRIDA"] == corrida_mais_longa["ID_CORRIDA"])

    # Tabela da corrida mais longa
    print("Tabela da corrida mais longa:")
    df_corrida_mais_longa.show()

# Função para encontrar a corrida mais longa
corrida_mais_longa = corrida_mais_longa_valor_por_km(df_corrida)

# Função para mostrar a tabela da corrida mais longa
mostrar_tabela_corrida_mais_longa(df_corrida, corrida_mais_longa)

"""Qual motorista realizou mais corridas? (Exibir nome do motorista, id motorista, quantidade corrida)"""

from pyspark.sql.functions import count

def motorista_com_mais_corridas(df_corrida, df_motorista):
    # DataFrame de corridas por ID do motorista e contar o número de corridas para cada um
    contagem_corridas_por_motorista = df_corrida.groupBy("ID_MOTORISTA").agg(count("*").alias("quantidade_corridas"))

    # DataFrame de contagem de corridas com o DataFrame de motoristas para obter o nome do motorista
    df_motorista_com_contagem = df_motorista.join(contagem_corridas_por_motorista, "ID_MOTORISTA")

    # Motorista com mais corridas
    motorista_mais_corridas = df_motorista_com_contagem.orderBy(col("quantidade_corridas").desc()).first()

    # Informações do motorista com mais corridas
    resultado = {
        "Nome do motorista": motorista_mais_corridas["NOME"],
        "ID do motorista": motorista_mais_corridas["ID_MOTORISTA"],
        "Quantidade de corridas": motorista_mais_corridas["quantidade_corridas"]
    }

    return resultado

# Função e exibição do resultado
resultado_motorista_mais_corridas = motorista_com_mais_corridas(df_corrida, df_motorista)
print("Motorista com mais corridas:")
print(resultado_motorista_mais_corridas)

"""Resultado na Tabela anteior"""

def mostrar_tabela_motorista_mais_corridas(df_corrida, df_motorista, resultado_motorista_mais_corridas):
    # DataFrame de motoristas para mostrar apenas o motorista com mais corridas
    df_motorista_mais_corridas = df_motorista.filter(df_motorista["ID_MOTORISTA"] == resultado_motorista_mais_corridas["ID do motorista"])

    # Tabela do motorista com mais corridas
    print("Tabela do motorista com mais corridas:")
    df_motorista_mais_corridas.show()

# Função para encontrar o motorista com mais corridas
resultado_motorista_mais_corridas = motorista_com_mais_corridas(df_corrida, df_motorista)

# Função para mostrar a tabela do motorista com mais corridas
mostrar_tabela_motorista_mais_corridas(df_corrida, df_motorista, resultado_motorista_mais_corridas)

"""Estrutura de dados, incluindo os nomes das colunas e os tipos de dados de cada coluna."""

df_corrida.printSchema()

"""Estrutura de dados, incluindo os nomes das colunas e os tipos de dados de cada coluna."""

df_carro.printSchema()

def verificar_coluna(df, coluna):
    """
    Verifica se a coluna especificada está presente no DataFrame.

    Parâmetros:
        - df: DataFrame do Spark.
        - coluna: Nome da coluna a ser verificada.

    Retorna:
        - True se a coluna estiver presente, False caso contrário.
    """
    if coluna in df.columns:
        return True
    else:
        return False

# Verificar se a coluna 'ID_CARRO' está presente no DataFrame
if verificar_coluna(df, 'ID_CARRO'):
    print("A coluna 'ID_CARRO' está presente no DataFrame.")
else:
    print("A coluna 'ID_CARRO' não está presente no DataFrame.")

from pyspark.sql.functions import monotonically_increasing_id

def adicionar_id_carro(df):
    """
    Adiciona uma coluna 'ID_CARRO' ao DataFrame com valores únicos para cada linha.

    Parâmetros:
        - df: DataFrame do Spark.

    Retorna:
        - DataFrame do Spark com a coluna 'ID_CARRO' adicionada.
    """
    # Adiciona uma coluna 'ID_CARRO' com valores únicos
    df_com_id = df.withColumn('ID_CARRO', monotonically_increasing_id())

    return df_com_id

# Adicionar a coluna 'ID_CARRO' ao DataFrame
df_com_id_carro = adicionar_id_carro(df)

# Exibir o DataFrame resultante
df_com_id_carro.show()

from pyspark.sql.functions import lit

def criar_coluna_verificacao(df_corrida):
    # Coluna "VALOR_TOTAL" está presente no esquema do DataFrame
    if "VALOR_TOTAL" in df_corrida.columns:
        # Coluna está presente, atribui True à nova coluna
        df_corrida = df_corrida.withColumn("VALOR_TOTAL_PRESENT", lit(True))
    else:
        # Coluna não está presente, atribui False à nova coluna
        df_corrida = df_corrida.withColumn("VALOR_TOTAL_PRESENT", lit(False))
    return df_corrida

# Chama a função para criar a coluna de verificação
df_corrida_com_verificacao = criar_coluna_verificacao(df_corrida)

# Exibe o DataFrame com a nova coluna de verificação
df_corrida_com_verificacao.show()

from pyspark.sql.functions import col

#DataFrame df_corrida pelo valor em ordem decrescente e selecionar as 10 primeiras linhas
corridas_mais_caras = df_corrida.orderBy(col("VALOR").desc()).limit(10)

# Mostrar as corridas mais caras
corridas_mais_caras.show()

corridas_mais_caras = df_corrida.orderBy(col("VALOR").desc()).limit(10)

corridas_mais_caras.show()

"""Qual corrida mais cara e qual modelo de carro realizou essa corrida (Exibir valor da corrida, motorista, modelo do carro)

"""

from pyspark.sql.functions import col

def detalhes_corrida_mais_cara(df_corrida, df_motorista, df_carro):
    # Encontre a corrida mais cara
    corrida_mais_cara = df_corrida.orderBy(col("VALOR").desc()).first()

    if corrida_mais_cara:
        # Obtenha o ID do motorista da corrida mais cara
        id_motorista_corrida_cara = corrida_mais_cara["ID_MOTORISTA"]

        # Encontre o ID do carro associado ao motorista da corrida mais cara
        id_carro = df_motorista.filter(df_motorista["ID_MOTORISTA"] == id_motorista_corrida_cara).select("ID_CARRO").first()["ID_CARRO"]

        # Encontre o modelo do carro associado ao ID do carro
        modelo_carro = df_carro.filter(df_carro["ID_CARRO"] == id_carro).select("MODELO").first()
        modelo_carro = modelo_carro["MODELO"] if modelo_carro else "Modelo não encontrado"

        # Crie uma tabela com os detalhes da corrida mais cara e o modelo do carro
        detalhes_corrida = spark.createDataFrame([(corrida_mais_cara["VALOR"], id_motorista_corrida_cara, modelo_carro)], ["Valor da corrida", "ID do motorista", "Modelo do carro"])

        return detalhes_corrida
    else:
        print("Não há corridas registradas.")

# Exibir a tabela com os detalhes da corrida mais cara
tabela_corrida_mais_cara = detalhes_corrida_mais_cara(df_corrida, df_motorista, df_carro)
if tabela_corrida_mais_cara:
    print("Tabela com os detalhes da corrida mais cara:")
    tabela_corrida_mais_cara.show()