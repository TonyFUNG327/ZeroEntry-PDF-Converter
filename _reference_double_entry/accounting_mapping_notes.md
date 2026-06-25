# Accounting Mapping Notes

## Bank record sheet: HSBC HKD CA

- Bank/account label: HSBC HKD C/A #123-456789-001
- Core input columns:
  A=No., B=Date, C=Particular, D=Payer / (Payee), E=Invoice no. (Cheque no.), F=Details, H=Deposit, I=Withdrawal, J=Balance, L=Control
- Accounting classification columns from row 7:
  N=Interbank; P=Computer ; Q=Furniture & fixtures; S=Director C/A; T=Accruals; V=Sales; W=Purchase; Y=Interest income; AA=Advertisement; AB=Bank charge; AC=Electricity & water; AD=Insurance; AE=Legal & professional fee; AF=Rental & rates; AG=Salaries; AH=Staff messing; AI=Staff training; AJ=Stamp duty; AK=Transportation; AM=Temp; AN=Suspense in; AO=Suspense out
- Sample transaction rows:
  - row 9: date=2020-03-09, particular=B/F BALANCE, deposit=, withdrawal=, balance=45, control=, classified=[]
  - row 10: date=2020-03-30, particular=CHEQUE, deposit=, withdrawal=-20000, balance==J9+H10+I10, control==SUM(H10:I10)-SUM(M10:AP10), classified=[]
  - row 11: date=2020-03-30, particular=FROM ABC LTD, deposit=20000, withdrawal=, balance==J10+H11+I11, control==SUM(H11:I11)-SUM(M11:AP11), classified=[]
  - row 12: date=2020-03-31, particular=E-CHEQUE, deposit=, withdrawal=-3400, balance==J11+H12+I12, control==SUM(H12:I12)-SUM(M12:AP12), classified=[]
  - row 13: date=2020-03-31, particular=E-CHEQUE, deposit=, withdrawal=-3975, balance==J12+H13+I13, control==SUM(H13:I13)-SUM(M13:AP13), classified=[]
  - row 14: date=2020-03-31, particular=FROM ABC LTD, deposit=3975, withdrawal=, balance==J13+H14+I14, control==SUM(H14:I14)-SUM(M14:AP14), classified=[]
  - row 15: date=2020-03-31, particular=FROM ABC LTD, deposit=3400, withdrawal=, balance==J14+H15+I15, control==SUM(H15:I15)-SUM(M15:AP15), classified=[]
  - row 16: date=, particular=, deposit=, withdrawal=, balance==J15+H16+I16, control==SUM(H16:I16)-SUM(M16:AP16), classified=[]
  - row 17: date=, particular=, deposit=, withdrawal=, balance==J16+H17+I17, control==SUM(H17:I17)-SUM(M17:AP17), classified=[]
  - row 18: date=, particular=, deposit=, withdrawal=, balance==J17+H18+I18, control==SUM(H18:I18)-SUM(M18:AP18), classified=[]
  - row 19: date=, particular=, deposit=, withdrawal=, balance==J18+H19+I19, control==SUM(H19:I19)-SUM(M19:AP19), classified=[]
  - row 20: date=, particular=, deposit=, withdrawal=, balance==J19+H20+I20, control==SUM(H20:I20)-SUM(M20:AP20), classified=[]

## Bank record sheet: USD SA

- Bank/account label: CBiBank USD S/A #900377047150
- Core input columns:
  A=No., B=Date, C=Particular, G=Deposit, H=Withdrawal, I=Balance, K=Deposit, L=Withdrawal
- Accounting classification columns from row 7:
  M=Balance; O=Control; Q=Interbank; S=Computer ; T=Furniture & fixtures; V=Director C/A; X=Sales; Y=Purchase; AA=Interest income; AC=Bank charge; AD=Electricity & water; AE=Insurance; AF=Legal & professional fee; AG=Rental & rates; AH=Salaries; AI=Staff messing; AJ=Staff training; AK=Stamp duty; AL=Transportation; AN=Temp; AO=Suspense in; AP=Suspense out
