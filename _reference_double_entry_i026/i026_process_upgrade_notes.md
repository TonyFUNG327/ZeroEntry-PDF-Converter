# I026 Process Upgrade Notes

I026 confirms the H026 advanced structure but adds deferred income, AR reclassification, PPE/depreciation, finance-cost style non-bank schedules, and broader report sections.

## Input Sheet: NCB HKD SA
- Account/record label: NCB HKD S/A #043-509-018239-2
- COA name: NCB HKD SA
- Detected header row: 9
- Nonblank dated transaction rows: 23
- First transaction rows:
  - row 10: date=Date, nature=Nature, payer/payee=Payer / (Payee), invoice=Invoice no. (Cheque no.)
  - row 11: date=2025-01-01, nature=Bank opening, payer/payee=, invoice=
  - row 12: date=2025-01-31, nature=Bank interest income, payer/payee=Interest, invoice=
  - row 13: date=2025-02-28, nature=Bank interest income, payer/payee=Interest, invoice=
  - row 14: date=2025-03-30, nature=Bank charges, payer/payee=Auditor’s Confirmation, invoice=
  - row 15: date=2025-03-31, nature=Bank interest income, payer/payee=Interest, invoice=
  - row 16: date=2025-04-30, nature=Bank interest income, payer/payee=Interest, invoice=
  - row 17: date=2025-05-31, nature=Bank interest income, payer/payee=Interest, invoice=
- Helper columns detected:
  57:Reference; 59:Number of Distributions; 60:G/L Account; 61:G/L Account; 62:Description; 63:Bank (Amount$); 64:Nature (Amount$)
- Key totals:
  - Deposit: 206923.16000000003
  - Withdrawal: -100600.0
  - Interbank: -100000.0
  - Receipt in advance: 172324.0
  - Membership fee income: 31676.0
  - Bank interest income: 2923.1600000000003
  - Bank charges: -600.0
  - Bank (Amount$): 106323.16
  - Nature (Amount$): -106323.16

## Input Sheet: NCB HKD CA
- Account/record label: NCB HKD C/A #043-509-007436-2
- COA name: NCB HKD CA
- Detected header row: 9
- Nonblank dated transaction rows: 20
- First transaction rows:
  - row 10: date=Date, nature=Nature, payer/payee=Payer / (Payee), invoice=Invoice no. (Cheque no.)
  - row 11: date=2025-01-01, nature=Bank opening, payer/payee=, invoice=
  - row 12: date=2025-01-03, nature=Accruals, payer/payee=000773, invoice=
  - row 13: date=2025-02-22, nature=Web hosting fee, payer/payee=000877, invoice=
  - row 14: date=2025-02-22, nature=Legal and professional fee, payer/payee=000775, invoice=Lee & Yu Corporate Services Limited
  - row 15: date=2025-03-05, nature=Web hosting fee, payer/payee=000876, invoice=mCommerce
  - row 16: date=2025-03-05, nature=Accruals, payer/payee=000774, invoice=
  - row 17: date=2025-03-14, nature=Accruals, payer/payee=000880, invoice=
- Helper columns detected:
  57:Reference; 59:Number of Distributions; 60:G/L Account; 61:G/L Account; 62:Description; 63:Bank (Amount$); 64:Nature (Amount$)
- Key totals:
  - Deposit: 136313.3
  - Withdrawal: -237093.24
  - Interbank: 100000.0
  - Prepayment: -9800.0
  - Accruals: -39630.82
  - Bank charges: -300.0
  - Web hosting fee: -76878.48000000001
  - Bank (Amount$): -100779.94000000002
  - Nature (Amount$): 100779.94000000002

## Input Sheet: HSBC USD SA
- Account/record label: HSBC USD S/A #123-456789-001
- COA name: HSBC USD SA
- Detected header row: 9
- Nonblank dated transaction rows: 4
- First transaction rows:
  - row 10: date=Date, nature=Nature, payer/payee=Payer / (Payee), invoice=Invoice no. (Cheque no.)
  - row 11: date=2025-01-01, nature=Bank opening, payer/payee=, invoice=
  - row 12: date=2025-01-01, nature=Sales, payer/payee=Sale invoce #12345, invoice=ABC customer
  - row 13: date=2025-01-01, nature=Bank charges, payer/payee=Bank chg, invoice=
