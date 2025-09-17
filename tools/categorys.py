
import json
from requests import Session
from models import Categorys


def listar_categorias(db: Session):
    categorys = db.query(Categorys).all()

    print(json.dumps([{
        "category": d.category,
        "subcategorys": d.subcategorys
    } for d in categorys], ensure_ascii=False, indent=2))

    return [
        {
            "id": d.id,
            "category": d.category,
            "subcategorys": d.subcategorys
        }
        for d in categorys
    ]


def montar_prompt(categorys: list):
    categorys_str = ""
    for category in categorys:
        categorys_str += f"- {category['category']}: {', '.join(category['subcategorys'])}\n"
    return categorys_str
