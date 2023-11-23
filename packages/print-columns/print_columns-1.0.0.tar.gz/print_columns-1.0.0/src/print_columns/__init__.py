from termcolor import colored
import textwrap


def print_columns(
    strings: list[str],
    column_widths: list[int],
    colors: list[str] | None = None,
    divider: str = " | ",
) -> None:
    # assertion checks
    assert len(strings) == len(column_widths)
    if colors:
        assert len(strings) == len(colors)

    # wrap text in columns
    column_wrapped_texts = [
        [
            # pad end of line with spaces
            text_line + " " * (width - len(text_line))
            for text_line in textwrap.wrap(text, width=width)
        ]
        for width, text in zip(column_widths, strings)
    ]

    # pad all columns to the same number of lines
    max_length = max(map(len, column_wrapped_texts))
    for column, width in zip(column_wrapped_texts, column_widths):
        column.extend([" " * width] * (max_length - len(column)))

    # print columns side by side
    if colors:
        for row in zip(*column_wrapped_texts):
            for i, (text, color) in enumerate(zip(row, colors)):
                print(colored(text, color), end="")
                if i < len(row) - 1:
                    print(divider, end="")
            print()
    else:
        for row in zip(*column_wrapped_texts):
            print(divider.join(row))
