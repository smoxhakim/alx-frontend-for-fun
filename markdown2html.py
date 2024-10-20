#!/usr/bin/python3
""" Markdown is awesome! """


import sys
import os


def main():
    # Check if the number of arguments is less than 2
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    # Assign arguments to variables
    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the Markdown file exists
    if not os.path.isfile(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    # Process the Markdown file and generate HTML
    try:
        with open(markdown_file, 'r') as md_file:
            lines = md_file.readlines()

        html_lines = []
        in_unordered_list = False  # Track whether we are inside an unordered list
        in_ordered_list = False    # Track whether we are inside an ordered list
        paragraph_lines = []        # Collect lines for the current paragraph

        for line in lines:
            line = line.rstrip()  # Remove trailing whitespace
            
            # Check for headings
            if line.startswith('#'):
                heading_level = line.count('#')
                heading_text = line[heading_level:].strip()  # Get text after hashes
                html_line = f"<h{heading_level}>{heading_text}</h{heading_level}>"
                html_lines.append(html_line)
                in_unordered_list = False  # End any list when a heading is encountered
                in_ordered_list = False

            # Check for unordered lists
            elif line.startswith('-'):
                if not in_unordered_list:
                    html_lines.append("<ul>")  # Start a new unordered list
                    in_unordered_list = True
                
                list_item_text = line[1:].strip()  # Get text after '-'
                html_lines.append(f"<li>{list_item_text}</li>")

            # Check for ordered lists
            elif line.startswith('*'):
                if not in_ordered_list:
                    html_lines.append("<ol>")  # Start a new ordered list
                    in_ordered_list = True
                
                list_item_text = line[1:].strip()  # Get text after '*'
                html_lines.append(f"<li>{list_item_text}</li>")

            # Handle paragraphs and line breaks
            elif line.strip() == "":
                if paragraph_lines:
                    html_lines.append("<p>")
                    html_lines.append("<br/>".join(paragraph_lines))  # Join lines with <br/>
                    html_lines.append("</p>")
                    paragraph_lines = []  # Reset for next paragraph

            else:
                paragraph_lines.append(line)  # Collect lines for the current paragraph

        # Close any open lists or paragraphs at the end
        if in_unordered_list:
            html_lines.append("</ul>")
        if in_ordered_list:
            html_lines.append("</ol>")
        if paragraph_lines:
            html_lines.append("<p>")
            html_lines.append("<br/>".join(paragraph_lines))
            html_lines.append("</p>")

        # Write the generated HTML to the output file
        with open(output_file, 'w') as out_file:
            out_file.write("\n".join(html_lines) + "\n")

    except Exception as e:
        print(f"Error processing files: {e}", file=sys.stderr)
        sys.exit(1)

    # If everything is fine, exit with 0
    sys.exit(0)

if __name__ == "__main__":
    main()