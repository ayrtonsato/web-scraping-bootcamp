import pandas as pd
from datetime import datetime
from selectolax.parser import Node
import re


def get_attrs_from_node(node: Node, attr: str):
    if node is None or not issubclass(Node, type(node)):
        raise ValueError(
            "The function expects a selectolax node to be provided."
        )
    return node.attributes.get(attr)


def get_first_n(input_list: list, n: int = 5):
    return input_list[:n]


def reformat_date(date_raw: str, input_format: str = "%b %d, %Y", output_format: str = "%Y-%m-%d"):
    dt_obj = datetime.strptime(date_raw, input_format)
    return datetime.strftime(dt_obj, output_format)


def regex(input_str: str, pattern: str, do_what: str = "findall"):
    if do_what == "findall":
        return re.findall(pattern, input_str)
    elif do_what == "split":
        result = re.split(pattern, input_str)
        return result
    else:
        raise ValueError("The function expects 'findall' or 'split'")


def format_and_transform(attrs: dict):
    transforms = {
        "thumbnail": lambda n: get_attrs_from_node(n, "src"),
        "tags": lambda input_list: get_first_n(input_list, 5),
        "release_date": lambda date: reformat_date(date, "%b %d, %Y", "%Y-%m-%d"),
        "reviewed_by": lambda raw: int(''.join(regex(raw, r'\d+'))),
        "price_currency": lambda raw: regex(raw, r'(R\$)(.*)', "split")[1],
        "sale_price": lambda raw: float(regex(raw, r'(R\$)(.*)', "split")[2].replace(",", ".")),
        "original_price": lambda raw: float(regex(raw, r'(R\$)(.*)', "split")[2].replace(",", ".")),
    }

    for k, v in transforms.items():
        if k in attrs:
            attrs[k] = v(attrs[k])
    attrs["discount_pct"] = round(
        (attrs["original_price"] - attrs["sale_price"]) / attrs["original_price"] * 100, 2
    )
    return attrs


def save_to_file(filename="extract.csv", data: list[dict] = None):
    if data is None:
        raise ValueError("Provide a list of dict")
    df = pd.DataFrame(data)
    filename = f"{datetime.now().strftime('%Y_%m_%d')}_{filename}"
    df.to_csv(filename, index=False)
