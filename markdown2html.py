#!/usr/bin/python3
""" Markdown is awesome! """


import sys
import os



def main():
    # Check if the number of arguments is less than 2
    if len(sys.argv) < 3:
        sys.exit("Usage: ./markdown2html.py README.md README.html")
    
    # Check if the Markdown file exists
    markdown_file = sys.argv[1]
    if not os.path.isfile(markdown_file):
        sys.exit("Missing {}".format(markdown_file))

    text = []
    in_unordered_list = False
    in_ordered_list = False

    with open(markdown_file, encoding='utf-8') as md_file:
        for line in md_file:
            line = line.rstrip()  # Remove trailing whitespace
            
            # Check for headings
            if line.startswith('#'):
                heading_level = line.count('#')
                heading_text = line[heading_level:].strip()  # Get text after hashes
                if heading_level < 7:  # Ensure valid heading level (1-6)
                    text.append(f"<h{heading_level}>{heading_text}</h{heading_level}>")
            
            # Check for unordered lists
            elif line.startswith('-'):
                if not in_unordered_list:
                    text.append("<ul>")
                    in_unordered_list = True
                list_item_text = line[1:].strip()  # Get text after '-'
                text.append(f"<li>{list_item_text}</li>")

            # Check for ordered lists
            elif line.startswith('*'):
                if not in_ordered_list:
                    text.append("<ol>")
                    in_ordered_list = True
                list_item_text = line[1:].strip()  # Get text after '*'
                text.append(f"<li>{list_item_text}</li>")
            
            else:
                # If we were in a list, close it
                if in_unordered_list:
                    text.append("</ul>")
                    in_unordered_list = False
                if in_ordered_list:
                    text.append("</ol>")
                    in_ordered_list = False
                
                # Handle paragraphs
                if line.strip():  # Only add non-empty lines as paragraphs
                    text.append(f"<p>{line}</p>")
        
        # Close any open lists at the end of the file
        if in_unordered_list:
            text.append("</ul>")
        if in_ordered_list:
            text.append("</ol>")

    # Write the generated HTML to the output file
    with open(sys.argv[2], 'w', encoding='utf-8') as html_file:
        html_file.write('\n'.join(text) + '\n')

if __name__ == "__main__":
    main()