- Sample transaction rows:
  - row 9: date=2024-01-01, particular=, deposit=, withdrawal=295, balance=, control=, classified=[Balance=2301]
  - row 10: date=2024-01-05, particular=Bank charge, deposit=-20, withdrawal==I9+G10+H10, balance=, control==ROUND(H10*$L$6,2), classified=[]
  - row 11: date=2024-02-05, particular=Bank charge, deposit=-20, withdrawal==I10+G11+H11, balance=, control==ROUND(H11*$L$6,2), classified=[]
  - row 12: date=2024-03-05, particular=Bank charge, deposit=-20, withdrawal==I11+G12+H12, balance=, control==ROUND(H12*$L$6,2), classified=[]
  - row 13: date=2024-04-05, particular=Bank conf, deposit=-100, withdrawal==I12+G13+H13, balance=, control==ROUND(H13*$L$6,2), classified=[]
  - row 14: date=2024-05-05, particular=Bank charge, deposit=-20, withdrawal==I13+G14+H14, balance=, control==ROUND(H14*$L$6,2), classified=[]
  - row 15: date=2024-06-05, particular=Bank charge, deposit=-20, withdrawal==I14+G15+H15, balance=, control==ROUND(H15*$L$6,2), classified=[]
  - row 16: date=2024-07-05, particular=Bank charge, deposit=-20, withdrawal==I15+G16+H16, balance=, control==ROUND(H16*$L$6,2), classified=[]
  - row 17: date=2024-08-05, particular=Bank charge, deposit=-20, withdrawal==I16+G17+H17, balance=, control==ROUND(H17*$L$6,2), classified=[]
  - row 18: date=2024-09-05, particular=Bank charge, deposit=-20, withdrawal==I17+G18+H18, balance=, control==ROUND(H18*$L$6,2), classified=[]
  - row 19: date=, particular=, deposit=-20, withdrawal==I18+G19+H19, balance=, control==ROUND(H19*$L$6,2), classified=[]
  - row 20: date=, particular=, deposit=, withdrawal==I19+G20+H20, balance=, control==ROUND(H20*$L$6,2), classified=[]

## Report sheet: TB-31.12.24

- row 1: Account ID | Account Description | Debit Amt | Credit Amt
- row 2: 1040 | CBiBank USD SA | 117 | 
- row 3: 1300 | Prepayment | 2910.6 | 
- row 4: 2200 | Accruals |  | 4700
- row 5: 2400 | Director's C/A |  | 18347.1
- row 6: 3920 | Share capital |  | 1
- row 7: 3950 | Retained earnings | 7851 | 
- row 8: 6100 | Auditor's remuneration | 4700 | 
- row 9: 6200 | Bank charges | 2184 | 
- row 10: 6220 | Building management fee | 525.8 | 
- row 11: 6250 | Business registration fee | 2200 | 
- row 12: 7200 | Rental expenses | 2559.7 | 
- row 14:  | Total: | =SUBTOTAL(9, C2:C13) | =SUBTOTAL(9, D2:D13)

## Report sheet: GL-31.12.24

