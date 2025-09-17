pt_date = '''
Considere que a data de hoje é {date}.
Extraia e converta qualquer expressão de tempo do texto abaixo para o formato YYYY-MM-DD.
Se não houver expressão de tempo, retorne a data atual.
Texto: "{param_text}"
Responda apenas com a data.
'''

pt_expenses = '''
Extraia as seguintes informações do texto abaixo:
- description (descrição da despesa)
- value (número com ponto decimal)
- category
- date (YYYY-MM-DD; use esta data {date})
texto: "{param_record}"
Responda estritamente em um objeto JSON, por exemplo:
[
{{
    "description": "Compra no supermercado",
    "value": 150.75,
    "category": "Alimentação",
    "event_date": "2024-09-05"
}}
]
'''