- Helper columns detected:
  61:Reference; 63:Number of Distributions; 64:G/L Account; 65:G/L Account; 66:Description; 67:Bank (Amount$); 68:Nature (Amount$)
- Key totals:
  - Deposit: 17600.0
  - Withdrawal: -8800.0
  - Sales: 15600.0
  - Bank charges: -7800.0
  - Bank (Amount$): 7800.0
  - Nature (Amount$): -7800.0

## Input Sheet: Finance costs
- Account/record label: Obligation under Finance Lease
- COA name: Obligation under Finance Lease
- Detected header row: 9
- Nonblank dated transaction rows: 3
- First transaction rows:
  - row 10: date=Date, nature=Nature, payer/payee=Payer / (Payee), invoice=Invoice no. (Cheque no.)
  - row 11: date=2025-01-01, nature=Bank opening, payer/payee=, invoice=
  - row 12: date=2025-01-01, nature=Interest on finance lease, payer/payee=, invoice=
- Helper columns detected:
  57:Reference; 59:Number of Distributions; 60:G/L Account; 61:G/L Account; 62:Description; 63:=BH10; 64:=BI10
- Non-zero control rows observed:
  row 12=-100; row 104=-100
- Key totals:
  - Withdrawal: -200.0
  - Control: -200.0

## Chart of Accounts Observations
- 1xxx: 1000 Cash; 1010 NCB HKD CA; 1020 NCB HKD SA; 1030 BOC HKD CA; 1040 BOC HKD SA; 1080 HSBC HKD Credit Card; 1090 Interbank; 1099 Temp; 1100 Trade receivable; 1120 Other receivables
- 2xxx: 2000 Trade payable; 2050 Other payables; 2100 Receipt in advance; 2200 Accruals; 2400 Director's C/A; 2500 Related company C/A; 2700 HSB Bank loan; 2800 Obligation under Finance Lease; 2900 Tax payable
- 3xxx: 3910 Retained Earnings; 3920 Share capital; 3930 Dividends Paid
- 4xxx: 4000 Membership fee income; 4050 Services income; 4100 Bank interest income; 4200 Government grants; 4300 Sundry income; 4900 Sales discounts
- 5xxx: 5000 Event Service Fee; 5100 Subcontractor; 5200 Transportation; 5300 Handling charges; 5400 Consumables; 5800 Opening inventories; 5900 Closing inventories
- 6xxx: 6000 Accounting fee; 6050 Advertisement; 6100 Auditor's remuneration; 6150 Bad debt; 6200 Bank charges; 6220 Building management fee; 6250 Business registration fee; 6300 Commission; 6330 Company secretarial fee; 6350 Computer accessories
- 7xxx: 7000 Overseas travelling; 7050 Penalty; 7100 Postage & courier; 7150 Printing & stationery; 7170 Promotion fee; 7200 Rental expenses; 7250 Repairs & maintenance; 7270 Retaining service fee; 7300 Salaries; 7350 Staff welfare
- 8xxx: 8000 Interest on bank loans; 8100 Interest on bank overdraft; 8200 Interest on finance lease; 8500 Impairment loss
- 9xxx: 9000 Income tax expenses

## Manual JV References Found in GL
- JV-AR-2512:
  - 1100 Trade receivable: Dr=20000 Cr= Desc=2025 AR:2025-M-70106-Ernst & Young Hong Kong
  - 1100 Trade receivable: Dr=20000 Cr= Desc=2025 AR:2025-M-70107-Alibaba Cloud (Singapore) Private Limited
  - 1100 Trade receivable: Dr=2000 Cr= Desc=2025 AR:2025-NGO-70102-Hong Kong Cyberport Management Company Limited
  - 1100 Trade receivable: Dr=2000 Cr= Desc=2025 AR:2025-NGO-70103-Hong Kong Federation of Insurers
  - 2100 Receipt in advance: Dr= Cr=11665 Desc=2025 AR:2025-M-70107-Alibaba Cloud (Singapore) Private Limited
  - 2100 Receipt in advance: Dr= Cr=1165 Desc=2025 AR:2025-NGO-70102-Hong Kong Cyberport Management Company Limited
  - 2100 Receipt in advance: Dr= Cr=11665 Desc=2025 AR:2025-M-70106-Ernst & Young Hong Kong
  - 2100 Receipt in advance: Dr= Cr=1165 Desc=2025 AR:2025-NGO-70103-Hong Kong Federation of Insurers
  - 4000 Membership fee income: Dr= Cr=8335 Desc=2025 AR:2025-M-70106-Ernst & Young Hong Kong
  - 4000 Membership fee income: Dr= Cr=8335 Desc=2025 AR:2025-M-70107-Alibaba Cloud (Singapore) Private Limited
  - 4000 Membership fee income: Dr= Cr=835 Desc=2025 AR:2025-NGO-70102-Hong Kong Cyberport Management Company Limited
  - 4000 Membership fee income: Dr= Cr=835 Desc=2025 AR:2025-NGO-70103-Hong Kong Federation of Insurers