- row 1: Account ID | Account Description | Date | Reference | Jrnl | Trans Description | Debit Amt | Credit Amt | Balance
- row 2: 1040 | CBiBank USD SA | 45292 |  |  | Beginning Balance |  |  | 
- row 3: 1040 | CBiBank USD SA | 45292 | Opening balance | GENJ | CBiBank USD SA-Opening balance | 2301 |  | 
- row 4: 1040 | CBiBank USD SA | 45292 | CBiBank USD SA 2412 | GENJ | Total Withdrawal-2412 |  | 2184 | 
- row 5: 1040 | CBiBank USD SA |  |  |  | Change | 2301 | 2184 | =G5-H5
- row 6:  |  | 31/12/24 |  |  | Ending Balance |  |  | =SUBTOTAL(9, I2:I5)
- row 7: 1300 | Prepayment | 45292 |  |  | Beginning Balance |  |  | 
- row 8: 1300 | Prepayment | 31/12/24 | CASH 2412 | GENJ | Total prepayment | 2910.6 |  | 
- row 9: 1300 | Prepayment |  |  |  | Change | 2910.6 |  | =G9-H9
- row 10:  |  | 31/12/24 |  |  | Ending Balance |  |  | =SUBTOTAL(9, I7:I9)
- row 11: 2200 | Accruals | 45292 |  |  | Beginning Balance |  |  | 
- row 12: 2200 | Accruals | 45292 | Opening balance | GENJ | Accruals-Opening balance |  | 5200 | 
- row 13: 2200 | Accruals | 31/12/24 | JV2412001 | GENJ | Being recognized of audit fee for the year |  | 4700 | 
- row 14: 2200 | Accruals | 31/12/24 | JV2412002 | GENJ | Being settlement of accruals for last year | 5200 |  | 
- row 15: 2200 | Accruals |  |  |  | Change | 5200 | 9900 | =G15-H15
- row 16:  |  | 31/12/24 |  |  | Ending Balance |  |  | =SUBTOTAL(9, I11:I15)
- row 17: 2400 | Director's C/A | 45292 |  |  | Beginning Balance |  |  | 
- row 18: 2400 | Director's C/A | 45292 | Opening balance | GENJ | Director's CA-Opening balance |  | 4951 | 
- row 19: 2400 | Director's C/A | 31/12/24 | CASH 2412 | GENJ | Total cash out-2412 |  | 5996.1 | 
- row 20: 2400 | Director's C/A | 31/12/24 | JV2412002 | GENJ | Being settlement of accruals for last year |  | 5200 | 
- row 21: 2400 | Director's C/A | 31/12/24 | JV2412003 | GENJ | Being recognized of BR fee for the year |  | 2200 | 
- row 22: 2400 | Director's C/A |  |  |  | Change |  | 18347.1 | =G22-H22
- row 23:  |  | 31/12/24 |  |  | Ending Balance |  |  | =SUBTOTAL(9, I17:I22)
- row 24: 3920 | Share capital | 45292 |  |  | Beginning Balance |  |  | 
- row 25: 3920 | Share capital | 45292 | Opening balance | GENJ | Share capital-Opening balance |  | 1 | 
- row 26: 3920 | Share capital |  |  |  | Change |  | 1 | =G26-H26
- row 27:  |  | 31/12/24 |  |  | Ending Balance |  |  | =SUBTOTAL(9, I24:I26)
- row 28: 3950 | Retained earnings | 45292 |  |  | Beginning Balance |  |  | 
- row 29: 3950 | Retained earnings | 45292 | Opening balance | GENJ | Retained earnings-Opening balance | 7851 |  | 
- row 30: 3950 | Retained earnings |  |  |  | Change | 7851 |  | =G30-H30
- row 31:  |  | 31/12/24 |  |  | Ending Balance |  |  | =SUBTOTAL(9, I28:I30)
- row 32: 6100 | Auditor's remuneration | 45292 |  |  | Beginning Balance |  |  | 
- row 33: 6100 | Auditor's remuneration | 31/12/24 | JV2412001 | GENJ | Being recognized of audit fee for the year | 4700 |  | 
- row 34: 6100 | Auditor's remuneration |  |  |  | Change | 4700 |  | =G34-H34
- row 35:  |  | 31/12/24 |  |  | Ending Balance |  |  | =SUBTOTAL(9, I32:I34)
- row 36: 6200 | Bank charges | 45292 |  |  | Beginning Balance |  |  | 
- row 37: 6200 | Bank charges | 45292 | CBiBank USD SA 2412 | GENJ | Total Bank charges-2412 | 2184 |  | 
- row 38: 6200 | Bank charges |  |  |  | Change | 2184 |  | =G38-H38
- row 39:  |  | 31/12/24 |  |  | Ending Balance |  |  | =SUBTOTAL(9, I36:I38)
- row 40: 6220 | Building management fee | 45292 |  |  | Beginning Balance |  |  | 
- row 41: 6220 | Building management fee | 31/12/24 | CASH 2412 | GENJ | Total Building management fee-2412 | 525.8 |  | 
- row 42: 6220 | Building management fee |  |  |  | Change | 525.8 |  | =G42-H42
- row 43:  |  | 31/12/24 |  |  | Ending Balance |  |  | =SUBTOTAL(9, I40:I42)
- row 44: 6250 | Business registration fee | 45292 |  |  | Beginning Balance |  |  | 
- row 45: 6250 | Business registration fee | 31/12/24 | JV2412003 | GENJ | Being recognized of BR fee for the year | 2200 |  | 
- row 46: 6250 | Business registration fee |  |  |  | Change | 2200 |  | =G46-H46
- row 47:  |  | 31/12/24 |  |  | Ending Balance |  |  | =SUBTOTAL(9, I44:I46)
- row 48: 7200 | Rental expenses | 45292 |  |  | Beginning Balance |  |  | 
- row 49: 7200 | Rental expenses | 31/12/24 | CASH 2412 | GENJ | Total Rental expenses-2412 | 2559.7 |  | 
- row 50: 7200 | Rental expenses |  |  |  | Change | 2559.7 |  | =G50-H50
- row 51:  |  | 31/12/24 |  |  | Ending Balance |  |  | =SUBTOTAL(9, I48:I50)

