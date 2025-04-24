#!/usr/bin/env python3
import csv
import re
from html.parser import HTMLParser
import json

# Define a custom HTML parser
class ChapterParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = []
        self.current_element = None
        self.current_attributes = {}
        self.current_data = ""
        self.in_div = False
        
    def handle_starttag(self, tag, attrs):
        self.current_element = tag
        self.current_attributes = dict(attrs)
        if tag == 'div':
            self.in_div = True
            
    def handle_endtag(self, tag):
        if tag == 'div' and self.in_div:
            self.in_div = False
            if self.current_data.strip():
                index = self.current_attributes.get('index', '')
                class_name = self.current_attributes.get('class', '')
                self.data.append({
                    'index': index,
                    'class': class_name,
                    'content': self.current_data.strip()
                })
            self.current_data = ""
        self.current_element = None
        
    def handle_data(self, data):
        if self.in_div:
            self.current_data += data

# Function to parse the content structure into hierarchical form
def parse_structure(data):
    rows = []
    current_row = [""] * 7  # Empty row with 7 columns
    
    # First row for chapter title
    chapter_title_row = [""] * 7
    chapter_title_row[0] = "Chapter 99"
    chapter_title_row[1] = data[0]['content'] + "\n" + data[1]['content'] + "\n" + data[2]['content'] + "\n" + data[3]['content'] + "\n" + data[4]['content']
    rows.append(chapter_title_row)
    
    # Process the remaining content
    i = 6  # Start after the chapter title and numbering
    
    # Track hierarchy levels
    current_level = 0
    
    while i < len(data):
        item = data[i]
        content = item['content']
        
        # Skip if content is just whitespace or meaningless
        if not content.strip() or content.strip() == "XXII":
            i += 1
            continue
        
        # US Notes
        if content == "US" or content == "U.S.":
            new_row = [""] * 7
            new_row[1] = content
            rows.append(new_row)
            i += 1
            continue
            
        # Statistical Notes
        if content == "Statistical":
            new_row = [""] * 7
            new_row[1] = content
            rows.append(new_row)
            i += 1
            continue
            
        # Notice
        if content == "NOTICE":
            new_row = [""] * 7
            new_row[1] = content
            rows.append(new_row)
            i += 1
            continue
            
        # Special Statistical Reporting Numbers
        if content == "SPECIAL STATISTICAL REPORTING NUMBERS":
            new_row = [""] * 7
            new_row[1] = content
            
            # Combine the next item which contains the reporting numbers
            if i+1 < len(data):
                new_row[2] = data[i+1]['content']
                i += 2
            else:
                i += 1
            
            rows.append(new_row)
            continue
            
        # Subchapter
        if content.startswith("SUBCHAPTER"):
            new_row = [""] * 7
            new_row[0] = content
            rows.append(new_row)
            i += 1
            continue
        
        # Numeric note (1, 2, 3, etc.)
        if re.match(r'^\d+$', content):
            new_row = [""] * 7
            new_row[2] = content
            
            # Look ahead for content
            if i+1 < len(data):
                new_row[3] = data[i+1]['content']
                i += 2
            else:
                i += 1
            
            rows.append(new_row)
            continue
            
        # Alphabetic sub-note (a, b, c, etc.)
        if re.match(r'^[a-z]$', content):
            new_row = [""] * 7
            new_row[3] = content
            
            # Look ahead for content
            if i+1 < len(data):
                new_row[4] = data[i+1]['content']
                i += 2
            else:
                i += 1
            
            rows.append(new_row)
            continue
            
        # Roman numeral sub-sub-note (i, ii, iii, etc.)
        if re.match(r'^[ivx]+$', content.lower()):
            new_row = [""] * 7
            new_row[4] = content
            
            # Look ahead for content
            if i+1 < len(data):
                new_row[5] = data[i+1]['content']
                i += 2
            else:
                i += 1
            
            rows.append(new_row)
            continue
            
        # Capital letter sub-sub-sub-note (A, B, C, etc.)
        if re.match(r'^[A-Z]$', content):
            new_row = [""] * 7
            new_row[5] = content
            
            # Look ahead for content
            if i+1 < len(data):
                new_row[6] = data[i+1]['content']
                i += 2
            else:
                i += 1
            
            rows.append(new_row)
            continue
        
        # If we can't categorize it, just add it as a new row
        new_row = [""] * 7
        new_row[0] = content
        rows.append(new_row)
        i += 1
    
    return rows

# Main execution
try:
    with open('chapter99_data.json', 'r', encoding='utf-8') as file:
        html_content = file.read()
except UnicodeDecodeError:
    with open('chapter99_data.json', 'r', encoding='latin-1') as file:
        html_content = file.read()

parser = ChapterParser()
parser.feed(html_content)

# Parse the structure
structured_data = parse_structure(parser.data)

# Write to CSV
with open('chapter99.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    for row in structured_data:
        csv_writer.writerow(row)

print("CSV file 'chapter99.csv' has been created.")