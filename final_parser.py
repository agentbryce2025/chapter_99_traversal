#!/usr/bin/env python3
import csv
import re
from html.parser import HTMLParser

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

def create_manual_structure():
    """Create a structure matching the example provided by the user"""
    with open('manual_chapter99.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Header row (blank)
        writer.writerow(['', '', '', '', '', '', ''])
        
        # Chapter title and description
        writer.writerow([
            'Chapter 99',
            """TEMPORARY LEGISLATION; TEMPORARY MODIFICATIONS ESTABLISHED
PURSUANT TO TRADE LEGISLATION; ADDITIONAL IMPORT RESTRICTIONS
ESTABLISHED PURSUANT TO SECTION 22 OF THE AGRICULTURAL
ADJUSTMENT ACT, AS AMENDED""",
            '', '', '', '', ''
        ])
        
        # US section
        writer.writerow(['', 'US', '', '', '', '', ''])
        
        # Note 1
        writer.writerow(['', '', '1', 'The provisions of this chapter relate to legislation and to executive and administrative actions pursuant to duly constituted authority, under which:', '', '', ''])
        
        # Sub-note a
        writer.writerow(['', '', '', 'a', 'One or more of the provisions in chapters 1 through 98 are temporarily amended or modified; or.', '', ''])
        
        # Sub-note b
        writer.writerow(['', '', '', 'b', 'Additional duties or other import restrictions are imposed by, or pursuant to, collateral legislation.', '', ''])
        
        # Note 2
        writer.writerow(['', '', '2', 'Unless the context requires otherwise, the general notes and rules of interpretation, the section notes, and the notes in chapters 1 through 98 apply to the provisions of this chapter.', '', '', ''])
        
        # Statistical section
        writer.writerow(['', 'Statistical', '', '', '', '', ''])
        
        # Statistical Note 1
        writer.writerow(['', '', '1', 'For statistical reporting of merchandise provided for herein:', '', '', ''])
        
        # Statistical Sub-note a
        writer.writerow(['', '', '', 'a', 'Unless more specific instructions appear in the subchapters of this chapter, report the 8-digit heading or subheading number (or 10-digit statistical reporting number, if any) found in this chapter in addition to the 10-digit statistical reporting number appearing in chapters 1 through 97 which would be applicable but for the provisions of this chapter; and', '', ''])
        
        # Statistical Sub-note b
        writer.writerow(['', '', '', 'b', 'The quantities reported should be in the units provided in chapters 1 through 97.', '', ''])
        
        # Statistical Note 2
        writer.writerow(['', '', '2', 'For those headings and subheadings herein for which no rate of duty appears (i.e., those headings and subheadings for which an absolute quota is prescribed), report the 8-digit heading or subheading number herein followed by the appropriate 10-digit statistical reporting number from chapters 1 through 97. The quantities reported should be in the units provided in chapters 1 through 97.', '', '', ''])
        
        # NOTICE section
        writer.writerow(['', 'NOTICE', 'The statistical reporting numbers contained in this chapter apply only to imports and may not be reported on Shipper\'s Export Declarations. See Notice to Exporters preceding chapter 1.', '', '', '', ''])
        
        # SPECIAL STATISTICAL REPORTING NUMBERS section
        writer.writerow(['', 'SPECIAL STATISTICAL REPORTING NUMBERS', """
StatisticalReportingNumber	Provision
SALVAGE
9999.00.2000	When a vessel has been sunk for 2 years in territorial waters of the United States and has been abandoned by its owner, any dutiable merchandise recovered therefrom may be brought into the nearest port free of duty under the authority of section 310 of the Tariff Act of 1930.
REPORTING REQUIREMENTS RELATED TO FREE TRADE AGREEMENTS
9999.00.84	Goods imported from Singapore and treated as originating goods under general note 25(m) for purposes of the U.S.-Singapore Free Trade Agreement.""", '', '', '', ''])
        
        # SUBCHAPTER I
        writer.writerow(['SUBCHAPTER I', '', '', '', '', '', ''])
        
        # US Notes for subchapter
        writer.writerow(['', 'US', """[COMPILER'S NOTE: Because the effective period of headings 9901.00.50 and 9901.00.52 has expired, the U.S. notes and their provisions, including the tariff-rate quota noted above, are not being administered. See also the compiler's note to these headings.]""", '', '', '', ''])
        
        # Note 1
        writer.writerow(['', '', '1', 'The duties provided for in this subchapter are cumulative duties which apply in addition to the duties, if any, otherwise imposed on the articles involved. The duties provided for in this subchapter apply only with respect to articles entered during the period specified in the last column.', '', '', ''])
        
        # Additional notes and content as needed...

def extract_complete_structure(html_content):
    parser = ChapterParser()
    parser.feed(html_content)
    raw_data = parser.data
    
    # Create a manual structure first
    create_manual_structure()
    
    # Now parse the HTML to extract all content
    rows = []
    
    # First row for chapter title
    chapter_title_row = [""] * 7
    chapter_title_row[0] = "Chapter 99"
    chapter_title_row[1] = raw_data[0]['content'] + "\n" + raw_data[1]['content'] + "\n" + raw_data[2]['content'] + "\n" + raw_data[3]['content'] + "\n" + raw_data[4]['content']
    rows.append(chapter_title_row)
    
    i = 6  # Start after the chapter title
    
    # Process the entire content
    while i < len(raw_data):
        content = raw_data[i]['content'].strip()
        
        # Skip empty content
        if not content or content == "XXII":
            i += 1
            continue
        
        # Process different types of content based on patterns
        
        # Check for section headers
        if content in ["US", "U.S."]:
            section_row = [""] * 7
            section_row[1] = "US"
            rows.append(section_row)
            i += 1
            continue
        
        if content == "Statistical":
            section_row = [""] * 7
            section_row[1] = "Statistical"
            rows.append(section_row)
            i += 1
            continue
        
        if content == "NOTICE":
            notice_row = [""] * 7
            notice_row[1] = "NOTICE"
            
            # Try to get the next content as the notice text
            if i+1 < len(raw_data):
                notice_row[2] = raw_data[i+1]['content']
                i += 2
            else:
                i += 1
                
            rows.append(notice_row)
            continue
        
        if content == "SPECIAL STATISTICAL REPORTING NUMBERS":
            special_row = [""] * 7
            special_row[1] = content
            
            # Try to get the next content
            if i+1 < len(raw_data):
                special_row[2] = raw_data[i+1]['content']
                i += 2
            else:
                i += 1
                
            rows.append(special_row)
            continue
        
        # Check for SUBCHAPTER
        if content.startswith("SUBCHAPTER"):
            subchapter_row = [""] * 7
            subchapter_row[0] = content
            rows.append(subchapter_row)
            i += 1
            continue
        
        # Check for numbered notes (1, 2, 3, etc.)
        if re.match(r'^\d+$', content):
            note_row = [""] * 7
            note_row[2] = content
            
            # Try to get the next content
            if i+1 < len(raw_data):
                note_row[3] = raw_data[i+1]['content']
                i += 2
            else:
                i += 1
                
            rows.append(note_row)
            continue
        
        # Check for lettered sub-notes (a, b, c, etc.)
        if re.match(r'^[a-z]$', content):
            subnote_row = [""] * 7
            subnote_row[3] = content
            
            # Try to get the next content
            if i+1 < len(raw_data):
                subnote_row[4] = raw_data[i+1]['content']
                i += 2
            else:
                i += 1
                
            rows.append(subnote_row)
            continue
        
        # Check for roman numerals (i, ii, iii, etc.)
        if re.match(r'^[ivx]+$', content.lower()) and len(content) <= 5:
            roman_row = [""] * 7
            roman_row[4] = content
            
            # Try to get the next content
            if i+1 < len(raw_data):
                roman_row[5] = raw_data[i+1]['content']
                i += 2
            else:
                i += 1
                
            rows.append(roman_row)
            continue
        
        # Check for capital letters (A, B, C, etc.)
        if re.match(r'^[A-Z]$', content):
            letter_row = [""] * 7
            letter_row[5] = content
            
            # Try to get the next content
            if i+1 < len(raw_data):
                letter_row[6] = raw_data[i+1]['content']
                i += 2
            else:
                i += 1
                
            rows.append(letter_row)
            continue
        
        # If we can't categorize it, add it to the first column
        default_row = [""] * 7
        default_row[0] = content
        rows.append(default_row)
        i += 1
    
    return rows

# Main execution
try:
    with open('chapter99_data.json', 'r', encoding='utf-8') as file:
        html_content = file.read()
except UnicodeDecodeError:
    with open('chapter99_data.json', 'r', encoding='latin-1') as file:
        html_content = file.read()

# Create full structured data
structured_data = extract_complete_structure(html_content)

# Write to CSV
with open('chapter99_final.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    for row in structured_data:
        csv_writer.writerow(row)

print("CSV file 'chapter99_final.csv' has been created.")
print("Manual example structure in 'manual_chapter99.csv' has been created.")