- JV-Accruals-2512:
  - 2200 Accruals: Dr= Cr=12200 Desc=Being the provision for acc + audit fee for the year.
  - 6000 Accounting fee: Dr=5000 Cr= Desc=Being the provision for acc + audit fee for the year.
  - 6100 Auditor's remuneration: Dr=7200 Cr= Desc=Being the provision for acc + audit fee for the year.
- JV-l/y prepaid:
  - 1300 Prepayment: Dr= Cr=4900 Desc=Company secretarial fee:l/y prepayment
  - 6330 Company secretarial fee: Dr=4900 Cr= Desc=Company secretarial fee:l/y prepayment
- JV-l/y trade dep rec:
  - 2100 Receipt in advance: Dr=81996 Cr= Desc=Being the reallocation of 2025 sales from trade deposits received.
  - 4000 Membership fee income: Dr= Cr=81996 Desc=Being the reallocation of 2025 sales from trade deposits received.

## Output Report Snapshot
### TB 31.12.25
- row 1: Account ID | Account Description | Debit Amt | Credit Amt | 
- row 2: 1010 | NCB HKD CA | 37231.66 |  | 
- row 3: 1020 | NCB HKD SA | 603180.5 |  | 
- row 4: 1100 | Trade receivable | 64000 |  | 
- row 5: 1300 | Prepayment | 4900 |  | 
- row 6: 1800 | Office equipment | 5750 |  | 
- row 7: 1850 | Accum Depreciation-OE |  | -5750 | 
- row 8: 2100 | Receipt in advance |  | -123310 | 
- row 9: 2200 | Accruals |  | -12200 | 
- row 10: 3910 | Retained Earnings |  | -549241.14 | 
- row 11: 4000 | Membership fee income |  | -116174 | 
- row 12: 4100 | Bank interest income |  | -1461.58 | 
- row 13: 6000 | Accounting fee | 5000 |  | 
- row 14: 6100 | Auditor's remuneration | 7200 |  | 
- row 15: 6200 | Bank charges | 450 |  | 
- row 16: 6330 | Company secretarial fee | 4900 |  | 
- row 17: 6350 | Computer accessories | 6844.32 |  | 
- row 18: 6550 | Entertainment | 7241 |  | 
- row 19: 6680 | Legal and professional fee | 23000 |  | 
- row 20: 7550 | Web hosting fee | 38439.24 |  | 
- row 22:  | Total: | 808136.72 | -808136.72 | 

