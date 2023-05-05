from selectolax.parser import HTMLParser

from config.tools import get_config
from utils.extract import extract_full_body_html
from utils.parse import parse_raw_attributes
from utils.process import format_and_transform, save_to_file


if __name__ == "__main__":
    config = get_config()

    url = config.get('url')
    items = config.get("item")

    html = extract_full_body_html(
        from_url=url,
        wait_for=config.get('container').get('selector')
    )

    nodes = parse_raw_attributes(html, [config.get('container')])

    game_data = []
    for d in nodes.get("store_sale_divs"):
        attrs = parse_raw_attributes(d, items)
        attrs = format_and_transform(attrs)
        game_data.append(attrs)

        # save to some csv file
        save_to_file("extract.csv", game_data)