## Report sheet: BS 31.12.24

- row 2: ASSETS |  | 
- row 4: Current Assets |  | 
- row 5: CBiBank USD SA | 117 | 
- row 6: Prepayment | 2910.6 | 
- row 8: Total Current Assets |  | =ROUND(SUBTOTAL(9, B2:B7), 5)
- row 10: Property and Equipment |  | 
- row 12: Total Property and Equipment |  | =ROUND(SUBTOTAL(9, C9:C11), 5)
- row 14: Other Assets |  | 
- row 16: Total Other Assets |  | =ROUND(SUBTOTAL(9, C13:C15), 5)
- row 18: Total Assets |  | =ROUND(C8+C12+C16, 5)
- row 22: LIABILITIES AND CAPITAL |  | 
- row 24: Current Liabilities |  | 
- row 25: Accruals | 4700 | 
- row 26: Director's C/A | 18347.1 | 
- row 28: Total Current Liabilities |  | =ROUND(SUBTOTAL(9, B20:B27), 5)
- row 30: Long-Term Liabilities |  | 
- row 32: Total Long-Term Liabilities |  | =ROUND(SUBTOTAL(9, C29:C31), 5)
- row 34: Total Liabilities |  | =-(ROUND(-C28+-C32, 5))
- row 36: Capital |  | 
- row 37: Share capital | 1 | 
- row 38: Retained earnings | -7851 | 
- row 39: Net Income | -12169.5 | 
- row 41: Total Capital |  | =ROUND(SUBTOTAL(9, B35:B40), 5)
- row 43: Total Liabilities & Capital |  | =-(ROUND(-C34+-C41, 5))

## Report sheet: PL 31.12.24

- row 1:  | Current Month |  | Year to Date | 
- row 2: Revenues |  |  |  | 
- row 4: Total Revenues | =ROUND(SUBTOTAL(9, B2:B3), 5) | =ROUND(SUBTOTAL(9, C2:C3), 5) | =ROUND(SUBTOTAL(9, D2:D3), 5) | =ROUND(SUBTOTAL(9, E2:E3), 5)
- row 7: Cost of Sales |  |  |  | 
- row 9: Total Cost of Sales | =ROUND(SUBTOTAL(9, B6:B8), 5) | =ROUND(SUBTOTAL(9, C6:C8), 5) | =ROUND(SUBTOTAL(9, D6:D8), 5) | =ROUND(SUBTOTAL(9, E6:E8), 5)
- row 11: Gross Profit | =-(ROUND(-B4+B9, 5)) | =-(ROUND(-C4+C9, 5)) | =-(ROUND(-D4+D9, 5)) | =-(ROUND(-E4+E9, 5))
- row 13: Expenses |  |  |  | 
- row 14: Auditor's remuneration | 4700 | =IF(0<>0, (B14/0)*100, 0) | 4700 | =IF(0<>0, (D14/0)*100, 0)
- row 15: Bank charges | 2184 | =IF(0<>0, (B15/0)*100, 0) | 2184 | =IF(0<>0, (D15/0)*100, 0)
- row 16: Building management fee | 525.8 | =IF(0<>0, (B16/0)*100, 0) | 525.8 | =IF(0<>0, (D16/0)*100, 0)
- row 17: Business registration fee | 2200 | =IF(0<>0, (B17/0)*100, 0) | 2200 | =IF(0<>0, (D17/0)*100, 0)
- row 18: Rental expenses | 2559.7 | =IF(0<>0, (B18/0)*100, 0) | 2559.7 | =IF(0<>0, (D18/0)*100, 0)
- row 20: Total Expenses | =ROUND(SUBTOTAL(9, B13:B19), 5) | =ROUND(SUBTOTAL(9, C13:C19), 5) | =ROUND(SUBTOTAL(9, D13:D19), 5) | =ROUND(SUBTOTAL(9, E13:E19), 5)
- row 22: Net Income | =-(ROUND(-B11+B20, 5)) | =-(ROUND(-C11+C20, 5)) | =-(ROUND(-D11+D20, 5)) | =-(ROUND(-E11+E20, 5))

# Report Values Snapshot

## Report sheet: TB-31.12.24