### GL 31.12.25
- row 1: Account ID | Account Description | Date | Reference | Jrnl | Trans Description | Debit Amt | Credit Amt | Balance
- row 2: 1010 | NCB HKD CA | 45658 |  |  | Beginning Balance |  |  | 
- row 3: 1010 | NCB HKD CA | 45658 | Opening balance | GENJ | Opening balance - NCB HKD CA | 87621.63 |  | 
- row 4: 1010 | NCB HKD CA | 45717 | NCB HKD CA-2501-001 | GENJ | Accruals:000773 |  | 3000 | 
- row 5: 1010 | NCB HKD CA | 22/2/25 | NCB HKD CA-2502-001 | GENJ | Web hosting fee:000877 - WIX.com Website Designing and Hosting Services |  | 2485.86 | 
- row 6: 1010 | NCB HKD CA | 22/2/25 | NCB HKD CA-2502-002 | GENJ | Legal and professional fee:000775 - Lee & Yu Corporate Services Limited - Debit Note C09080-s.88 services |  | 4800 | 
- row 7: 1010 | NCB HKD CA | 45780 | NCB HKD CA-2503-001 | GENJ | Web hosting fee:000876 - mCommerce - Amazon Web Services - 2025 January 1 to January 31 |  | 4366.6 | 
- row 8: 1010 | NCB HKD CA | 45780 | NCB HKD CA-2503-002 | GENJ | Accruals:000774 |  | 4615.41 | 
- row 9: 1010 | NCB HKD CA | 14/3/25 | NCB HKD CA-2503-003 | GENJ | Accruals:000880 - 2024 Autid and Accounting |  | 12200 | 
- row 10: 1010 | NCB HKD CA | 14/3/25 | NCB HKD CA-2503-004 | GENJ | Legal and professional fee:000878 - Lee & Yu Corporate Services Limited - Debit Note C09092 - trademark registration |  | 18200 | 
- row 11: 1010 | NCB HKD CA | 15/3/25 | NCB HKD CA-2503-005 | GENJ | Web hosting fee:000879 - mCommerce - Amazon Web Services - 2025 February 1 to February 28 |  | 4604.13 | 
- row 12: 1010 | NCB HKD CA | 18/3/25 | NCB HKD CA-2503-006 | GENJ | Web hosting fee:000882 - Website development tools : Slidespeak - USD 359 |  | 2800 | 
- row 13: 1010 | NCB HKD CA | 18/3/25 | NCB HKD CA-2503-007 | GENJ | Entertainment:000881 - Dinner with Vetting Committee |  | 7241 | 
- row 14: 1010 | NCB HKD CA | 45936 | NCB HKD CA-2506-001 | GENJ | Web hosting fee:000883 - WIX.COM - Website fee |  | 6026 | 
- row 15: 1010 | NCB HKD CA | 14/6/25 | NCB HKD CA-2506-002 | GENJ | Temp:000884 - mCommerce - Amazon Web Services |  | 18156.65 | 
- row 16: 1010 | NCB HKD CA | 16/6/25 | NCB HKD CA-2506-003 | GENJ | Bank charges:Return cheque |  | 150 | 
- row 17: 1010 | NCB HKD CA | 16/6/25 | NCB HKD CA-2506-004 | GENJ | Temp:000884IN-CLEARING RETURN - mCommerce - Amazon Web Services | 18156.65 |  | 
- row 18: 1010 | NCB HKD CA | 19/6/25 | NCB HKD CA-2506-005 | GENJ | Computer accessories:000885 - eeio Limited - Microsoft 365 Business Standard annual subscription yearly |  | 6844.32 | 
- row 19: 1010 | NCB HKD CA | 20/6/25 | NCB HKD CA-2506-006 | GENJ | Company secretarial fee:000886 - AC Business Service Limited - Renew Package(Annual Return,Company Secretary) - Service Period: 2025-07-19~2026-07-18 |  | 4900 | 
- row 20: 1010 | NCB HKD CA | 20/6/25 | NCB HKD CA-2506-007 | GENJ | Interbank:transfer | 50000 |  | 
- row 21: 1010 | NCB HKD CA | 24/6/25 | NCB HKD CA-2506-008 | GENJ | Web hosting fee:000887 - mCommerce - Amazon Web Services |  | 18156.65 | 
- row 22: 1010 | NCB HKD CA |  |  |  | Change | 155778.28 | 118546.62 | 37231.66
- row 23:  |  | 31/12/25 |  |  | Ending Balance |  |  | 37231.66
- row 24: 1020 | NCB HKD SA | 45658 |  |  | Beginning Balance |  |  | 
- row 25: 1020 | NCB HKD SA | 45658 | Opening balance | GENJ | Opening balance - NCB HKD SA | 550018.92 |  | 
- row 26: 1020 | NCB HKD SA | 31/1/25 | NCB HKD SA-2501-001 | GENJ | Bank interest income:Interest | 175.18 |  | 
- row 27: 1020 | NCB HKD SA | 28/2/25 | NCB HKD SA-2502-001 | GENJ | Bank interest income:Interest | 158.27 |  | 
- row 28: 1020 | NCB HKD SA | 30/3/25 | NCB HKD SA-2503-001 | GENJ | Bank charges:Auditor’s Confirmation |  | 300 | 
- row 29: 1020 | NCB HKD SA | 31/3/25 | NCB HKD SA-2503-002 | GENJ | Bank interest income:Interest | 175.25 |  | 
- row 30: 1020 | NCB HKD SA | 30/4/25 | NCB HKD SA-2504-001 | GENJ | Bank interest income:Interest | 169.59 |  | 
- row 31: 1020 | NCB HKD SA | 31/5/25 | NCB HKD SA-2505-001 | GENJ | Bank interest income:Interest | 175.3 |  | 
- row 32: 1020 | NCB HKD SA | 20/6/25 | NCB HKD SA-2506-001 | GENJ | Interbank:transfer |  | 50000 | 
- row 33: 1020 | NCB HKD SA | 30/6/25 | NCB HKD SA-2506-002 | GENJ | Bank interest income:Interest | 164.56 |  | 
- row 34: 1020 | NCB HKD SA | 31/7/25 | NCB HKD SA-2507-001 | GENJ | Bank interest income:Interest | 159.48 |  | 
- row 35: 1020 | NCB HKD SA | 31/8/25 | NCB HKD SA-2508-001 | GENJ | Bank interest income:Interest | 113.22 |  | 

