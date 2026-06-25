Hong Kong Bank PDF to Excel Converter Prototype
===============================================

Supported statement layouts in this prototype:
- Hang Seng Bank / HSB statement layout from the tested sample
- HSBC Business Direct HKD Current and HKD Savings layouts
- HSBC Business Direct Foreign Currency Savings layouts, split into one sheet per currency
- Bank of China (Hong Kong) / BOC HKD Savings and HKD Current statement layout
- DBS Bank (Hong Kong) Current Account and Multi-currency Savings Account statement layouts
- Bank of Communications consolidated statement HKD Savings and HKD Current layouts
- OCBC Business Account / Integrated Account Statement Savings layouts, split into one sheet per currency

How to use
----------
1. Put PDF files into the BB folder.
2. Double-click run_converter.bat.
3. Generated Excel files will appear in the BB2 folder.

Output columns
--------------
Bank_Account, Date, Description, Deposit, Withdrawal, Balance, Control

Notes
-----
- The converter auto-detects HSBC vs HSB from the first pages of each PDF.
- BOC Chinese descriptions are preserved from the PDF text layer.
- DBS statements are exported into separate sheets by account/currency, such as DBS HKD Current Account and DBS USD MCY Savings.
- Bank of Communications statements are exported into Savings and Current sheets.
- OCBC integrated account statements are exported into separate sheets by currency, such as OCBC HKD Statement Savings, OCBC CNY Statement Savings and OCBC NOK Statement Savings.
- HSBC Foreign Currency Savings is exported into separate sheets such as:
  - HSBC USD Foreign Currency Savings
  - HSBC CNY Foreign Currency Savings
  - HSBC JPY Foreign Currency Savings
  - HSBC EUR Foreign Currency Savings
- The parser is coordinate-based, so new bank/PDF layouts should be calibrated with sample PDFs before production use.
