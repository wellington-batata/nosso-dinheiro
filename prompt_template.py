pt_date = '''
Considere que a data de hoje é {date}.
Extraia e converta qualquer expressão de tempo do texto abaixo para o formato YYYY-MM-DD.
Se não houver expressão de tempo, retorne a data atual.
Texto: "{param_text}"
Responda apenas com a data.
'''

pt_transaction = '''
Extraia as seguintes informações do texto abaixo:
- description (descrição da despesa, caso não encontre adicione o texto original)
- value (número com ponto decimal, caso não encontre adicione 0.0)
- category (uma categoria válida para a categoria, caso não encontre adicione "Não categorizado")
- subcategory (uma subcategoria válida para a categoria, caso não encontre adicione "Não categorizado")
- type (transação: credit ou debit)
- date (YYYY-MM-DD; use esta data {date})
texto: "{param_record}"
Responda estritamente em um objeto JSON, por exemplo:
[
{{
    "description": "Compra no supermercado",
    "value": 150.75,
    "category": "Alimentação",
    "subcategory": "Supermercado",
    "event_date": "2024-09-05"
}}
]
caso não consiga extrair alguma informação, retorne um array vazio: []
'''
