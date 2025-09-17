from datetime import datetime

format_date = "%Y-%m-%d %H:%M:%S"


def tratar_data(data_str: str = None) -> str:
    hoje = datetime.now()
    if not data_str or data_str.strip() == "" or data_str.strip().lower() == "hoje":
        # Nenhuma data informada ou "hoje", retorna data atual
        return hoje.strftime(format_date)
    data_str = data_str.strip().lower()
    if data_str == "ontem":
        ontem = hoje.replace(hour=0, minute=0, second=0,
                             microsecond=0)  # zera hora
        ontem = ontem.fromordinal(hoje.toordinal() - 1)
        return ontem.strftime(format_date)
    try:
        # Se vier só o dia (ex: "5")
        if data_str.isdigit():
            return f"{hoje.year}-{hoje.month:02d}-{int(data_str):02d}"
        # Se vier só dia e mês (ex: "05-09" ou "5-9")
        partes = data_str.split("-")
        if len(partes) == 2 and all(p.isdigit() for p in partes):
            return f"{hoje.year}-{int(partes[1]):02d}-{int(partes[0]):02d}"
        # Se vier ano, mês e dia (ex: "2025-09-05")
        if len(partes) == 3 and all(p.isdigit() for p in partes):
            return f"{int(partes[0]):04d}-{int(partes[1]):02d}-{int(partes[2]):02d}"
        # Tenta converter diretamente
        return datetime.fromisoformat(data_str).strftime(format_date)
    except Exception:
        # Se não conseguir interpretar, retorna data atual
        return hoje.strftime(format_date)
