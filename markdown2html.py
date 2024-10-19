#!/usr/bin/python3
""" Markdown is awesome! """

import sys
import os

def main():
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(markdown_file, 'r') as md_file:
            lines = md_file.readlines()

        html_lines = []
        for line in lines:
            line = line.rstrip()
            if line.startswith('#'):
                heading_level = line.count('#')
                heading_text = line[heading_level:].strip()
                html_line = f"<h{heading_level}>{heading_text}</h{heading_level}>"
                html_lines.append(html_line)

        with open(output_file, 'w') as out_file:
            out_file.write("\n".join(html_lines) + "\n")

    except Exception as e:
        print(f"Error processing files: {e}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()