### PL 31.12.25
- row 1:  | Current Month |  | Year to Date | 
- row 2: Revenues |  |  |  | 
- row 3: Membership fee income | 116174 | 98.75753577276535 | 116174 | 98.75753577276535
- row 4: Bank interest income | 1461.58 | 1.242464227234651 | 1461.58 | 1.242464227234651
- row 6: Total Revenues | 117635.58 | 100 | 117635.58 | 100
- row 9: Cost of Sales |  |  |  | 
- row 11: Total Cost of Sales | 0 | 0 | 0 | 0
- row 13: Gross Profit | 117635.58 | 100 | 117635.58 | 100
- row 15: Expenses |  |  |  | 
- row 16: Accounting fee | 5000 | 4.250414712963544 | 5000 | 4.250414712963544
- row 17: Auditor's remuneration | 7200 | 6.120597186667503 | 7200 | 6.120597186667503
- row 18: Bank charges | 450 | 0.38253732416671893 | 450 | 0.38253732416671893
- row 19: Company secretarial fee | 4900 | 4.165406418704273 | 4900 | 4.165406418704273
- row 20: Computer accessories | 6844.32 | 5.8182396856461285 | 6844.32 | 5.8182396856461285
- row 21: Entertainment | 7241 | 6.155450587313805 | 7241 | 6.155450587313805
- row 22: Legal and professional fee | 23000 | 19.5519076796323 | 23000 | 19.5519076796323
- row 23: Web hosting fee | 38439.24 | 32.67654225022735 | 38439.24 | 32.67654225022735
- row 25: Total Expenses | 93074.56 | 79.1211 | 93074.56 | 79.1211
- row 27: Net Income | 24561.02 | 20.8789 | 24561.02 | 20.8789

### BS 31.12.25
- row 2: ASSETS |  | 
- row 4: Current Assets |  | 
- row 5: NCB HKD CA | 37231.66 | 
- row 6: NCB HKD SA | 603180.5 | 
- row 7: Trade receivable | 64000 | 
- row 8: Prepayment | 4900 | 
- row 10: Total Current Assets |  | 709312.16
- row 12: Property and Equipment |  | 
- row 13: Office equipment | 5750 | 
- row 14: Accum Depreciation-OE | -5750 | 
- row 16: Total Property and Equipment |  | 0
- row 18: Other Assets |  | 
- row 20: Total Other Assets |  | 0
- row 22: Total Assets |  | 709312.16
- row 26: LIABILITIES AND CAPITAL |  | 
- row 28: Current Liabilities |  | 
- row 29: Receipt in advance | 123310 | 
- row 30: Accruals | 12200 | 
- row 32: Total Current Liabilities |  | 135510
- row 34: Long-Term Liabilities |  | 
- row 36: Total Long-Term Liabilities |  | 0
- row 38: Total Liabilities |  | 135510
- row 40: Capital |  | 
- row 41: Retained Earnings | 549241.14 | 
- row 42: Net Income | 24561.02 | 
- row 44: Total Capital |  | 573802.16
- row 46: Total Liabilities & Capital |  | 709312.16
