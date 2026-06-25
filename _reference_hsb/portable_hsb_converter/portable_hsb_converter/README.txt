Hang Seng PDF to Excel Converter
================================

How to move to another computer
-------------------------------
1. Copy this whole folder to the other computer.
2. Put Hang Seng PDF files into the BB folder.
3. Double-click run_converter.bat.
4. Generated Excel files will appear in the BB2 folder.

Requirements
------------
- Windows
- Python 3.10 or newer
- Internet connection the first time you run it, so pip can install:
  - pdfplumber
  - openpyxl

Folder layout
-------------
portable_hsb_converter
  convert_hsb_pdf.py
  hsb_pdf_converter.py
  requirements.txt
  run_converter.bat
  BB     <- put PDF files here
  BB2    <- Excel files are generated here

Command line use
----------------
From this folder:

python convert_hsb_pdf.py

Optional custom paths:

python convert_hsb_pdf.py "C:\path\to\pdf_or_folder" -o "C:\path\to\excel_output"

Notes
-----
The converter is designed for Hang Seng statement PDFs with the same style as
the sample files already tested. It creates one Excel sheet per bank account
and includes these columns:

Bank_Account, Date, Description, Deposit, Withdrawal, Balance, Control
