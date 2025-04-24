# Chapter 99 Traversal

This repository contains a CSV representation of the Chapter 99 data from the Harmonized Tariff Schedule of the United States (HTSUS).

## Data Source

The data was scraped from: https://hts.usitc.gov/reststop/getChapterNotes?doc=99

## File Structure

The CSV file `manual_chapter99.csv` contains the hierarchical structure of Chapter 99 with the following columns:

1. Column 1: Chapter/Subchapter level
2. Column 2: Section level (US, Statistical, NOTICE)
3. Column 3: Numeric note level (1, 2, 3, etc.)
4. Column 4: Alphabetic sub-note level (a, b, c, etc.)
5. Column 5: Roman numeral sub-sub-note level (i, ii, iii, etc.)
6. Column 6: Capital letter sub-sub-sub-note level (A, B, C, etc.)
7. Column 7: Content for the deepest level

This structure allows for easy traversal and navigation through the hierarchical content of Chapter 99.

## Usage

You can use this CSV file for:
1. Analysis of the HTSUS Chapter 99 provisions
2. Integration with tariff classification systems
3. Legal research related to temporary duty modifications and trade legislation
4. Educational purposes to understand the structure of the HTSUS

## Script

The repository also includes the Python script used to scrape and parse the data, which can be adapted for other chapters of the HTSUS.