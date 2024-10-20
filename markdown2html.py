#!/usr/bin/python3
""" Markdown is awesome! """

import sys
import os
import re

def process_bold_emphasis(text):
    """Process bold and emphasis markdown syntax in text"""
    # Process bold syntax with **
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    # Process emphasis syntax with __
    text = re.sub(r'__([^_]+)__', r'<em>\1</em>', text)
    return text

def process_paragraph(lines):
    """Process a paragraph's lines and return the HTML representation"""
    if not lines:
        return ""
    
    # Process each line for bold and emphasis
    formatted_lines = []
    for i, line in enumerate(lines):
        # Process bold and emphasis syntax
        line = process_bold_emphasis(line)
        
        if i < len(lines) - 1:  # Add <br /> for all lines except the last
            formatted_lines.append(f"    {line}\n        <br />")
        else:
            formatted_lines.append(f"    {line}")
    
    return "<p>\n{}\n</p>".format("\n".join(formatted_lines))

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
    current_paragraph = []

    with open(markdown_file, encoding='utf-8') as md_file:
        lines = md_file.readlines()
        
        for line in lines:
            line = line.rstrip()  # Remove trailing whitespace
            
            # Check for headings
            if line.startswith('#'):
                # Process any pending paragraph
                if current_paragraph:
                    text.append(process_paragraph(current_paragraph))
                    current_paragraph = []
                
                heading_level = line.count('#')
                heading_text = line[heading_level:].strip()
                # Process bold and emphasis in heading
                heading_text = process_bold_emphasis(heading_text)
                if heading_level < 7:
                    text.append(f"<h{heading_level}>{heading_text}</h{heading_level}>")
            
            # Check for unordered lists
            elif line.startswith('-'):
                # Process any pending paragraph
                if current_paragraph:
                    text.append(process_paragraph(current_paragraph))
                    current_paragraph = []
                
                if not in_unordered_list:
                    text.append("<ul>")
                    in_unordered_list = True
                list_item_text = line[1:].strip()
                # Process bold and emphasis in list items
                list_item_text = process_bold_emphasis(list_item_text)
                text.append(f"<li>{list_item_text}</li>")

            # Check for ordered lists
            elif line.startswith('*'):
                # Process any pending paragraph
                if current_paragraph:
                    text.append(process_paragraph(current_paragraph))
                    current_paragraph = []
                
                if not in_ordered_list:
                    text.append("<ol>")
                    in_ordered_list = True
                list_item_text = line[1:].strip()
                # Process bold and emphasis in list items
                list_item_text = process_bold_emphasis(list_item_text)
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
                if not line.strip():  # Empty line
                    if current_paragraph:  # If we have a pending paragraph, process it
                        text.append(process_paragraph(current_paragraph))
                        current_paragraph = []
                else:
                    current_paragraph.append(line)
        
        # Process any remaining paragraph at the end of the file
        if current_paragraph:
            text.append(process_paragraph(current_paragraph))
        
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