- row 1: Account ID | Account Description | Debit Amt | Credit Amt
- row 2: 1040 | CBiBank USD SA | 117 | 
- row 3: 1300 | Prepayment | 2910.6 | 
- row 4: 2200 | Accruals |  | 4700
- row 5: 2400 | Director's C/A |  | 18347.1
- row 6: 3920 | Share capital |  | 1
- row 7: 3950 | Retained earnings | 7851 | 
- row 8: 6100 | Auditor's remuneration | 4700 | 
- row 9: 6200 | Bank charges | 2184 | 
- row 10: 6220 | Building management fee | 525.8 | 
- row 11: 6250 | Business registration fee | 2200 | 
- row 12: 7200 | Rental expenses | 2559.7 | 
- row 14:  | Total: | 23048.1 | 23048.1

## Report sheet: GL-31.12.24

- row 1: Account ID | Account Description | Date | Reference | Jrnl | Trans Description | Debit Amt | Credit Amt | Balance
- row 2: 1040 | CBiBank USD SA | 45292 |  |  | Beginning Balance |  |  | 
- row 3: 1040 | CBiBank USD SA | 45292 | Opening balance | GENJ | CBiBank USD SA-Opening balance | 2301 |  | 
- row 4: 1040 | CBiBank USD SA | 45292 | CBiBank USD SA 2412 | GENJ | Total Withdrawal-2412 |  | 2184 | 
- row 5: 1040 | CBiBank USD SA |  |  |  | Change | 2301 | 2184 | 117
- row 6:  |  | 31/12/24 |  |  | Ending Balance |  |  | 117
- row 7: 1300 | Prepayment | 45292 |  |  | Beginning Balance |  |  | 
- row 8: 1300 | Prepayment | 31/12/24 | CASH 2412 | GENJ | Total prepayment | 2910.6 |  | 
- row 9: 1300 | Prepayment |  |  |  | Change | 2910.6 |  | 2910.6
- row 10:  |  | 31/12/24 |  |  | Ending Balance |  |  | 2910.6
- row 11: 2200 | Accruals | 45292 |  |  | Beginning Balance |  |  | 
- row 12: 2200 | Accruals | 45292 | Opening balance | GENJ | Accruals-Opening balance |  | 5200 | 
- row 13: 2200 | Accruals | 31/12/24 | JV2412001 | GENJ | Being recognized of audit fee for the year |  | 4700 | 
- row 14: 2200 | Accruals | 31/12/24 | JV2412002 | GENJ | Being settlement of accruals for last year | 5200 |  | 
- row 15: 2200 | Accruals |  |  |  | Change | 5200 | 9900 | -4700
- row 16:  |  | 31/12/24 |  |  | Ending Balance |  |  | -4700
- row 17: 2400 | Director's C/A | 45292 |  |  | Beginning Balance |  |  | 
- row 18: 2400 | Director's C/A | 45292 | Opening balance | GENJ | Director's CA-Opening balance |  | 4951 | 
- row 19: 2400 | Director's C/A | 31/12/24 | CASH 2412 | GENJ | Total cash out-2412 |  | 5996.1 | 
- row 20: 2400 | Director's C/A | 31/12/24 | JV2412002 | GENJ | Being settlement of accruals for last year |  | 5200 | 
- row 21: 2400 | Director's C/A | 31/12/24 | JV2412003 | GENJ | Being recognized of BR fee for the year |  | 2200 | 
- row 22: 2400 | Director's C/A |  |  |  | Change |  | 18347.1 | -18347.1
- row 23:  |  | 31/12/24 |  |  | Ending Balance |  |  | -18347.1
- row 24: 3920 | Share capital | 45292 |  |  | Beginning Balance |  |  | 
- row 25: 3920 | Share capital | 45292 | Opening balance | GENJ | Share capital-Opening balance |  | 1 | 
- row 26: 3920 | Share capital |  |  |  | Change |  | 1 | -1
- row 27:  |  | 31/12/24 |  |  | Ending Balance |  |  | -1
- row 28: 3950 | Retained earnings | 45292 |  |  | Beginning Balance |  |  | 
- row 29: 3950 | Retained earnings | 45292 | Opening balance | GENJ | Retained earnings-Opening balance | 7851 |  | 
- row 30: 3950 | Retained earnings |  |  |  | Change | 7851 |  | 7851
- row 31:  |  | 31/12/24 |  |  | Ending Balance |  |  | 7851
- row 32: 6100 | Auditor's remuneration | 45292 |  |  | Beginning Balance |  |  | 
- row 33: 6100 | Auditor's remuneration | 31/12/24 | JV2412001 | GENJ | Being recognized of audit fee for the year | 4700 |  | 
- row 34: 6100 | Auditor's remuneration |  |  |  | Change | 4700 |  | 4700
- row 35:  |  | 31/12/24 |  |  | Ending Balance |  |  | 4700
- row 36: 6200 | Bank charges | 45292 |  |  | Beginning Balance |  |  | 
- row 37: 6200 | Bank charges | 45292 | CBiBank USD SA 2412 | GENJ | Total Bank charges-2412 | 2184 |  | 
- row 38: 6200 | Bank charges |  |  |  | Change | 2184 |  | 2184
- row 39:  |  | 31/12/24 |  |  | Ending Balance |  |  | 2184
- row 40: 6220 | Building management fee | 45292 |  |  | Beginning Balance |  |  | 
- row 41: 6220 | Building management fee | 31/12/24 | CASH 2412 | GENJ | Total Building management fee-2412 | 525.8 |  | 
- row 42: 6220 | Building management fee |  |  |  | Change | 525.8 |  | 525.8
- row 43:  |  | 31/12/24 |  |  | Ending Balance |  |  | 525.8
- row 44: 6250 | Business registration fee | 45292 |  |  | Beginning Balance |  |  | 
- row 45: 6250 | Business registration fee | 31/12/24 | JV2412003 | GENJ | Being recognized of BR fee for the year | 2200 |  | 
- row 46: 6250 | Business registration fee |  |  |  | Change | 2200 |  | 2200
- row 47:  |  | 31/12/24 |  |  | Ending Balance |  |  | 2200
- row 48: 7200 | Rental expenses | 45292 |  |  | Beginning Balance |  |  | 
- row 49: 7200 | Rental expenses | 31/12/24 | CASH 2412 | GENJ | Total Rental expenses-2412 | 2559.7 |  | 
- row 50: 7200 | Rental expenses |  |  |  | Change | 2559.7 |  | 2559.7
- row 51:  |  | 31/12/24 |  |  | Ending Balance |  |  | 2559.7

## Report sheet: BS 31.12.24

- row 2: ASSETS |  | 
- row 4: Current Assets |  | 
- row 5: CBiBank USD SA | 117 | 
- row 6: Prepayment | 2910.6 | 
- row 8: Total Current Assets |  | 3027.6
- row 10: Property and Equipment |  | 
- row 12: Total Property and Equipment |  | 0
- row 14: Other Assets |  | 
- row 16: Total Other Assets |  | 0
- row 18: Total Assets |  | 3027.6
- row 22: LIABILITIES AND CAPITAL |  | 
- row 24: Current Liabilities |  | 
- row 25: Accruals | 4700 | 
- row 26: Director's C/A | 18347.1 | 
- row 28: Total Current Liabilities |  | 23047.1
- row 30: Long-Term Liabilities |  | 
- row 32: Total Long-Term Liabilities |  | 0
- row 34: Total Liabilities |  | 23047.1
- row 36: Capital |  | 
- row 37: Share capital | 1 | 
- row 38: Retained earnings | -7851 | 
- row 39: Net Income | -12169.5 | 
- row 41: Total Capital |  | -20019.5
- row 43: Total Liabilities & Capital |  | 3027.6

## Report sheet: PL 31.12.24

- row 1:  | Current Month |  | Year to Date | 
- row 2: Revenues |  |  |  | 
- row 4: Total Revenues | 0 | 0 | 0 | 0
- row 7: Cost of Sales |  |  |  | 
- row 9: Total Cost of Sales | 0 | 0 | 0 | 0
- row 11: Gross Profit | 0 | 0 | 0 | 0
- row 13: Expenses |  |  |  | 
- row 14: Auditor's remuneration | 4700 | 0 | 4700 | 0
- row 15: Bank charges | 2184 | 0 | 2184 | 0
- row 16: Building management fee | 525.8 | 0 | 525.8 | 0
- row 17: Business registration fee | 2200 | 0 | 2200 | 0
- row 18: Rental expenses | 2559.7 | 0 | 2559.7 | 0
- row 20: Total Expenses | 12169.5 | 0 | 12169.5 | 0
- row 22: Net Income | -12169.5 | 0 | -12169.5 | 0
