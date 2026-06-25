# I026 Accounting Mapping Notes

## Workbook Overview
- bank_record: 001-I026-Bank record-31.12.25.converted.xlsx
  - NCB HKD SA: rows=105, cols=67, used={'min_row': 1, 'min_col': 1, 'max_row': 105, 'max_col': 64}, header_row=9, formulas_sampled=25
  - NCB HKD CA: rows=106, cols=65, used={'min_row': 1, 'min_col': 1, 'max_row': 105, 'max_col': 64}, header_row=9, formulas_sampled=25
  - HSBC USD SA: rows=105, cols=69, used={'min_row': 1, 'min_col': 1, 'max_row': 105, 'max_col': 68}, header_row=9, formulas_sampled=25
  - Finance costs: rows=106, cols=65, used={'min_row': 1, 'min_col': 1, 'max_row': 105, 'max_col': 64}, header_row=9, formulas_sampled=25
  - Chart of Accounts: rows=107, cols=2, used={'min_row': 1, 'min_col': 1, 'max_row': 94, 'max_col': 2}, header_row=None, formulas_sampled=0
- reports: 002-I026-TB, GL, PL, BS-31.12.25.xlsx
  - TB 31.12.25: rows=23, cols=5, used={'min_row': 1, 'min_col': 1, 'max_row': 22, 'max_col': 4}, header_row=None, formulas_sampled=2
  - GL 31.12.25: rows=168, cols=9, used={'min_row': 1, 'min_col': 1, 'max_row': 168, 'max_col': 9}, header_row=None, formulas_sampled=25
  - PL 31.12.25: rows=28, cols=5, used={'min_row': 1, 'min_col': 1, 'max_row': 27, 'max_col': 5}, header_row=None, formulas_sampled=25
  - BS 31.12.25: rows=47, cols=3, used={'min_row': 2, 'min_col': 1, 'max_row': 46, 'max_col': 3}, header_row=None, formulas_sampled=9

## Bank/Cash record sheet: NCB HKD SA

- Company: International Data Industry Alliance Limited
- Period: 1.1.25-31.12.25
- Account label: NCB HKD S/A #043-509-018239-2
- Detected transaction header row: 9
- header row 1: A=Company Name; C=International Data Industry Alliance Limited; G=Remind; H=- "+ve" for income, "-ve" for expenses
- header row 2: A=Period; C=1.1.25-31.12.25; H=- 1 file for each bank account
- header row 3: A=Bank record; C=NCB HKD S/A #043-509-018239-2
- header row 4: A=Bank COA:; C=NCB HKD SA
- header row 5: A=Bank name:; C=NCB HKD SA
- header row 8: BD=For Peachtree import use - Please don't move this column
- header row 9: A=No.; B=Date; C=Particular; I=Deposit; J=Withdrawal; K=Balance; M=Control; O=Interbank; Q=Computer equipment; R=Fixture & furniture; T=Director's C/A; V=Trade receivable; W=Receipt in advance; X=Accruals; Z=Membership fee income; AA=Purchases; AC=Bank interest income; AE=Director's remuneration; AF=Salaries; AG=Mandatory provident fund; AI=Advertisement; AJ=Bank charges; AK=Business registration fee; AL=Company secretary fee; AM=Electricity & water; AN=Entertainment; AO=Insurance; AP=Legal and professional fee; AQ=Local travelling; AR=Postage & courier; AS=Printing & stationery; AT=Rental expenses; AU=Staff welfare; AV=Stamp duty; AW=Telecommunication; AX=Transportation; AZ=Temp; BD=Date; BE=Reference; BG=Number of Distributions; BH=G/L Account ; BI=G/L Account ; BJ=Description; BK=Bank (Amount$); BL=Nature (Amount$)
- header row 10: A=No.; B=Date; C=Nature; D=Payer / (Payee); E=Invoice no. (Cheque no.); F=Details; G=Month-Year; BH==C4; BI=(Nature)
- header row 11: A=0; B=2025-01-01; C=Bank opening; K=550018.9199999998
- header row 12: A=2501-001; B=2025-01-31; C=Bank interest income; D=Interest; I=175.18; K==K11+I12+J12; M==SUM(I12:J12)-SUM(N12:BA12); O==IF($C12=O$9,$I12+$J12,0); Q==IF($C12=Q$9,$I12+$J12,0); R==IF($C12=R$9,$I12+$J12,0); T==IF($C12=T$9,$I12+$J12,0); V==IF($C12=V$9,$I12+$J12,0); W==IF($C12=W$9,$I12+$J12,0); X==IF($C12=X$9,$I12+$J12,0); Z==IF($C12=Z$9,$I12+$J12,0); AA==IF($C12=AA$9,$I12+$J12,0); AC==IF($C12=AC$9,$I12+$J12,0); AE==IF($C12=AE$9,$I12+$J12,0); AF==IF($C12=AF$9,$I12+$J12,0); AG==IF($C12=AG$9,$I12+$J12,0); AI==IF($C12=AI$9,$I12+$J12,0); AJ==IF($C12=AJ$9,$I12+$J12,0); AK==IF($C12=AK$9,$I12+$J12,0); AL==IF($C12=AL$9,$I12+$J12,0); AM==IF($C12=AM$9,$I12+$J12,0); AN==IF($C12=AN$9,$I12+$J12,0); AO==IF($C12=AO$9,$I12+$J12,0); AP==IF($C12=AP$9,$I12+$J12,0); AQ==IF($C12=AQ$9,$I12+$J12,0); AR==IF($C12=AR$9,$I12+$J12,0); AS==IF($C12=AS$9,$I12+$J12,0); AT==IF($C12=AT$9,$I12+$J12,0); AU==IF($C12=AU$9,$I12+$J12,0); AV==IF($C12=AV$9,$I12+$J12,0); AW==IF($C12=AW$9,$I12+$J12,0); AX==IF($C12=AX$9,$I12+$J12,0); AZ==IF($C12=AZ$9,$I12+$J12,0); BD==IF(B12="","",B12); BE==IF(C12="","",$C$5&"-"&A12); BG==IF(BE12="","",COUNTIF(BE:BE,BE12)*2); BH==IF(C12="","",IF($C$4="","",VLOOKUP($C$4,'Chart of Accounts'!$A:$B,2,FALSE))); BI==IF(C12="","",VLOOKUP(C:C,'Chart of Accounts'!$A:$B,2,FALSE)); BJ==IF(C12="","",C12&":"&D12&IF(E12="",""," - "&E12)&IF(F12="",""," - "&F12)&IF(G12="",""," - "&TEXT(G12,"MMM-YY"))); BK==SUM(I12:J12); BL==-BK12
- header row 13: A=2502-001; B=2025-02-28; C=Bank interest income; D=Interest; I=158.27; K==K12+I13+J13; M==SUM(I13:J13)-SUM(N13:BA13); O==IF($C13=O$9,$I13+$J13,0); Q==IF($C13=Q$9,$I13+$J13,0); R==IF($C13=R$9,$I13+$J13,0); T==IF($C13=T$9,$I13+$J13,0); V==IF($C13=V$9,$I13+$J13,0); W==IF($C13=W$9,$I13+$J13,0); X==IF($C13=X$9,$I13+$J13,0); Z==IF($C13=Z$9,$I13+$J13,0); AA==IF($C13=AA$9,$I13+$J13,0); AC==IF($C13=AC$9,$I13+$J13,0); AE==IF($C13=AE$9,$I13+$J13,0); AF==IF($C13=AF$9,$I13+$J13,0); AG==IF($C13=AG$9,$I13+$J13,0); AI==IF($C13=AI$9,$I13+$J13,0); AJ==IF($C13=AJ$9,$I13+$J13,0); AK==IF($C13=AK$9,$I13+$J13,0); AL==IF($C13=AL$9,$I13+$J13,0); AM==IF($C13=AM$9,$I13+$J13,0); AN==IF($C13=AN$9,$I13+$J13,0); AO==IF($C13=AO$9,$I13+$J13,0); AP==IF($C13=AP$9,$I13+$J13,0); AQ==IF($C13=AQ$9,$I13+$J13,0); AR==IF($C13=AR$9,$I13+$J13,0); AS==IF($C13=AS$9,$I13+$J13,0); AT==IF($C13=AT$9,$I13+$J13,0); AU==IF($C13=AU$9,$I13+$J13,0); AV==IF($C13=AV$9,$I13+$J13,0); AW==IF($C13=AW$9,$I13+$J13,0); AX==IF($C13=AX$9,$I13+$J13,0); AZ==IF($C13=AZ$9,$I13+$J13,0); BD==IF(B13="","",B13); BE==IF(C13="","",$C$5&"-"&A13); BG==IF(BE13="","",COUNTIF(BE:BE,BE13)*2); BH==IF(C13="","",IF($C$4="","",VLOOKUP($C$4,'Chart of Accounts'!$A:$B,2,FALSE))); BI==IF(C13="","",VLOOKUP(C:C,'Chart of Accounts'!$A:$B,2,FALSE)); BJ==IF(C13="","",C13&":"&D13&IF(E13="",""," - "&E13)&IF(F13="",""," - "&F13)&IF(G13="",""," - "&TEXT(G13,"MMM-YY"))); BK==SUM(I13:J13); BL==-BK13
- header row 14: A=2503-001; B=2025-03-30; C=Bank charges; D=Auditor’s Confirmation; J=-300; K==K13+I14+J14; M==SUM(I14:J14)-SUM(N14:BA14); O==IF($C14=O$9,$I14+$J14,0); Q==IF($C14=Q$9,$I14+$J14,0); R==IF($C14=R$9,$I14+$J14,0); T==IF($C14=T$9,$I14+$J14,0); V==IF($C14=V$9,$I14+$J14,0); W==IF($C14=W$9,$I14+$J14,0); X==IF($C14=X$9,$I14+$J14,0); Z==IF($C14=Z$9,$I14+$J14,0); AA==IF($C14=AA$9,$I14+$J14,0); AC==IF($C14=AC$9,$I14+$J14,0); AE==IF($C14=AE$9,$I14+$J14,0); AF==IF($C14=AF$9,$I14+$J14,0); AG==IF($C14=AG$9,$I14+$J14,0); AI==IF($C14=AI$9,$I14+$J14,0); AJ==IF($C14=AJ$9,$I14+$J14,0); AK==IF($C14=AK$9,$I14+$J14,0); AL==IF($C14=AL$9,$I14+$J14,0); AM==IF($C14=AM$9,$I14+$J14,0); AN==IF($C14=AN$9,$I14+$J14,0); AO==IF($C14=AO$9,$I14+$J14,0); AP==IF($C14=AP$9,$I14+$J14,0); AQ==IF($C14=AQ$9,$I14+$J14,0); AR==IF($C14=AR$9,$I14+$J14,0); AS==IF($C14=AS$9,$I14+$J14,0); AT==IF($C14=AT$9,$I14+$J14,0); AU==IF($C14=AU$9,$I14+$J14,0); AV==IF($C14=AV$9,$I14+$J14,0); AW==IF($C14=AW$9,$I14+$J14,0); AX==IF($C14=AX$9,$I14+$J14,0); AZ==IF($C14=AZ$9,$I14+$J14,0); BD==IF(B14="","",B14); BE==IF(C14="","",$C$5&"-"&A14); BG==IF(BE14="","",COUNTIF(BE:BE,BE14)*2); BH==IF(C14="","",IF($C$4="","",VLOOKUP($C$4,'Chart of Accounts'!$A:$B,2,FALSE))); BI==IF(C14="","",VLOOKUP(C:C,'Chart of Accounts'!$A:$B,2,FALSE)); BJ==IF(C14="","",C14&":"&D14&IF(E14="",""," - "&E14)&IF(F14="",""," - "&F14)&IF(G14="",""," - "&TEXT(G14,"MMM-YY"))); BK==SUM(I14:J14); BL==-BK14
- header row 15: A=2503-002; B=2025-03-31; C=Bank interest income; D=Interest; I=175.25; K==K14+I15+J15; M==SUM(I15:J15)-SUM(N15:BA15); O==IF($C15=O$9,$I15+$J15,0); Q==IF($C15=Q$9,$I15+$J15,0); R==IF($C15=R$9,$I15+$J15,0); T==IF($C15=T$9,$I15+$J15,0); V==IF($C15=V$9,$I15+$J15,0); W==IF($C15=W$9,$I15+$J15,0); X==IF($C15=X$9,$I15+$J15,0); Z==IF($C15=Z$9,$I15+$J15,0); AA==IF($C15=AA$9,$I15+$J15,0); AC==IF($C15=AC$9,$I15+$J15,0); AE==IF($C15=AE$9,$I15+$J15,0); AF==IF($C15=AF$9,$I15+$J15,0); AG==IF($C15=AG$9,$I15+$J15,0); AI==IF($C15=AI$9,$I15+$J15,0); AJ==IF($C15=AJ$9,$I15+$J15,0); AK==IF($C15=AK$9,$I15+$J15,0); AL==IF($C15=AL$9,$I15+$J15,0); AM==IF($C15=AM$9,$I15+$J15,0); AN==IF($C15=AN$9,$I15+$J15,0); AO==IF($C15=AO$9,$I15+$J15,0); AP==IF($C15=AP$9,$I15+$J15,0); AQ==IF($C15=AQ$9,$I15+$J15,0); AR==IF($C15=AR$9,$I15+$J15,0); AS==IF($C15=AS$9,$I15+$J15,0); AT==IF($C15=AT$9,$I15+$J15,0); AU==IF($C15=AU$9,$I15+$J15,0); AV==IF($C15=AV$9,$I15+$J15,0); AW==IF($C15=AW$9,$I15+$J15,0); AX==IF($C15=AX$9,$I15+$J15,0); AZ==IF($C15=AZ$9,$I15+$J15,0); BD==IF(B15="","",B15); BE==IF(C15="","",$C$5&"-"&A15); BG==IF(BE15="","",COUNTIF(BE:BE,BE15)*2); BH==IF(C15="","",IF($C$4="","",VLOOKUP($C$4,'Chart of Accounts'!$A:$B,2,FALSE))); BI==IF(C15="","",VLOOKUP(C:C,'Chart of Accounts'!$A:$B,2,FALSE)); BJ==IF(C15="","",C15&":"&D15&IF(E15="",""," - "&E15)&IF(F15="",""," - "&F15)&IF(G15="",""," - "&TEXT(G15,"MMM-YY"))); BK==SUM(I15:J15); BL==-BK15
- Header labels:
  A=No.; B=Date; C=Particular; I=Deposit; J=Withdrawal; K=Balance; M=Control; O=Interbank; Q=Computer equipment; R=Fixture & furniture; T=Director's C/A; V=Trade receivable; W=Receipt in advance; X=Accruals; Z=Membership fee income; AA=Purchases; AC=Bank interest income; AE=Director's remuneration; AF=Salaries; AG=Mandatory provident fund; AI=Advertisement; AJ=Bank charges; AK=Business registration fee; AL=Company secretary fee; AM=Electricity & water; AN=Entertainment; AO=Insurance; AP=Legal and professional fee; AQ=Local travelling; AR=Postage & courier; AS=Printing & stationery; AT=Rental expenses; AU=Staff welfare; AV=Stamp duty; AW=Telecommunication; AX=Transportation; AZ=Temp; BD=Date; BE=Reference; BG=Number of Distributions; BH=G/L Account ; BI=G/L Account ; BJ=Description; BK=Bank (Amount$); BL=Nature (Amount$)
- Peachtree/helper columns:
  BE=Reference; BG=Number of Distributions; BJ=Description; BK=Bank (Amount$); BL=Nature (Amount$)
- First active rows:
  - row 11: 0 | 2025-01-01 | Bank opening |  |  |  |  |  |  || K:Balance=550018.9199999998
  - row 12: 2501-001 | 2025-01-31 | Bank interest income | Interest |  |  |  |  | 175.18 || I:Deposit=175.18; K:Balance=550194.0999999999; AC:Bank interest income=175.18; BG:Number of Distributions=2; BK:Bank (Amount$)=175.18; BL:Nature (Amount$)=-175.18
  - row 13: 2502-001 | 2025-02-28 | Bank interest income | Interest |  |  |  |  | 158.27 || I:Deposit=158.27; K:Balance=550352.3699999999; AC:Bank interest income=158.27; BG:Number of Distributions=2; BK:Bank (Amount$)=158.27; BL:Nature (Amount$)=-158.27
  - row 14: 2503-001 | 2025-03-30 | Bank charges | Auditor’s Confirmation |  |  |  |  |  || J:Withdrawal=-300; K:Balance=550052.3699999999; AJ:Bank charges=-300; BG:Number of Distributions=2; BK:Bank (Amount$)=-300; BL:Nature (Amount$)=300
  - row 15: 2503-002 | 2025-03-31 | Bank interest income | Interest |  |  |  |  | 175.25 || I:Deposit=175.25; K:Balance=550227.6199999999; AC:Bank interest income=175.25; BG:Number of Distributions=2; BK:Bank (Amount$)=175.25; BL:Nature (Amount$)=-175.25
  - row 16: 2504-001 | 2025-04-30 | Bank interest income | Interest |  |  |  |  | 169.59 || I:Deposit=169.59; K:Balance=550397.2099999998; AC:Bank interest income=169.59; BG:Number of Distributions=2; BK:Bank (Amount$)=169.59; BL:Nature (Amount$)=-169.59
  - row 17: 2505-001 | 2025-05-31 | Bank interest income | Interest |  |  |  |  | 175.3 || I:Deposit=175.3; K:Balance=550572.5099999999; AC:Bank interest income=175.3; BG:Number of Distributions=2; BK:Bank (Amount$)=175.3; BL:Nature (Amount$)=-175.3
  - row 18: 2506-001 | 2025-06-20 | Interbank | transfer |  |  |  |  |  || J:Withdrawal=-50000; K:Balance=500572.5099999999; O:Interbank=-50000; BG:Number of Distributions=2; BK:Bank (Amount$)=-50000; BL:Nature (Amount$)=50000
  - row 19: 2506-002 | 2025-06-30 | Bank interest income | Interest |  |  |  |  | 164.56 || I:Deposit=164.56; K:Balance=500737.0699999999; AC:Bank interest income=164.56; BG:Number of Distributions=2; BK:Bank (Amount$)=164.56; BL:Nature (Amount$)=-164.56
  - row 20: 2507-001 | 2025-07-31 | Bank interest income | Interest |  |  |  |  | 159.48 || I:Deposit=159.48; K:Balance=500896.5499999999; AC:Bank interest income=159.48; BG:Number of Distributions=2; BK:Bank (Amount$)=159.48; BL:Nature (Amount$)=-159.48
  - row 21: 2508-001 | 2025-08-31 | Bank interest income | Interest |  |  |  |  | 113.22 || I:Deposit=113.22; K:Balance=501009.76999999984; AC:Bank interest income=113.22; BG:Number of Distributions=2; BK:Bank (Amount$)=113.22; BL:Nature (Amount$)=-113.22
  - row 22: 2509-001 | 2025-09-18 | Membership fee income | Cheque Deposit NO.189888 | 2025-M-70105 | MTR Corporation Limited |  |  | 6668 || I:Deposit=6668; K:Balance=507677.76999999984; Z:Membership fee income=6668; BG:Number of Distributions=4; BK:Bank (Amount$)=6668; BL:Nature (Amount$)=-6668
  - row 23: 2509-001 | 2025-09-18 | Receipt in advance | Cheque Deposit NO.189888 | 2025-M-70105 | MTR Corporation Limited |  |  | 13332 || I:Deposit=13332; K:Balance=521009.76999999984; W:Receipt in advance=13332; BG:Number of Distributions=4; BK:Bank (Amount$)=13332; BL:Nature (Amount$)=-13332
  - row 24: 2509-002 | 2025-09-22 | Membership fee income | FPS IN CR | 2025-M-70104 | Hong Kong Exchanges and Clearing Limited |  |  | 8335 || I:Deposit=8335; K:Balance=529344.7699999998; Z:Membership fee income=8335; BG:Number of Distributions=4; BK:Bank (Amount$)=8335; BL:Nature (Amount$)=-8335
  - row 25: 2509-002 | 2025-09-22 | Receipt in advance | FPS IN CR | 2025-M-70104 | Hong Kong Exchanges and Clearing Limited |  |  | 11665 || I:Deposit=11665; K:Balance=541009.7699999998; W:Receipt in advance=11665; BG:Number of Distributions=4; BK:Bank (Amount$)=11665; BL:Nature (Amount$)=-11665
  - row 26: 2509-003 | 2025-09-29 | Receipt in advance | NYITT250188772//NYITT250188772 | 2025-MSHK-60101 | Microsoft Hong Kong Limited |  |  | 60000 || I:Deposit=60000; K:Balance=601009.7699999998; W:Receipt in advance=60000; BG:Number of Distributions=2; BK:Bank (Amount$)=60000; BL:Nature (Amount$)=-60000
  - row 27: 2509-004 | 2025-09-30 | Bank interest income | Interest |  |  |  |  | 91.07 || I:Deposit=91.07; K:Balance=601100.8399999997; AC:Bank interest income=91.07; BG:Number of Distributions=2; BK:Bank (Amount$)=91.07; BL:Nature (Amount$)=-91.07
  - row 28: 2510-001 | 2025-10-22 | Membership fee income | FPS IN CR | 2025-NGO-70101 | Hong Kong-Shenzhen Innovation and Technology Park Limited |  |  | 835 || I:Deposit=835; K:Balance=601935.8399999997; Z:Membership fee income=835; BG:Number of Distributions=4; BK:Bank (Amount$)=835; BL:Nature (Amount$)=-835
  - row 29: 2510-001 | 2025-10-22 | Receipt in advance | FPS IN CR | 2025-NGO-70101 | Hong Kong-Shenzhen Innovation and Technology Park Limited |  |  | 1165 || I:Deposit=1165; K:Balance=603100.8399999997; W:Receipt in advance=1165; BG:Number of Distributions=4; BK:Bank (Amount$)=1165; BL:Nature (Amount$)=-1165
  - row 30: 2510-002 | 2025-10-31 | Bank interest income | Interest |  |  |  |  | 63.88 || I:Deposit=63.88; K:Balance=603164.7199999997; AC:Bank interest income=63.88; BG:Number of Distributions=2; BK:Bank (Amount$)=63.88; BL:Nature (Amount$)=-63.88
  - row 31: 2511-001 | 2025-11-30 | Bank interest income | Interest |  |  |  |  | 10.66 || I:Deposit=10.66; K:Balance=603175.3799999998; AC:Bank interest income=10.66; BG:Number of Distributions=2; BK:Bank (Amount$)=10.66; BL:Nature (Amount$)=-10.66
  - row 32: 2512-001 | 2025-12-31 | Bank interest income | Interest |  |  |  |  | 5.12 || I:Deposit=5.12; K:Balance=603180.4999999998; AC:Bank interest income=5.12; BG:Number of Distributions=2; BK:Bank (Amount$)=5.12; BL:Nature (Amount$)=-5.12
  - row 33: 2512-005 |  |  |  |  |  |  |  |  || K:Balance=603180.4999999998
  - row 34: 2512-006 |  |  |  |  |  |  |  |  || K:Balance=603180.4999999998
  - row 35: 2512-007 |  |  |  |  |  |  |  |  || K:Balance=603180.4999999998
- Non-zero totals by header label:
  - Balance: 54393375.96999999
  - Bank (Amount$): 106323.16
  - Bank charges: -600.0
  - Bank interest income: 2923.1600000000003
  - Deposit: 206923.16000000003
  - Interbank: -100000.0
  - Membership fee income: 31676.0
  - Nature (Amount$): -106323.16
  - Number of Distributions: 54.0
  - Receipt in advance: 172324.0
  - Withdrawal: -100600.0

## Bank/Cash record sheet: NCB HKD CA

- Company: International Data Industry Alliance Limited
- Period: 1.1.25-31.12.25
- Account label: NCB HKD C/A #043-509-007436-2
- Detected transaction header row: 9
- header row 1: A=Company Name; C=International Data Industry Alliance Limited; G=Remind; H=- "+ve" for income, "-ve" for expenses
- header row 2: A=Period; C=1.1.25-31.12.25; H=- 1 file for each bank account
- header row 3: A=Bank record; C=NCB HKD C/A #043-509-007436-2
- header row 4: A=Bank COA (Peachtree):; C=NCB HKD CA
- header row 5: A=Bank name:; C=NCB HKD CA
- header row 8: BD=For Peachtree import use - Please don't move this column
- header row 9: A=No.; B=Date; C=Particular; I=Deposit; J=Withdrawal; K=Balance; M=Control; O=Interbank; Q=Computer equipment; R=Fixture & furniture; T=Director's C/A; V=Trade receivable; W=Prepayment; X=Accruals; Z=Sales; AA=Purchases; AC=Bank interest income; AE=Director's remuneration; AF=Salaries; AG=Mandatory provident fund; AI=Advertisement; AJ=Bank charges; AK=Computer accessories; AL=Company secretarial fee; AM=Electricity & water; AN=Entertainment; AO=Insurance; AP=Legal and professional fee; AQ=Local travelling; AR=Postage & courier; AS=Printing & stationery; AT=Rental expenses; AU=Staff welfare; AV=Stamp duty; AW=Telecommunication; AX=Web hosting fee; AZ=Temp; BD=Date; BE=Reference; BG=Number of Distributions; BH=G/L Account ; BI=G/L Account ; BJ=Description; BK=Bank (Amount$); BL=Nature (Amount$)
- header row 10: A=No.; B=Date; C=Nature; D=Payer / (Payee); E=Invoice no. (Cheque no.); F=Details; G=Month-Year; BH==C5; BI=(Nature)
- header row 11: A=0; B=2025-01-01; C=Bank opening; K=87621.63
- header row 12: A=2501-001; B=2025-01-03; C=Accruals; D=000773; J=-3000; K==K11+I12+J12; M==SUM(I12:J12)-SUM(N12:BA12); O==IF($C12=O$9,$I12+$J12,0); Q==IF($C12=Q$9,$I12+$J12,0); R==IF($C12=R$9,$I12+$J12,0); T==IF($C12=T$9,$I12+$J12,0); V==IF($C12=V$9,$I12+$J12,0); W==IF($C12=W$9,$I12+$J12,0); X==IF($C12=X$9,$I12+$J12,0); Z==IF($C12=Z$9,$I12+$J12,0); AA==IF($C12=AA$9,$I12+$J12,0); AC==IF($C12=AC$9,$I12+$J12,0); AE==IF($C12=AE$9,$I12+$J12,0); AF==IF($C12=AF$9,$I12+$J12,0); AG==IF($C12=AG$9,$I12+$J12,0); AI==IF($C12=AI$9,$I12+$J12,0); AJ==IF($C12=AJ$9,$I12+$J12,0); AK==IF($C12=AK$9,$I12+$J12,0); AL==IF($C12=AL$9,$I12+$J12,0); AM==IF($C12=AM$9,$I12+$J12,0); AN==IF($C12=AN$9,$I12+$J12,0); AO==IF($C12=AO$9,$I12+$J12,0); AP==IF($C12=AP$9,$I12+$J12,0); AQ==IF($C12=AQ$9,$I12+$J12,0); AR==IF($C12=AR$9,$I12+$J12,0); AS==IF($C12=AS$9,$I12+$J12,0); AT==IF($C12=AT$9,$I12+$J12,0); AU==IF($C12=AU$9,$I12+$J12,0); AV==IF($C12=AV$9,$I12+$J12,0); AW==IF($C12=AW$9,$I12+$J12,0); AX==IF($C12=AX$9,$I12+$J12,0); AZ==IF($C12=AZ$9,$I12+$J12,0); BD==IF(B12="","",B12); BE==IF(C12="","",$C$5&"-"&A12); BG==IF(BE12="","",COUNTIF(BE:BE,BE12)*2); BH==IF(C12="","",IF($C$4="","",VLOOKUP($C$4,'Chart of Accounts'!$A:$B,2,FALSE))); BI==IF(C12="","",VLOOKUP(C:C,'Chart of Accounts'!$A:$B,2,FALSE)); BJ==IF(C12="","",C12&":"&D12&IF(E12="",""," - "&E12)&IF(F12="",""," - "&F12)&IF(G12="",""," - "&TEXT(G12,"MMM-YY"))); BK==SUM(I12:J12); BL==-BK12
- header row 13: A=2502-001; B=2025-02-22; C=Web hosting fee; D=000877; F=WIX.com Website Designing and Hosting Services; J=-2485.86; K==K12+I13+J13; M==SUM(I13:J13)-SUM(N13:BA13); O==IF($C13=O$9,$I13+$J13,0); Q==IF($C13=Q$9,$I13+$J13,0); R==IF($C13=R$9,$I13+$J13,0); T==IF($C13=T$9,$I13+$J13,0); V==IF($C13=V$9,$I13+$J13,0); W==IF($C13=W$9,$I13+$J13,0); X==IF($C13=X$9,$I13+$J13,0); Z==IF($C13=Z$9,$I13+$J13,0); AA==IF($C13=AA$9,$I13+$J13,0); AC==IF($C13=AC$9,$I13+$J13,0); AE==IF($C13=AE$9,$I13+$J13,0); AF==IF($C13=AF$9,$I13+$J13,0); AG==IF($C13=AG$9,$I13+$J13,0); AI==IF($C13=AI$9,$I13+$J13,0); AJ==IF($C13=AJ$9,$I13+$J13,0); AK==IF($C13=AK$9,$I13+$J13,0); AL==IF($C13=AL$9,$I13+$J13,0); AM==IF($C13=AM$9,$I13+$J13,0); AN==IF($C13=AN$9,$I13+$J13,0); AO==IF($C13=AO$9,$I13+$J13,0); AP==IF($C13=AP$9,$I13+$J13,0); AQ==IF($C13=AQ$9,$I13+$J13,0); AR==IF($C13=AR$9,$I13+$J13,0); AS==IF($C13=AS$9,$I13+$J13,0); AT==IF($C13=AT$9,$I13+$J13,0); AU==IF($C13=AU$9,$I13+$J13,0); AV==IF($C13=AV$9,$I13+$J13,0); AW==IF($C13=AW$9,$I13+$J13,0); AX==IF($C13=AX$9,$I13+$J13,0); AZ==IF($C13=AZ$9,$I13+$J13,0); BD==IF(B13="","",B13); BE==IF(C13="","",$C$5&"-"&A13); BG==IF(BE13="","",COUNTIF(BE:BE,BE13)*2); BH==IF(C13="","",IF($C$4="","",VLOOKUP($C$4,'Chart of Accounts'!$A:$B,2,FALSE))); BI==IF(C13="","",VLOOKUP(C:C,'Chart of Accounts'!$A:$B,2,FALSE)); BJ==IF(C13="","",C13&":"&D13&IF(E13="",""," - "&E13)&IF(F13="",""," - "&F13)&IF(G13="",""," - "&TEXT(G13,"MMM-YY"))); BK==SUM(I13:J13)
- header row 14: A=2502-002; B=2025-02-22; C=Legal and professional fee; D=000775; E=Lee & Yu Corporate Services Limited; F=Debit Note C09080-s.88 services; J=-4800; K==K13+I14+J14; M==SUM(I14:J14)-SUM(N14:BA14); O==IF($C14=O$9,$I14+$J14,0); Q==IF($C14=Q$9,$I14+$J14,0); R==IF($C14=R$9,$I14+$J14,0); T==IF($C14=T$9,$I14+$J14,0); V==IF($C14=V$9,$I14+$J14,0); W==IF($C14=W$9,$I14+$J14,0); X==IF($C14=X$9,$I14+$J14,0); Z==IF($C14=Z$9,$I14+$J14,0); AA==IF($C14=AA$9,$I14+$J14,0); AC==IF($C14=AC$9,$I14+$J14,0); AE==IF($C14=AE$9,$I14+$J14,0); AF==IF($C14=AF$9,$I14+$J14,0); AG==IF($C14=AG$9,$I14+$J14,0); AI==IF($C14=AI$9,$I14+$J14,0); AJ==IF($C14=AJ$9,$I14+$J14,0); AK==IF($C14=AK$9,$I14+$J14,0); AL==IF($C14=AL$9,$I14+$J14,0); AM==IF($C14=AM$9,$I14+$J14,0); AN==IF($C14=AN$9,$I14+$J14,0); AO==IF($C14=AO$9,$I14+$J14,0); AP==IF($C14=AP$9,$I14+$J14,0); AQ==IF($C14=AQ$9,$I14+$J14,0); AR==IF($C14=AR$9,$I14+$J14,0); AS==IF($C14=AS$9,$I14+$J14,0); AT==IF($C14=AT$9,$I14+$J14,0); AU==IF($C14=AU$9,$I14+$J14,0); AV==IF($C14=AV$9,$I14+$J14,0); AW==IF($C14=AW$9,$I14+$J14,0); AX==IF($C14=AX$9,$I14+$J14,0); AZ==IF($C14=AZ$9,$I14+$J14,0); BD==IF(B14="","",B14); BE==IF(C14="","",$C$5&"-"&A14); BG==IF(BE14="","",COUNTIF(BE:BE,BE14)*2); BH==IF(C14="","",IF($C$4="","",VLOOKUP($C$4,'Chart of Accounts'!$A:$B,2,FALSE))); BI==IF(C14="","",VLOOKUP(C:C,'Chart of Accounts'!$A:$B,2,FALSE)); BJ==IF(C14="","",C14&":"&D14&IF(E14="",""," - "&E14)&IF(F14="",""," - "&F14)&IF(G14="",""," - "&TEXT(G14,"MMM-YY")))
- header row 15: A=2503-001; B=2025-03-05; C=Web hosting fee; D=000876; E=mCommerce; F=Amazon Web Services; G=2025 January 1 to January 31; J=-4366.6; K==K14+I15+J15; M==SUM(I15:J15)-SUM(N15:BA15); O==IF($C15=O$9,$I15+$J15,0); Q==IF($C15=Q$9,$I15+$J15,0); R==IF($C15=R$9,$I15+$J15,0); T==IF($C15=T$9,$I15+$J15,0); V==IF($C15=V$9,$I15+$J15,0); W==IF($C15=W$9,$I15+$J15,0); X==IF($C15=X$9,$I15+$J15,0); Z==IF($C15=Z$9,$I15+$J15,0); AA==IF($C15=AA$9,$I15+$J15,0); AC==IF($C15=AC$9,$I15+$J15,0); AE==IF($C15=AE$9,$I15+$J15,0); AF==IF($C15=AF$9,$I15+$J15,0); AG==IF($C15=AG$9,$I15+$J15,0); AI==IF($C15=AI$9,$I15+$J15,0); AJ==IF($C15=AJ$9,$I15+$J15,0); AK==IF($C15=AK$9,$I15+$J15,0); AL==IF($C15=AL$9,$I15+$J15,0); AM==IF($C15=AM$9,$I15+$J15,0); AN==IF($C15=AN$9,$I15+$J15,0); AO==IF($C15=AO$9,$I15+$J15,0); AP==IF($C15=AP$9,$I15+$J15,0); AQ==IF($C15=AQ$9,$I15+$J15,0); AR==IF($C15=AR$9,$I15+$J15,0); AS==IF($C15=AS$9,$I15+$J15,0); AT==IF($C15=AT$9,$I15+$J15,0); AU==IF($C15=AU$9,$I15+$J15,0); AV==IF($C15=AV$9,$I15+$J15,0); AW==IF($C15=AW$9,$I15+$J15,0); AX==IF($C15=AX$9,$I15+$J15,0); AZ==IF($C15=AZ$9,$I15+$J15,0); BD==IF(B15="","",B15); BE==IF(C15="","",$C$5&"-"&A15); BG==IF(BE15="","",COUNTIF(BE:BE,BE15)*2); BH==IF(C15="","",IF($C$4="","",VLOOKUP($C$4,'Chart of Accounts'!$A:$B,2,FALSE))); BI==IF(C15="","",VLOOKUP(C:C,'Chart of Accounts'!$A:$B,2,FALSE))
- Header labels:
  A=No.; B=Date; C=Particular; I=Deposit; J=Withdrawal; K=Balance; M=Control; O=Interbank; Q=Computer equipment; R=Fixture & furniture; T=Director's C/A; V=Trade receivable; W=Prepayment; X=Accruals; Z=Sales; AA=Purchases; AC=Bank interest income; AE=Director's remuneration; AF=Salaries; AG=Mandatory provident fund; AI=Advertisement; AJ=Bank charges; AK=Computer accessories; AL=Company secretarial fee; AM=Electricity & water; AN=Entertainment; AO=Insurance; AP=Legal and professional fee; AQ=Local travelling; AR=Postage & courier; AS=Printing & stationery; AT=Rental expenses; AU=Staff welfare; AV=Stamp duty; AW=Telecommunication; AX=Web hosting fee; AZ=Temp; BD=Date; BE=Reference; BG=Number of Distributions; BH=G/L Account ; BI=G/L Account ; BJ=Description; BK=Bank (Amount$); BL=Nature (Amount$)
- Peachtree/helper columns:
  BE=Reference; BG=Number of Distributions; BJ=Description; BK=Bank (Amount$); BL=Nature (Amount$)
- First active rows:
  - row 11: 0 | 2025-01-01 | Bank opening |  |  |  |  |  |  || K:Balance=87621.63
  - row 12: 2501-001 | 2025-01-03 | Accruals | 000773 |  |  |  |  |  || J:Withdrawal=-3000; K:Balance=84621.63; X:Accruals=-3000; BG:Number of Distributions=2; BK:Bank (Amount$)=-3000; BL:Nature (Amount$)=3000
  - row 13: 2502-001 | 2025-02-22 | Web hosting fee | 000877 |  | WIX.com Website Designing and Hosting Services |  |  |  || J:Withdrawal=-2485.86; K:Balance=82135.77; AX:Web hosting fee=-2485.86; BG:Number of Distributions=2; BK:Bank (Amount$)=-2485.86; BL:Nature (Amount$)=2485.86
  - row 14: 2502-002 | 2025-02-22 | Legal and professional fee | 000775 | Lee & Yu Corporate Services Limited | Debit Note C09080-s.88 services |  |  |  || J:Withdrawal=-4800; K:Balance=77335.77; AP:Legal and professional fee=-4800; BG:Number of Distributions=2; BI:G/L Account =6680; BK:Bank (Amount$)=-4800; BL:Nature (Amount$)=4800
  - row 15: 2503-001 | 2025-03-05 | Web hosting fee | 000876 | mCommerce | Amazon Web Services | 2025 January 1 to January 31 |  |  || J:Withdrawal=-4366.6; K:Balance=72969.17; AX:Web hosting fee=-4366.6; BG:Number of Distributions=2; BK:Bank (Amount$)=-4366.6; BL:Nature (Amount$)=4366.6
  - row 16: 2503-002 | 2025-03-05 | Accruals | 000774 |  |  |  |  |  || J:Withdrawal=-4615.41; K:Balance=68353.76; X:Accruals=-4615.41; BG:Number of Distributions=2; BK:Bank (Amount$)=-4615.41; BL:Nature (Amount$)=4615.41
  - row 17: 2503-003 | 2025-03-14 | Accruals | 000880 |  | 2024 Autid and Accounting |  |  |  || J:Withdrawal=-12200; K:Balance=56153.759999999995; X:Accruals=-12200; BG:Number of Distributions=2; BK:Bank (Amount$)=-12200; BL:Nature (Amount$)=12200
  - row 18: 2503-004 | 2025-03-14 | Legal and professional fee | 000878 | Lee & Yu Corporate Services Limited | Debit Note C09092 - trademark registration |  |  |  || J:Withdrawal=-18200; K:Balance=37953.759999999995; AP:Legal and professional fee=-18200; BG:Number of Distributions=2; BI:G/L Account =6680; BK:Bank (Amount$)=-18200; BL:Nature (Amount$)=18200
  - row 19: 2503-005 | 2025-03-15 | Web hosting fee | 000879 | mCommerce | Amazon Web Services | 2025 February 1 to February 28 |  |  || J:Withdrawal=-4604.13; K:Balance=33349.63; AX:Web hosting fee=-4604.13; BG:Number of Distributions=2; BK:Bank (Amount$)=-4604.13; BL:Nature (Amount$)=4604.13
  - row 20: 2503-006 | 2025-03-18 | Web hosting fee | 000882 |  | Website development tools : Slidespeak | USD 359 |  |  || J:Withdrawal=-2800; K:Balance=30549.629999999997; AX:Web hosting fee=-2800; BG:Number of Distributions=2; BK:Bank (Amount$)=-2800; BL:Nature (Amount$)=2800
  - row 21: 2503-007 | 2025-03-18 | Entertainment | 000881 |  | Dinner with Vetting Committee |  |  |  || J:Withdrawal=-7241; K:Balance=23308.629999999997; AN:Entertainment=-7241; BG:Number of Distributions=2; BK:Bank (Amount$)=-7241; BL:Nature (Amount$)=7241
  - row 22: 2506-001 | 2025-06-10 | Web hosting fee | 000883 | WIX.COM | Website fee |  |  |  || J:Withdrawal=-6026; K:Balance=17282.629999999997; AX:Web hosting fee=-6026; BG:Number of Distributions=2; BK:Bank (Amount$)=-6026; BL:Nature (Amount$)=6026
  - row 23: 2506-002 | 2025-06-14 | Temp | 000884 | mCommerce | Amazon Web Services |  |  |  || J:Withdrawal=-18156.65; K:Balance=-874.0200000000041; AZ:Temp=-18156.65; BG:Number of Distributions=2; BK:Bank (Amount$)=-18156.65; BL:Nature (Amount$)=18156.65
  - row 24: 2506-003 | 2025-06-16 | Bank charges | Return cheque |  |  |  |  |  || J:Withdrawal=-150; K:Balance=-1024.020000000004; AJ:Bank charges=-150; BG:Number of Distributions=2; BK:Bank (Amount$)=-150; BL:Nature (Amount$)=150
  - row 25: 2506-004 | 2025-06-16 | Temp | 000884IN-CLEARING RETURN | mCommerce | Amazon Web Services |  |  | 18156.65 || I:Deposit=18156.65; K:Balance=17132.629999999997; AZ:Temp=18156.65; BG:Number of Distributions=2; BK:Bank (Amount$)=18156.65; BL:Nature (Amount$)=-18156.65
  - row 26: 2506-005 | 2025-06-19 | Computer accessories | 000885 | eeio Limited | Microsoft 365 Business Standard annual subscription yearly |  |  |  || J:Withdrawal=-6844.32; K:Balance=10288.309999999998; AK:Computer accessories=-6844.32; BG:Number of Distributions=2; BK:Bank (Amount$)=-6844.32; BL:Nature (Amount$)=6844.32
  - row 27: 2506-006 | 2025-06-20 | Prepayment | 000886 | AC Business Service Limited | Renew Package(Annual Return,Company Secretary) | Service Period: 2025-07-19~2026-07-18 |  |  || J:Withdrawal=-4900; K:Balance=5388.309999999998; W:Prepayment=-4900; BG:Number of Distributions=2; BK:Bank (Amount$)=-4900; BL:Nature (Amount$)=4900
  - row 28: 2506-007 | 2025-06-20 | Interbank | transfer |  |  |  |  | 50000 || I:Deposit=50000; K:Balance=55388.31; O:Interbank=50000; BG:Number of Distributions=2; BK:Bank (Amount$)=50000; BL:Nature (Amount$)=-50000
  - row 29: 2506-008 | 2025-06-24 | Web hosting fee | 000887 | mCommerce | Amazon Web Services |  |  |  || J:Withdrawal=-18156.65; K:Balance=37231.659999999996; AX:Web hosting fee=-18156.65; BG:Number of Distributions=2; BK:Bank (Amount$)=-18156.65; BL:Nature (Amount$)=18156.65
  - row 30: 2508-001 |  |  |  |  |  |  |  |  || K:Balance=37231.659999999996
  - row 31: 2506-010 |  |  |  |  |  |  |  |  || K:Balance=37231.659999999996
  - row 32: 2506-011 |  |  |  |  |  |  |  |  || K:Balance=37231.659999999996
  - row 33: 2506-012 |  |  |  |  |  |  |  |  || K:Balance=37231.659999999996
  - row 34: 2506-013 |  |  |  |  |  |  |  |  || K:Balance=37231.659999999996
  - row 35: 2506-014 |  |  |  |  |  |  |  |  || K:Balance=37231.659999999996
- Non-zero totals by header label:
  - Accruals: -39630.82
  - Balance: 3513078.1300000036
  - Bank (Amount$): -100779.94000000002
  - Bank charges: -300.0
  - Computer accessories: -13688.64
  - Deposit: 136313.3
  - Entertainment: -14482.0
  - G/L Account : 13360.0
  - Interbank: 100000.0
  - Legal and professional fee: -46000.0
  - Nature (Amount$): 100779.94000000002
  - Number of Distributions: 36.0
  - Prepayment: -9800.0
  - Web hosting fee: -76878.48000000001
  - Withdrawal: -237093.24

## Bank/Cash record sheet: HSBC USD SA

- Company: ABC Ltd
- Period: 1.1.25-31.12.25
- Account label: HSBC USD S/A #123-456789-001
- Detected transaction header row: 9
- header row 1: A=Company Name; C=ABC Ltd; J=Remind; K=- "+ve" for income, "-ve" for expenses
- header row 2: A=Period; C=1.1.25-31.12.25; K=- 1 file for each bank account
- header row 3: A=Bank record; C=HSBC USD S/A #123-456789-001
- header row 4: A=Bank COA:; C=HSBC USD SA
- header row 5: A=Bank name:; C=HSBC USD SA
- header row 8: M=Ex-rate; N=7.8; BH=For Peachtree import use - Please don't move this column
- header row 9: A=No.; B=Date; C=Particular; I=Deposit; J=Withdrawal; K=Balance; M=Deposit; N=Withdrawal; O=Balance; Q=Control; S=Interbank; U=Computer equipment; V=Fixture & furniture; X=Director's C/A; Z=Trade receivable; AA=Trade payable; AB=Accruals; AD=Sales; AE=Purchases; AG=Bank interest income; AI=Director's remuneration; AJ=Salaries; AK=Mandatory provident fund; AM=Advertisement; AN=Bank charges; AO=Business registration fee; AP=Company secretary fee; AQ=Electricity & water; AR=Entertainment; AS=Insurance; AT=Legal and professional fee; AU=Local travelling; AV=Postage & courier; AW=Printing & stationery; AX=Rental expenses; AY=Staff welfare; AZ=Stamp duty; BA=Telecommunication; BB=Transportation; BD=Temp; BH=Date; BI=Reference; BK=Number of Distributions; BL=G/L Account ; BM=G/L Account 
- header row 10: A=No.; B=Date; C=Nature; D=Payer / (Payee); E=Invoice no. (Cheque no.); F=Details; G=Month-Year; I=USD; J=USD; K=USD; M=HKD; N=HKD; O=HKD; BL==C4; BM=(Nature)
- header row 11: A=0; B=2025-01-01; C=Bank opening; K=10; O==ROUND(K11*$N$8,2)
- header row 12: A=2501-001; B=2025-01-01; C=Sales; D=Sale invoce #12345; E=ABC customer; G=2025-01-01; I=1000; K==K11+I12+J12; M==ROUND(I12*$N$8,2); N==ROUND(J12*$N$8,2); O==O11+M12+N12; Q==SUM(M12:N12)-SUM(R12:BE12); S==IF($C12=S$9,$M12+$N12,0); U==IF($C12=U$9,$M12+$N12,0); V==IF($C12=V$9,$M12+$N12,0); X==IF($C12=X$9,$M12+$N12,0); Z==IF($C12=Z$9,$M12+$N12,0); AA==IF($C12=AA$9,$M12+$N12,0); AB==IF($C12=AB$9,$M12+$N12,0); AD==IF($C12=AD$9,$M12+$N12,0); AE==IF($C12=AE$9,$M12+$N12,0); AG==IF($C12=AG$9,$M12+$N12,0); AI==IF($C12=AI$9,$M12+$N12,0); AJ==IF($C12=AJ$9,$M12+$N12,0); AK==IF($C12=AK$9,$M12+$N12,0); AM==IF($C12=AM$9,$M12+$N12,0); AN==IF($C12=AN$9,$M12+$N12,0); AO==IF($C12=AO$9,$M12+$N12,0); AP==IF($C12=AP$9,$M12+$N12,0); AQ==IF($C12=AQ$9,$M12+$N12,0); AR==IF($C12=AR$9,$M12+$N12,0); AS==IF($C12=AS$9,$M12+$N12,0); AT==IF($C12=AT$9,$M12+$N12,0); AU==IF($C12=AU$9,$M12+$N12,0); AV==IF($C12=AV$9,$M12+$N12,0); AW==IF($C12=AW$9,$M12+$N12,0); AX==IF($C12=AX$9,$M12+$N12,0); AY==IF($C12=AY$9,$M12+$N12,0); AZ==IF($C12=AZ$9,$M12+$N12,0); BA==IF($C12=BA$9,$M12+$N12,0); BB==IF($C12=BB$9,$M12+$N12,0); BD==IF($C12=BD$9,$M12+$N12,0); BH==IF(B12="","",B12); BI==IF(C12="","",$C$5&"-"&A12); BK==IF(BI12="","",COUNTIF(BI:BI,BI12)*2)
- header row 13: A=2501-002; B=2025-01-01; C=Bank charges; D=Bank chg; J=-500; K==K12+I13+J13; M==ROUND(I13*$N$8,2); N==ROUND(J13*$N$8,2); O==O12+M13+N13; Q==SUM(M13:N13)-SUM(R13:BE13); S==IF($C13=S$9,$M13+$N13,0); U==IF($C13=U$9,$M13+$N13,0); V==IF($C13=V$9,$M13+$N13,0); X==IF($C13=X$9,$M13+$N13,0); Z==IF($C13=Z$9,$M13+$N13,0); AA==IF($C13=AA$9,$M13+$N13,0); AB==IF($C13=AB$9,$M13+$N13,0); AD==IF($C13=AD$9,$M13+$N13,0); AE==IF($C13=AE$9,$M13+$N13,0); AG==IF($C13=AG$9,$M13+$N13,0); AI==IF($C13=AI$9,$M13+$N13,0); AJ==IF($C13=AJ$9,$M13+$N13,0); AK==IF($C13=AK$9,$M13+$N13,0); AM==IF($C13=AM$9,$M13+$N13,0); AN==IF($C13=AN$9,$M13+$N13,0); AO==IF($C13=AO$9,$M13+$N13,0); AP==IF($C13=AP$9,$M13+$N13,0); AQ==IF($C13=AQ$9,$M13+$N13,0); AR==IF($C13=AR$9,$M13+$N13,0); AS==IF($C13=AS$9,$M13+$N13,0); AT==IF($C13=AT$9,$M13+$N13,0); AU==IF($C13=AU$9,$M13+$N13,0); AV==IF($C13=AV$9,$M13+$N13,0); AW==IF($C13=AW$9,$M13+$N13,0); AX==IF($C13=AX$9,$M13+$N13,0); AY==IF($C13=AY$9,$M13+$N13,0); AZ==IF($C13=AZ$9,$M13+$N13,0); BA==IF($C13=BA$9,$M13+$N13,0); BB==IF($C13=BB$9,$M13+$N13,0); BD==IF($C13=BD$9,$M13+$N13,0); BH==IF(B13="","",B13); BI==IF(C13="","",$C$5&"-"&A13); BK==IF(BI13="","",COUNTIF(BI:BI,BI13)*2); BL==IF(C13="","",IF($C$4="","",VLOOKUP($C$4,'Chart of Accounts'!$A:$B,2,FALSE))); BM==IF(C13="","",VLOOKUP(C:C,'Chart of Accounts'!$A:$B,2,FALSE))
- header row 14: A=2501-003; K==K13+I14+J14; M==ROUND(I14*$N$8,2); N==ROUND(J14*$N$8,2); O==O13+M14+N14; Q==SUM(M14:N14)-SUM(R14:BE14); S==IF($C14=S$9,$M14+$N14,0); U==IF($C14=U$9,$M14+$N14,0); V==IF($C14=V$9,$M14+$N14,0); X==IF($C14=X$9,$M14+$N14,0); Z==IF($C14=Z$9,$M14+$N14,0); AA==IF($C14=AA$9,$M14+$N14,0); AB==IF($C14=AB$9,$M14+$N14,0); AD==IF($C14=AD$9,$M14+$N14,0); AE==IF($C14=AE$9,$M14+$N14,0); AG==IF($C14=AG$9,$M14+$N14,0); AI==IF($C14=AI$9,$M14+$N14,0); AJ==IF($C14=AJ$9,$M14+$N14,0); AK==IF($C14=AK$9,$M14+$N14,0); AM==IF($C14=AM$9,$M14+$N14,0); AN==IF($C14=AN$9,$M14+$N14,0); AO==IF($C14=AO$9,$M14+$N14,0); AP==IF($C14=AP$9,$M14+$N14,0); AQ==IF($C14=AQ$9,$M14+$N14,0); AR==IF($C14=AR$9,$M14+$N14,0); AS==IF($C14=AS$9,$M14+$N14,0); AT==IF($C14=AT$9,$M14+$N14,0); AU==IF($C14=AU$9,$M14+$N14,0); AV==IF($C14=AV$9,$M14+$N14,0); AW==IF($C14=AW$9,$M14+$N14,0); AX==IF($C14=AX$9,$M14+$N14,0); AY==IF($C14=AY$9,$M14+$N14,0); AZ==IF($C14=AZ$9,$M14+$N14,0); BA==IF($C14=BA$9,$M14+$N14,0); BB==IF($C14=BB$9,$M14+$N14,0); BD==IF($C14=BD$9,$M14+$N14,0); BH==IF(B14="","",B14); BI==IF(C14="","",$C$5&"-"&A14); BK==IF(BI14="","",COUNTIF(BI:BI,BI14)*2); BL==IF(C14="","",IF($C$4="","",VLOOKUP($C$4,'Chart of Accounts'!$A:$B,2,FALSE))); BM==IF(C14="","",VLOOKUP(C:C,'Chart of Accounts'!$A:$B,2,FALSE)); BN==IF(C14="","",D14&":"&E14&IF(E14="",""," - "&E14)&IF(F14="",""," - "&F14)&IF(G14="",""," - "&TEXT(G14,"MMM-YY"))); BO==SUM(M14:N14); BP==-BO14
- header row 15: A=2501-004; K==K14+I15+J15; M==ROUND(I15*$N$8,2); N==ROUND(J15*$N$8,2); O==O14+M15+N15; Q==SUM(M15:N15)-SUM(R15:BE15); S==IF($C15=S$9,$M15+$N15,0); U==IF($C15=U$9,$M15+$N15,0); V==IF($C15=V$9,$M15+$N15,0); X==IF($C15=X$9,$M15+$N15,0); Z==IF($C15=Z$9,$M15+$N15,0); AA==IF($C15=AA$9,$M15+$N15,0); AB==IF($C15=AB$9,$M15+$N15,0); AD==IF($C15=AD$9,$M15+$N15,0); AE==IF($C15=AE$9,$M15+$N15,0); AG==IF($C15=AG$9,$M15+$N15,0); AI==IF($C15=AI$9,$M15+$N15,0); AJ==IF($C15=AJ$9,$M15+$N15,0); AK==IF($C15=AK$9,$M15+$N15,0); AM==IF($C15=AM$9,$M15+$N15,0); AN==IF($C15=AN$9,$M15+$N15,0); AO==IF($C15=AO$9,$M15+$N15,0); AP==IF($C15=AP$9,$M15+$N15,0); AQ==IF($C15=AQ$9,$M15+$N15,0); AR==IF($C15=AR$9,$M15+$N15,0); AS==IF($C15=AS$9,$M15+$N15,0); AT==IF($C15=AT$9,$M15+$N15,0); AU==IF($C15=AU$9,$M15+$N15,0); AV==IF($C15=AV$9,$M15+$N15,0); AW==IF($C15=AW$9,$M15+$N15,0); AX==IF($C15=AX$9,$M15+$N15,0); AY==IF($C15=AY$9,$M15+$N15,0); AZ==IF($C15=AZ$9,$M15+$N15,0); BA==IF($C15=BA$9,$M15+$N15,0); BB==IF($C15=BB$9,$M15+$N15,0); BD==IF($C15=BD$9,$M15+$N15,0); BH==IF(B15="","",B15); BI==IF(C15="","",$C$5&"-"&A15); BK==IF(BI15="","",COUNTIF(BI:BI,BI15)*2); BL==IF(C15="","",IF($C$4="","",VLOOKUP($C$4,'Chart of Accounts'!$A:$B,2,FALSE))); BM==IF(C15="","",VLOOKUP(C:C,'Chart of Accounts'!$A:$B,2,FALSE)); BN==IF(C15="","",D15&":"&E15&IF(E15="",""," - "&E15)&IF(F15="",""," - "&F15)&IF(G15="",""," - "&TEXT(G15,"MMM-YY"))); BO==SUM(M15:N15); BP==-BO15
- Header labels:
  A=No.; B=Date; C=Particular; I=Deposit; J=Withdrawal; K=Balance; M=Deposit; N=Withdrawal; O=Balance; Q=Control; S=Interbank; U=Computer equipment; V=Fixture & furniture; X=Director's C/A; Z=Trade receivable; AA=Trade payable; AB=Accruals; AD=Sales; AE=Purchases; AG=Bank interest income; AI=Director's remuneration; AJ=Salaries; AK=Mandatory provident fund; AM=Advertisement; AN=Bank charges; AO=Business registration fee; AP=Company secretary fee; AQ=Electricity & water; AR=Entertainment; AS=Insurance; AT=Legal and professional fee; AU=Local travelling; AV=Postage & courier; AW=Printing & stationery; AX=Rental expenses; AY=Staff welfare; AZ=Stamp duty; BA=Telecommunication; BB=Transportation; BD=Temp; BH=Date; BI=Reference; BK=Number of Distributions; BL=G/L Account ; BM=G/L Account ; BN=Description; BO=Bank (Amount$); BP=Nature (Amount$)
- Peachtree/helper columns:
  BI=Reference; BK=Number of Distributions; BN=Description; BO=Bank (Amount$); BP=Nature (Amount$)
- First active rows:
  - row 11: 0 | 2025-01-01 | Bank opening |  |  |  |  |  |  || K:Balance=10; O:Balance=78
  - row 12: 2501-001 | 2025-01-01 | Sales | Sale invoce #12345 | ABC customer |  | 2025-01-01 |  | 1000 || I:Deposit=1000; K:Balance=1010; M:Deposit=7800; O:Balance=7878; AD:Sales=7800; BK:Number of Distributions=2; BO:Bank (Amount$)=7800; BP:Nature (Amount$)=-7800
  - row 13: 2501-002 | 2025-01-01 | Bank charges | Bank chg |  |  |  |  |  || J:Withdrawal=-500; K:Balance=510; N:Withdrawal=-3900; O:Balance=3978; AN:Bank charges=-3900; BK:Number of Distributions=2; BO:Bank (Amount$)=-3900; BP:Nature (Amount$)=3900
  - row 14: 2501-003 |  |  |  |  |  |  |  |  || K:Balance=510; O:Balance=3978
  - row 15: 2501-004 |  |  |  |  |  |  |  |  || K:Balance=510; O:Balance=3978
  - row 16: 2501-005 |  |  |  |  |  |  |  |  || K:Balance=510; O:Balance=3978
  - row 17: 2501-006 |  |  |  |  |  |  |  |  || K:Balance=510; O:Balance=3978
  - row 18: 2501-007 |  |  |  |  |  |  |  |  || K:Balance=510; O:Balance=3978
  - row 19: 2501-008 |  |  |  |  |  |  |  |  || K:Balance=510; O:Balance=3978
  - row 20: 2501-009 |  |  |  |  |  |  |  |  || K:Balance=510; O:Balance=3978
  - row 21: 2501-010 |  |  |  |  |  |  |  |  || K:Balance=510; O:Balance=3978
  - row 22: 2501-011 |  |  |  |  |  |  |  |  || K:Balance=510; O:Balance=3978
  - row 23: 2501-012 |  |  |  |  |  |  |  |  || K:Balance=510; O:Balance=3978
  - row 24: 2501-013 |  |  |  |  |  |  |  |  || K:Balance=510; O:Balance=3978
  - row 25: 2501-014 |  |  |  |  |  |  |  |  || K:Balance=510; O:Balance=3978
  - row 26: 2501-015 |  |  |  |  |  |  |  |  || K:Balance=510; O:Balance=3978
  - row 27: 2501-016 |  |  |  |  |  |  |  |  || K:Balance=510; O:Balance=3978
  - row 28: 2502-001 |  |  |  |  |  |  |  |  || K:Balance=510; O:Balance=3978
  - row 29: 2502-002 |  |  |  |  |  |  |  |  || K:Balance=510; O:Balance=3978
  - row 30: 2502-003 |  |  |  |  |  |  |  |  || K:Balance=510; O:Balance=3978
  - row 31: 2502-004 |  |  |  |  |  |  |  |  || K:Balance=510; O:Balance=3978
  - row 32: 2502-005 |  |  |  |  |  |  |  |  || K:Balance=510; O:Balance=3978
  - row 33: 2502-006 |  |  |  |  |  |  |  |  || K:Balance=510; O:Balance=3978
  - row 34: 2502-007 |  |  |  |  |  |  |  |  || K:Balance=510; O:Balance=3978
  - row 35: 2502-008 |  |  |  |  |  |  |  |  || K:Balance=510; O:Balance=3978
- Non-zero totals by header label:
  - Balance: 412896.0
  - Bank (Amount$): 7800.0
  - Bank charges: -7800.0
  - Deposit: 17600.0
  - Nature (Amount$): -7800.0
  - Number of Distributions: 4.0
  - Sales: 15600.0
  - Withdrawal: -8800.0

## Bank/Cash record sheet: Finance costs

- Company: ABC Ltd
- Period: 1.1.25-31.12.25
- Account label: Obligation under Finance Lease
- Detected transaction header row: 9
- header row 1: A=Company Name; C=ABC Ltd; G=Remind; H=- "+ve" for income, "-ve" for expenses
- header row 2: A=Period; C=1.1.25-31.12.25; H=- 1 file for each bank account
- header row 3: A=Interest on finance leases; C=Obligation under Finance Lease
- header row 4: A=Bank COA (Peachtree):; C=Obligation under Finance Lease
- header row 5: A=Bank name:; C=Obligation under Finance Lease
- header row 8: BD=For Peachtree import use - Please don't move this column
- header row 9: A=No.; B=Date; C=Particular; I=Deposit; J=Withdrawal; K=Balance; M=Control; O=Interbank; Q=Computer equipment; R=Fixture & furniture; T=Director's C/A; V=Trade receivable; W=Trade payable; X=Accruals; Z=Sales; AA=Purchases; AC=Bank interest income; AE=Director's remuneration; AF=Salaries; AG=Mandatory provident fund; AI=Advertisement; AJ=Bank charges; AK=Business registration fee; AL=Company secretary fee; AM=Electricity & water; AN=Entertainment; AO=Insurance; AP=Legal and professional fee; AQ=Local travelling; AR=Postage & courier; AS=Printing & stationery; AT=Rental expenses; AU=Staff welfare; AV=Stamp duty; AW=Telecommunication; AX=Transportation; AZ=Temp; BD=Date; BE=Reference; BG=Number of Distributions; BH=G/L Account ; BI=G/L Account ; BJ=Description; BK==BH10; BL==BI10
- header row 10: A=No.; B=Date; C=Nature; D=Payer / (Payee); E=Invoice no. (Cheque no.); F=Details; G=Month-Year; BH==C5; BI=(Nature); BK=(Amount$); BL=(Amount$)
- header row 11: A=0; B=2025-01-01; C=Bank opening; K=10000
- header row 12: A=2501-001; B=2025-01-01; C=Interest on finance lease; J=-100; K==K11+I12+J12; M==SUM(I12:J12)-SUM(N12:BA12); O==IF($C12=O$9,$I12+$J12,0); Q==IF($C12=Q$9,$I12+$J12,0); R==IF($C12=R$9,$I12+$J12,0); T==IF($C12=T$9,$I12+$J12,0); V==IF($C12=V$9,$I12+$J12,0); W==IF($C12=W$9,$I12+$J12,0); X==IF($C12=X$9,$I12+$J12,0); Z==IF($C12=Z$9,$I12+$J12,0); AA==IF($C12=AA$9,$I12+$J12,0); AC==IF($C12=AC$9,$I12+$J12,0); AE==IF($C12=AE$9,$I12+$J12,0); AF==IF($C12=AF$9,$I12+$J12,0); AG==IF($C12=AG$9,$I12+$J12,0); AI==IF($C12=AI$9,$I12+$J12,0); AJ==IF($C12=AJ$9,$I12+$J12,0); AK==IF($C12=AK$9,$I12+$J12,0); AL==IF($C12=AL$9,$I12+$J12,0); AM==IF($C12=AM$9,$I12+$J12,0); AN==IF($C12=AN$9,$I12+$J12,0); AO==IF($C12=AO$9,$I12+$J12,0); AP==IF($C12=AP$9,$I12+$J12,0); AQ==IF($C12=AQ$9,$I12+$J12,0); AR==IF($C12=AR$9,$I12+$J12,0); AS==IF($C12=AS$9,$I12+$J12,0); AT==IF($C12=AT$9,$I12+$J12,0); AU==IF($C12=AU$9,$I12+$J12,0); AV==IF($C12=AV$9,$I12+$J12,0); AW==IF($C12=AW$9,$I12+$J12,0); AX==IF($C12=AX$9,$I12+$J12,0); AZ==IF($C12=AZ$9,$I12+$J12,0); BD==IF(B12="","",B12); BE==IF(C12="","",$C$5&"-"&A12); BG==IF(BE12="","",COUNTIF(BE:BE,BE12)*2); BH==IF(C12="","",IF($C$4="","",VLOOKUP($C$4,'Chart of Accounts'!$A:$B,2,FALSE))); BI==IF(C12="","",VLOOKUP(C:C,'Chart of Accounts'!$A:$B,2,FALSE)); BJ==IF(C12="","",C12&":"&D12&IF(E12="",""," - "&E12)&IF(F12="",""," - "&F12)&IF(G12="",""," - "&TEXT(G12,"MMM-YY"))); BK==SUM(I12:J12); BL==-BK12
- header row 13: A=2501-002; B=2025-01-01; K==K12+I13+J13; M==SUM(I13:J13)-SUM(N13:BA13); O==IF($C13=O$9,$I13+$J13,0); Q==IF($C13=Q$9,$I13+$J13,0); R==IF($C13=R$9,$I13+$J13,0); T==IF($C13=T$9,$I13+$J13,0); V==IF($C13=V$9,$I13+$J13,0); W==IF($C13=W$9,$I13+$J13,0); X==IF($C13=X$9,$I13+$J13,0); Z==IF($C13=Z$9,$I13+$J13,0); AA==IF($C13=AA$9,$I13+$J13,0); AC==IF($C13=AC$9,$I13+$J13,0); AE==IF($C13=AE$9,$I13+$J13,0); AF==IF($C13=AF$9,$I13+$J13,0); AG==IF($C13=AG$9,$I13+$J13,0); AI==IF($C13=AI$9,$I13+$J13,0); AJ==IF($C13=AJ$9,$I13+$J13,0); AK==IF($C13=AK$9,$I13+$J13,0); AL==IF($C13=AL$9,$I13+$J13,0); AM==IF($C13=AM$9,$I13+$J13,0); AN==IF($C13=AN$9,$I13+$J13,0); AO==IF($C13=AO$9,$I13+$J13,0); AP==IF($C13=AP$9,$I13+$J13,0); AQ==IF($C13=AQ$9,$I13+$J13,0); AR==IF($C13=AR$9,$I13+$J13,0); AS==IF($C13=AS$9,$I13+$J13,0); AT==IF($C13=AT$9,$I13+$J13,0); AU==IF($C13=AU$9,$I13+$J13,0); AV==IF($C13=AV$9,$I13+$J13,0); AW==IF($C13=AW$9,$I13+$J13,0); AX==IF($C13=AX$9,$I13+$J13,0); AZ==IF($C13=AZ$9,$I13+$J13,0); BD==IF(B13="","",B13); BE==IF(C13="","",$C$5&"-"&A13); BG==IF(BE13="","",COUNTIF(BE:BE,BE13)*2); BH==IF(C13="","",IF($C$4="","",VLOOKUP($C$4,'Chart of Accounts'!$A:$B,2,FALSE))); BI==IF(C13="","",VLOOKUP(C:C,'Chart of Accounts'!$A:$B,2,FALSE)); BJ==IF(C13="","",C13&":"&D13&IF(E13="",""," - "&E13)&IF(F13="",""," - "&F13)&IF(G13="",""," - "&TEXT(G13,"MMM-YY"))); BK==SUM(I13:J13); BL==-BK13
- header row 14: A=2501-003; K==K13+I14+J14; M==SUM(I14:J14)-SUM(N14:BA14); O==IF($C14=O$9,$I14+$J14,0); Q==IF($C14=Q$9,$I14+$J14,0); R==IF($C14=R$9,$I14+$J14,0); T==IF($C14=T$9,$I14+$J14,0); V==IF($C14=V$9,$I14+$J14,0); W==IF($C14=W$9,$I14+$J14,0); X==IF($C14=X$9,$I14+$J14,0); Z==IF($C14=Z$9,$I14+$J14,0); AA==IF($C14=AA$9,$I14+$J14,0); AC==IF($C14=AC$9,$I14+$J14,0); AE==IF($C14=AE$9,$I14+$J14,0); AF==IF($C14=AF$9,$I14+$J14,0); AG==IF($C14=AG$9,$I14+$J14,0); AI==IF($C14=AI$9,$I14+$J14,0); AJ==IF($C14=AJ$9,$I14+$J14,0); AK==IF($C14=AK$9,$I14+$J14,0); AL==IF($C14=AL$9,$I14+$J14,0); AM==IF($C14=AM$9,$I14+$J14,0); AN==IF($C14=AN$9,$I14+$J14,0); AO==IF($C14=AO$9,$I14+$J14,0); AP==IF($C14=AP$9,$I14+$J14,0); AQ==IF($C14=AQ$9,$I14+$J14,0); AR==IF($C14=AR$9,$I14+$J14,0); AS==IF($C14=AS$9,$I14+$J14,0); AT==IF($C14=AT$9,$I14+$J14,0); AU==IF($C14=AU$9,$I14+$J14,0); AV==IF($C14=AV$9,$I14+$J14,0); AW==IF($C14=AW$9,$I14+$J14,0); AX==IF($C14=AX$9,$I14+$J14,0); AZ==IF($C14=AZ$9,$I14+$J14,0); BD==IF(B14="","",B14); BE==IF(C14="","",$C$5&"-"&A14); BG==IF(BE14="","",COUNTIF(BE:BE,BE14)*2); BH==IF(C14="","",IF($C$4="","",VLOOKUP($C$4,'Chart of Accounts'!$A:$B,2,FALSE))); BI==IF(C14="","",VLOOKUP(C:C,'Chart of Accounts'!$A:$B,2,FALSE)); BJ==IF(C14="","",C14&":"&D14&IF(E14="",""," - "&E14)&IF(F14="",""," - "&F14)&IF(G14="",""," - "&TEXT(G14,"MMM-YY"))); BK==SUM(I14:J14); BL==-BK14
- header row 15: A=2501-004; K==K14+I15+J15; M==SUM(I15:J15)-SUM(N15:BA15); O==IF($C15=O$9,$I15+$J15,0); Q==IF($C15=Q$9,$I15+$J15,0); R==IF($C15=R$9,$I15+$J15,0); T==IF($C15=T$9,$I15+$J15,0); V==IF($C15=V$9,$I15+$J15,0); W==IF($C15=W$9,$I15+$J15,0); X==IF($C15=X$9,$I15+$J15,0); Z==IF($C15=Z$9,$I15+$J15,0); AA==IF($C15=AA$9,$I15+$J15,0); AC==IF($C15=AC$9,$I15+$J15,0); AE==IF($C15=AE$9,$I15+$J15,0); AF==IF($C15=AF$9,$I15+$J15,0); AG==IF($C15=AG$9,$I15+$J15,0); AI==IF($C15=AI$9,$I15+$J15,0); AJ==IF($C15=AJ$9,$I15+$J15,0); AK==IF($C15=AK$9,$I15+$J15,0); AL==IF($C15=AL$9,$I15+$J15,0); AM==IF($C15=AM$9,$I15+$J15,0); AN==IF($C15=AN$9,$I15+$J15,0); AO==IF($C15=AO$9,$I15+$J15,0); AP==IF($C15=AP$9,$I15+$J15,0); AQ==IF($C15=AQ$9,$I15+$J15,0); AR==IF($C15=AR$9,$I15+$J15,0); AS==IF($C15=AS$9,$I15+$J15,0); AT==IF($C15=AT$9,$I15+$J15,0); AU==IF($C15=AU$9,$I15+$J15,0); AV==IF($C15=AV$9,$I15+$J15,0); AW==IF($C15=AW$9,$I15+$J15,0); AX==IF($C15=AX$9,$I15+$J15,0); AZ==IF($C15=AZ$9,$I15+$J15,0); BD==IF(B15="","",B15); BE==IF(C15="","",$C$5&"-"&A15); BG==IF(BE15="","",COUNTIF(BE:BE,BE15)*2); BH==IF(C15="","",IF($C$4="","",VLOOKUP($C$4,'Chart of Accounts'!$A:$B,2,FALSE))); BI==IF(C15="","",VLOOKUP(C:C,'Chart of Accounts'!$A:$B,2,FALSE)); BJ==IF(C15="","",C15&":"&D15&IF(E15="",""," - "&E15)&IF(F15="",""," - "&F15)&IF(G15="",""," - "&TEXT(G15,"MMM-YY"))); BK==SUM(I15:J15); BL==-BK15
- Header labels:
  A=No.; B=Date; C=Particular; I=Deposit; J=Withdrawal; K=Balance; M=Control; O=Interbank; Q=Computer equipment; R=Fixture & furniture; T=Director's C/A; V=Trade receivable; W=Trade payable; X=Accruals; Z=Sales; AA=Purchases; AC=Bank interest income; AE=Director's remuneration; AF=Salaries; AG=Mandatory provident fund; AI=Advertisement; AJ=Bank charges; AK=Business registration fee; AL=Company secretary fee; AM=Electricity & water; AN=Entertainment; AO=Insurance; AP=Legal and professional fee; AQ=Local travelling; AR=Postage & courier; AS=Printing & stationery; AT=Rental expenses; AU=Staff welfare; AV=Stamp duty; AW=Telecommunication; AX=Transportation; AZ=Temp; BD=Date; BE=Reference; BG=Number of Distributions; BH=G/L Account ; BI=G/L Account ; BJ=Description; BK==BH10; BL==BI10
- Peachtree/helper columns:
  BE=Reference; BG=Number of Distributions; BJ=Description
- First active rows:
  - row 11: 0 | 2025-01-01 | Bank opening |  |  |  |  |  |  || K:Balance=10000
  - row 12: 2501-001 | 2025-01-01 | Interest on finance lease |  |  |  |  |  |  || J:Withdrawal=-100; K:Balance=9900; M:Control=-100; BG:Number of Distributions=2; BK:=BH10=-100; BL:=BI10=100
  - row 13: 2501-002 | 2025-01-01 |  |  |  |  |  |  |  || K:Balance=9900
  - row 14: 2501-003 |  |  |  |  |  |  |  |  || K:Balance=9900
  - row 15: 2501-004 |  |  |  |  |  |  |  |  || K:Balance=9900
  - row 16: 2501-005 |  |  |  |  |  |  |  |  || K:Balance=9900
  - row 17: 2501-006 |  |  |  |  |  |  |  |  || K:Balance=9900
  - row 18: 2501-007 |  |  |  |  |  |  |  |  || K:Balance=9900
  - row 19: 2501-008 |  |  |  |  |  |  |  |  || K:Balance=9900
  - row 20: 2501-009 |  |  |  |  |  |  |  |  || K:Balance=9900
  - row 21: 2501-010 |  |  |  |  |  |  |  |  || K:Balance=9900
  - row 22: 2501-011 |  |  |  |  |  |  |  |  || K:Balance=9900
  - row 23: 2501-012 |  |  |  |  |  |  |  |  || K:Balance=9900
  - row 24: 2502-001 |  |  |  |  |  |  |  |  || K:Balance=9900
  - row 25: 2502-002 |  |  |  |  |  |  |  |  || K:Balance=9900
  - row 26: 2502-003 |  |  |  |  |  |  |  |  || K:Balance=9900
  - row 27: 2502-004 |  |  |  |  |  |  |  |  || K:Balance=9900
  - row 28: 2502-005 |  |  |  |  |  |  |  |  || K:Balance=9900
  - row 29: 2502-006 |  |  |  |  |  |  |  |  || K:Balance=9900
  - row 30: 2502-007 |  |  |  |  |  |  |  |  || K:Balance=9900
  - row 31: 2502-008 |  |  |  |  |  |  |  |  || K:Balance=9900
  - row 32: 2502-009 |  |  |  |  |  |  |  |  || K:Balance=9900
  - row 33: 2502-010 |  |  |  |  |  |  |  |  || K:Balance=9900
  - row 34: 2502-011 |  |  |  |  |  |  |  |  || K:Balance=9900
  - row 35: 2502-012 |  |  |  |  |  |  |  |  || K:Balance=9900
- Non-zero totals by header label:
  - =BH10: -200.0
  - =BI10: 200.0
  - Balance: 910900.0
  - Control: -200.0
  - Number of Distributions: 2.0
  - Withdrawal: -200.0

## Bank/Cash record sheet: Chart of Accounts

- Company: 
- Period: 
- Account label: 
- Detected transaction header row: None
- header row 1: A=Account Description; B=Account ID
- header row 2: A=Cash; B=1000
- header row 3: A=NCB HKD CA; B=1010
- header row 4: A=NCB HKD SA; B=1020
- header row 5: A=BOC HKD CA; B=1030
- header row 6: A=BOC HKD SA; B=1040
- header row 7: A=HSBC HKD Credit Card; B=1080
- header row 8: A=Interbank; B=1090
- header row 9: A=Temp; B=1099
- header row 10: A=Trade receivable; B=1100
- header row 11: A=Other receivables; B=1120
- header row 12: A=Trade deposit paid; B=1150
- header row 13: A=Rental &  utilities deposit; B=1200
- header row 14: A=Prepayment; B=1300
- header row 15: A=Inventory; B=1400

## Report sheet: TB 31.12.25

- row 1: Account ID | Account Description | Debit Amt | Credit Amt
- row 2: 1010 | NCB HKD CA | 37231.66
- row 3: 1020 | NCB HKD SA | 603180.5
- row 4: 1100 | Trade receivable | 64000
- row 5: 1300 | Prepayment | 4900
- row 6: 1800 | Office equipment | 5750
- row 7: 1850 | Accum Depreciation-OE | -5750
- row 8: 2100 | Receipt in advance | -123310
- row 9: 2200 | Accruals | -12200
- row 10: 3910 | Retained Earnings | -549241.14
- row 11: 4000 | Membership fee income | -116174
- row 12: 4100 | Bank interest income | -1461.58
- row 13: 6000 | Accounting fee | 5000
- row 14: 6100 | Auditor's remuneration | 7200
- row 15: 6200 | Bank charges | 450
- row 16: 6330 | Company secretarial fee | 4900
- row 17: 6350 | Computer accessories | 6844.32
- row 18: 6550 | Entertainment | 7241
- row 19: 6680 | Legal and professional fee | 23000
- row 20: 7550 | Web hosting fee | 38439.24
- row 22: formula=[Total: | =SUBTOTAL(9, C2:C21) | =SUBTOTAL(9, D2:D21)]
          values =[Total: | 808136.72 | -808136.72]

## Report sheet: GL 31.12.25

- row 1: Account ID | Account Description | Date | Reference | Jrnl | Trans Description | Debit Amt | Credit Amt | Balance
- row 2: 1010 | NCB HKD CA | 45658 | Beginning Balance
- row 3: 1010 | NCB HKD CA | 45658 | Opening balance | GENJ | Opening balance - NCB HKD CA | 87621.63
- row 4: 1010 | NCB HKD CA | 45717 | NCB HKD CA-2501-001 | GENJ | Accruals:000773 | 3000
- row 5: 1010 | NCB HKD CA | 22/2/25 | NCB HKD CA-2502-001 | GENJ | Web hosting fee:000877 - WIX.com Website Designing and Hosting Services | 2485.86
- row 6: 1010 | NCB HKD CA | 22/2/25 | NCB HKD CA-2502-002 | GENJ | Legal and professional fee:000775 - Lee & Yu Corporate Services Limited - Debit Note C09080-s.88 services | 4800
- row 7: 1010 | NCB HKD CA | 45780 | NCB HKD CA-2503-001 | GENJ | Web hosting fee:000876 - mCommerce - Amazon Web Services - 2025 January 1 to January 31 | 4366.6
- row 8: 1010 | NCB HKD CA | 45780 | NCB HKD CA-2503-002 | GENJ | Accruals:000774 | 4615.41
- row 9: 1010 | NCB HKD CA | 14/3/25 | NCB HKD CA-2503-003 | GENJ | Accruals:000880 - 2024 Autid and Accounting | 12200
- row 10: 1010 | NCB HKD CA | 14/3/25 | NCB HKD CA-2503-004 | GENJ | Legal and professional fee:000878 - Lee & Yu Corporate Services Limited - Debit Note C09092 - trademark registration | 18200
- row 11: 1010 | NCB HKD CA | 15/3/25 | NCB HKD CA-2503-005 | GENJ | Web hosting fee:000879 - mCommerce - Amazon Web Services - 2025 February 1 to February 28 | 4604.13
- row 12: 1010 | NCB HKD CA | 18/3/25 | NCB HKD CA-2503-006 | GENJ | Web hosting fee:000882 - Website development tools : Slidespeak - USD 359 | 2800
- row 13: 1010 | NCB HKD CA | 18/3/25 | NCB HKD CA-2503-007 | GENJ | Entertainment:000881 - Dinner with Vetting Committee | 7241
- row 14: 1010 | NCB HKD CA | 45936 | NCB HKD CA-2506-001 | GENJ | Web hosting fee:000883 - WIX.COM - Website fee | 6026
- row 15: 1010 | NCB HKD CA | 14/6/25 | NCB HKD CA-2506-002 | GENJ | Temp:000884 - mCommerce - Amazon Web Services | 18156.65
- row 16: 1010 | NCB HKD CA | 16/6/25 | NCB HKD CA-2506-003 | GENJ | Bank charges:Return cheque | 150
- row 17: 1010 | NCB HKD CA | 16/6/25 | NCB HKD CA-2506-004 | GENJ | Temp:000884IN-CLEARING RETURN - mCommerce - Amazon Web Services | 18156.65
- row 18: 1010 | NCB HKD CA | 19/6/25 | NCB HKD CA-2506-005 | GENJ | Computer accessories:000885 - eeio Limited - Microsoft 365 Business Standard annual subscription yearly | 6844.32
- row 19: 1010 | NCB HKD CA | 20/6/25 | NCB HKD CA-2506-006 | GENJ | Company secretarial fee:000886 - AC Business Service Limited - Renew Package(Annual Return,Company Secretary) - Service Period: 2025-07-19~2026-07-18 | 4900
- row 20: 1010 | NCB HKD CA | 20/6/25 | NCB HKD CA-2506-007 | GENJ | Interbank:transfer | 50000
- row 21: 1010 | NCB HKD CA | 24/6/25 | NCB HKD CA-2506-008 | GENJ | Web hosting fee:000887 - mCommerce - Amazon Web Services | 18156.65
- row 22: formula=[1010 | NCB HKD CA | Change | 155778.28 | 118546.62 | =G22-H22]
          values =[1010 | NCB HKD CA | Change | 155778.28 | 118546.62 | 37231.66]
- row 23: formula=[31/12/25 | Ending Balance | =SUBTOTAL(9, I2:I22)]
          values =[31/12/25 | Ending Balance | 37231.66]
- row 24: 1020 | NCB HKD SA | 45658 | Beginning Balance
- row 25: 1020 | NCB HKD SA | 45658 | Opening balance | GENJ | Opening balance - NCB HKD SA | 550018.92
- row 26: 1020 | NCB HKD SA | 31/1/25 | NCB HKD SA-2501-001 | GENJ | Bank interest income:Interest | 175.18
- row 27: 1020 | NCB HKD SA | 28/2/25 | NCB HKD SA-2502-001 | GENJ | Bank interest income:Interest | 158.27
- row 28: 1020 | NCB HKD SA | 30/3/25 | NCB HKD SA-2503-001 | GENJ | Bank charges:Auditor’s Confirmation | 300
- row 29: 1020 | NCB HKD SA | 31/3/25 | NCB HKD SA-2503-002 | GENJ | Bank interest income:Interest | 175.25
- row 30: 1020 | NCB HKD SA | 30/4/25 | NCB HKD SA-2504-001 | GENJ | Bank interest income:Interest | 169.59
- row 31: 1020 | NCB HKD SA | 31/5/25 | NCB HKD SA-2505-001 | GENJ | Bank interest income:Interest | 175.3
- row 32: 1020 | NCB HKD SA | 20/6/25 | NCB HKD SA-2506-001 | GENJ | Interbank:transfer | 50000
- row 33: 1020 | NCB HKD SA | 30/6/25 | NCB HKD SA-2506-002 | GENJ | Bank interest income:Interest | 164.56
- row 34: 1020 | NCB HKD SA | 31/7/25 | NCB HKD SA-2507-001 | GENJ | Bank interest income:Interest | 159.48
- row 35: 1020 | NCB HKD SA | 31/8/25 | NCB HKD SA-2508-001 | GENJ | Bank interest income:Interest | 113.22
- row 36: 1020 | NCB HKD SA | 18/9/25 | NCB HKD SA-2509-001 | GENJ | Membership fee income:Cheque Deposit NO.189888 - 2025-M-70105 - MTR Corporation Limited | 6668
- row 37: 1020 | NCB HKD SA | 18/9/25 | NCB HKD SA-2509-001 | GENJ | Receipt in advance:Cheque Deposit NO.189888 - 2025-M-70105 - MTR Corporation Limited | 13332
- row 38: 1020 | NCB HKD SA | 22/9/25 | NCB HKD SA-2509-002 | GENJ | Membership fee income:FPS IN CR - 2025-M-70104 - Hong Kong Exchanges and Clearing Limited | 8335
- row 39: 1020 | NCB HKD SA | 22/9/25 | NCB HKD SA-2509-002 | GENJ | Receipt in advance:FPS IN CR - 2025-M-70104 - Hong Kong Exchanges and Clearing Limited | 11665
- row 40: 1020 | NCB HKD SA | 29/9/25 | NCB HKD SA-2509-003 | GENJ | Receipt in advance:NYITT250188772//NYITT250188772 - 2025-MSHK-60101 - Microsoft Hong Kong Limited | 60000
- row 41: 1020 | NCB HKD SA | 30/9/25 | NCB HKD SA-2509-004 | GENJ | Bank interest income:Interest | 91.07
- row 42: 1020 | NCB HKD SA | 22/10/25 | NCB HKD SA-2510-001 | GENJ | Membership fee income:FPS IN CR | 835
- row 43: 1020 | NCB HKD SA | 22/10/25 | NCB HKD SA-2510-001 | GENJ | Receipt in advance:FPS IN CR - 2025-NGO-70101 - Hong Kong-Shenzhen Innovation and Technology Park Limited | 1165
- row 44: 1020 | NCB HKD SA | 31/10/25 | NCB HKD SA-2510-002 | GENJ | Bank interest income:Interest | 63.88
- row 45: 1020 | NCB HKD SA | 30/11/25 | NCB HKD SA-2511-001 | GENJ | Bank interest income:Interest | 10.66
- row 46: 1020 | NCB HKD SA | 31/12/25 | NCB HKD SA-2512-001 | GENJ | Bank interest income:Interest | 5.12
- row 47: formula=[1020 | NCB HKD SA | Change | 653480.5 | 50300 | =G47-H47]
          values =[1020 | NCB HKD SA | Change | 653480.5 | 50300 | 603180.5]
- row 48: formula=[31/12/25 | Ending Balance | =SUBTOTAL(9, I24:I47)]
          values =[31/12/25 | Ending Balance | 603180.5]
- row 49: 1090 | Interbank | 45663 | Beginning Balance
- row 50: 1090 | Interbank | 20/6/25 | NCB HKD CA-2506-007 | GENJ | Interbank:transfer | 50000
- row 51: 1090 | Interbank | 20/6/25 | NCB HKD SA-2506-001 | GENJ | Interbank:transfer | 50000
- row 52: formula=[1090 | Interbank | Change | 50000 | 50000 | =G52-H52]
          values =[1090 | Interbank | Change | 50000 | 50000 | 0]
- row 53: 1099 | Temp | 45663 | Beginning Balance
- row 54: 1099 | Temp | 14/6/25 | NCB HKD CA-2506-002 | GENJ | Temp:000884 - mCommerce - Amazon Web Services | 18156.65
- row 55: 1099 | Temp | 16/6/25 | NCB HKD CA-2506-004 | GENJ | Temp:000884IN-CLEARING RETURN - mCommerce - Amazon Web Services | 18156.65
- row 56: formula=[1099 | Temp | Change | 18156.65 | 18156.65 | =G56-H56]
          values =[1099 | Temp | Change | 18156.65 | 18156.65 | 0]
- row 57: 1100 | Trade receivable | 45658 | Beginning Balance
- row 58: 1100 | Trade receivable | 45658 | Opening balance | GENJ | Opening balance - Trade receivable | 20000
- row 59: 1100 | Trade receivable | 31/12/25 | JV-AR-2512 | GENJ | 2025 AR:2025-M-70106-Ernst & Young Hong Kong | 20000
- row 60: 1100 | Trade receivable | 31/12/25 | JV-AR-2512 | GENJ | 2025 AR:2025-M-70107-Alibaba Cloud (Singapore) Private Limited | 20000
- row 61: 1100 | Trade receivable | 31/12/25 | JV-AR-2512 | GENJ | 2025 AR:2025-NGO-70102-Hong Kong Cyberport Management Company Limited | 2000
- row 62: 1100 | Trade receivable | 31/12/25 | JV-AR-2512 | GENJ | 2025 AR:2025-NGO-70103-Hong Kong Federation of Insurers | 2000
- row 63: formula=[1100 | Trade receivable | Change | 64000 | =G63-H63]
          values =[1100 | Trade receivable | Change | 64000 | 64000]
- row 64: formula=[31/12/25 | Ending Balance | =SUBTOTAL(9, I49:I63)]
          values =[31/12/25 | Ending Balance | 64000]
- row 65: 1300 | Prepayment | 45658 | Beginning Balance
- row 66: 1300 | Prepayment | 45658 | Opening balance | GENJ | Opening balance - Prepayment | 4900
- row 67: 1300 | Prepayment | 20/6/25 | NCB HKD CA-2506-006 | GENJ | Prepayment:000886 - AC Business Service Limited - Renew Package(Annual Return,Company Secretary) - Service Period: 2025-07-19~2026-07-18 | 4900
- row 68: 1300 | Prepayment | 31/12/25 | JV-l/y prepaid | GENJ | Company secretarial fee:l/y prepayment | 4900
- row 69: formula=[1300 | Prepayment | Change | 9800 | 4900 | =G69-H69]
          values =[1300 | Prepayment | Change | 9800 | 4900 | 4900]
- row 70: formula=[31/12/25 | Ending Balance | =SUBTOTAL(9, I65:I69)]
          values =[31/12/25 | Ending Balance | 4900]
- row 71: 1800 | Office equipment | 45658 | Beginning Balance
- row 72: 1800 | Office equipment | 45658 | Opening balance | GENJ | Opening balance - Office equipment | 5750
- row 73: formula=[1800 | Office equipment | Change | 5750 | =G73-H73]
          values =[1800 | Office equipment | Change | 5750 | 5750]
- row 74: formula=[31/12/25 | Ending Balance | =SUBTOTAL(9, I71:I73)]
          values =[31/12/25 | Ending Balance | 5750]
- row 75: 1850 | Accum Depreciation-OE | 45658 | Beginning Balance
- row 76: 1850 | Accum Depreciation-OE | 45658 | Opening balance | GENJ | Opening balance - Accum Depreciation-OE | 5750
- row 77: formula=[1850 | Accum Depreciation-OE | Change | 5750 | =G77-H77]
          values =[1850 | Accum Depreciation-OE | Change | 5750 | -5750]
- row 78: formula=[31/12/25 | Ending Balance | =SUBTOTAL(9, I75:I77)]
          values =[31/12/25 | Ending Balance | -5750]
- row 79: 2100 | Receipt in advance | 45658 | Beginning Balance
- row 80: 2100 | Receipt in advance | 45658 | Opening balance | GENJ | Opening balance - Receipt in advance | 93484
- row 81: 2100 | Receipt in advance | 18/9/25 | NCB HKD SA-2509-001 | GENJ | Receipt in advance:Cheque Deposit NO.189888 - 2025-M-70105 - MTR Corporation Limited | 13332
- row 82: 2100 | Receipt in advance | 22/9/25 | NCB HKD SA-2509-002 | GENJ | Receipt in advance:FPS IN CR - 2025-M-70104 - Hong Kong Exchanges and Clearing Limited | 11665
- row 83: 2100 | Receipt in advance | 29/9/25 | NCB HKD SA-2509-003 | GENJ | Receipt in advance:NYITT250188772//NYITT250188772 - 2025-MSHK-60101 - Microsoft Hong Kong Limited | 60000
- row 84: 2100 | Receipt in advance | 22/10/25 | NCB HKD SA-2510-001 | GENJ | Receipt in advance:FPS IN CR - 2025-NGO-70101 - Hong Kong-Shenzhen Innovation and Technology Park Limited | 1165
- row 85: 2100 | Receipt in advance | 31/12/25 | JV-l/y trade dep rec | GENJ | Being the reallocation of 2025 sales from trade deposits received. | 81996
- row 86: 2100 | Receipt in advance | 31/12/25 | JV-AR-2512 | GENJ | 2025 AR:2025-M-70107-Alibaba Cloud (Singapore) Private Limited | 11665
- row 87: 2100 | Receipt in advance | 31/12/25 | JV-AR-2512 | GENJ | 2025 AR:2025-NGO-70102-Hong Kong Cyberport Management Company Limited | 1165
- row 88: 2100 | Receipt in advance | 31/12/25 | JV-AR-2512 | GENJ | 2025 AR:2025-M-70106-Ernst & Young Hong Kong | 11665
- row 89: 2100 | Receipt in advance | 31/12/25 | JV-AR-2512 | GENJ | 2025 AR:2025-NGO-70103-Hong Kong Federation of Insurers | 1165
- row 90: formula=[2100 | Receipt in advance | Change | 81996 | 205306 | =G90-H90]
          values =[2100 | Receipt in advance | Change | 81996 | 205306 | -123310]
- row 91: formula=[31/12/25 | Ending Balance | =SUBTOTAL(9, I79:I90)]
          values =[31/12/25 | Ending Balance | -123310]
- row 92: 2200 | Accruals | 45658 | Beginning Balance
- row 93: 2200 | Accruals | 45658 | Opening balance | GENJ | Opening balance - Accruals | 19815.41
- row 94: 2200 | Accruals | 45717 | NCB HKD CA-2501-001 | GENJ | Accruals:000773 | 3000
- row 95: 2200 | Accruals | 45780 | NCB HKD CA-2503-002 | GENJ | Accruals:000774 | 4615.41
- row 96: 2200 | Accruals | 14/3/25 | NCB HKD CA-2503-003 | GENJ | Accruals:000880 - 2024 Autid and Accounting | 12200
- row 97: 2200 | Accruals | 31/12/25 | JV-Accruals-2512 | GENJ | Being the provision for acc + audit fee for the year. | 12200
- row 98: formula=[2200 | Accruals | Change | 19815.41 | 32015.41 | =G98-H98]
          values =[2200 | Accruals | Change | 19815.41 | 32015.41 | -12200]
- row 99: formula=[31/12/25 | Ending Balance | =SUBTOTAL(9, I92:I98)]
          values =[31/12/25 | Ending Balance | -12200]
- row 100: 3910 | Retained Earnings | 45658 | Beginning Balance
- row 101: 3910 | Retained Earnings | 45658 | Opening balance | GENJ | Opening balance - Retained Earnings | 549241.14
- row 102: formula=[3910 | Retained Earnings | Change | 549241.14 | =G102-H102]
          values =[3910 | Retained Earnings | Change | 549241.14 | -549241.14]
- row 103: formula=[31/12/25 | Ending Balance | =SUBTOTAL(9, I100:I102)]
          values =[31/12/25 | Ending Balance | -549241.14]
- row 104: 4000 | Membership fee income | 45658 | Beginning Balance
- row 105: 4000 | Membership fee income | 18/9/25 | NCB HKD SA-2509-001 | GENJ | Membership fee income:Cheque Deposit NO.189888 - 2025-M-70105 - MTR Corporation Limited | 6668
- row 106: 4000 | Membership fee income | 22/9/25 | NCB HKD SA-2509-002 | GENJ | Membership fee income:FPS IN CR - 2025-M-70104 - Hong Kong Exchanges and Clearing Limited | 8335
- row 107: 4000 | Membership fee income | 22/10/25 | NCB HKD SA-2510-001 | GENJ | Membership fee income:FPS IN CR | 835
- row 108: 4000 | Membership fee income | 31/12/25 | JV-l/y trade dep rec | GENJ | Being the reallocation of 2025 sales from trade deposits received. | 81996
- row 109: 4000 | Membership fee income | 31/12/25 | JV-AR-2512 | GENJ | 2025 AR:2025-M-70106-Ernst & Young Hong Kong | 8335
- row 110: 4000 | Membership fee income | 31/12/25 | JV-AR-2512 | GENJ | 2025 AR:2025-M-70107-Alibaba Cloud (Singapore) Private Limited | 8335
- row 111: 4000 | Membership fee income | 31/12/25 | JV-AR-2512 | GENJ | 2025 AR:2025-NGO-70102-Hong Kong Cyberport Management Company Limited | 835
- row 112: 4000 | Membership fee income | 31/12/25 | JV-AR-2512 | GENJ | 2025 AR:2025-NGO-70103-Hong Kong Federation of Insurers | 835
- row 113: formula=[4000 | Membership fee income | Change | 116174 | =G113-H113]
          values =[4000 | Membership fee income | Change | 116174 | -116174]
- row 114: formula=[31/12/25 | Ending Balance | =SUBTOTAL(9, I104:I113)]
          values =[31/12/25 | Ending Balance | -116174]
- row 115: 4100 | Bank interest income | 45658 | Beginning Balance
- row 116: 4100 | Bank interest income | 31/1/25 | NCB HKD SA-2501-001 | GENJ | Bank interest income:Interest | 175.18
- row 117: 4100 | Bank interest income | 28/2/25 | NCB HKD SA-2502-001 | GENJ | Bank interest income:Interest | 158.27
- row 118: 4100 | Bank interest income | 31/3/25 | NCB HKD SA-2503-002 | GENJ | Bank interest income:Interest | 175.25
- row 119: 4100 | Bank interest income | 30/4/25 | NCB HKD SA-2504-001 | GENJ | Bank interest income:Interest | 169.59
- row 120: 4100 | Bank interest income | 31/5/25 | NCB HKD SA-2505-001 | GENJ | Bank interest income:Interest | 175.3
- row 121: 4100 | Bank interest income | 30/6/25 | NCB HKD SA-2506-002 | GENJ | Bank interest income:Interest | 164.56
- row 122: 4100 | Bank interest income | 31/7/25 | NCB HKD SA-2507-001 | GENJ | Bank interest income:Interest | 159.48
- row 123: 4100 | Bank interest income | 31/8/25 | NCB HKD SA-2508-001 | GENJ | Bank interest income:Interest | 113.22
- row 124: 4100 | Bank interest income | 30/9/25 | NCB HKD SA-2509-004 | GENJ | Bank interest income:Interest | 91.07
- row 125: 4100 | Bank interest income | 31/10/25 | NCB HKD SA-2510-002 | GENJ | Bank interest income:Interest | 63.88
- row 126: 4100 | Bank interest income | 30/11/25 | NCB HKD SA-2511-001 | GENJ | Bank interest income:Interest | 10.66
- row 127: 4100 | Bank interest income | 31/12/25 | NCB HKD SA-2512-001 | GENJ | Bank interest income:Interest | 5.12
- row 128: formula=[4100 | Bank interest income | Change | 1461.58 | =G128-H128]
          values =[4100 | Bank interest income | Change | 1461.58 | -1461.58]
- row 129: formula=[31/12/25 | Ending Balance | =SUBTOTAL(9, I115:I128)]
          values =[31/12/25 | Ending Balance | -1461.58]
- row 130: 6000 | Accounting fee | 45658 | Beginning Balance
- row 131: 6000 | Accounting fee | 31/12/25 | JV-Accruals-2512 | GENJ | Being the provision for acc + audit fee for the year. | 5000
- row 132: formula=[6000 | Accounting fee | Change | 5000 | =G132-H132]
          values =[6000 | Accounting fee | Change | 5000 | 5000]
- row 133: formula=[31/12/25 | Ending Balance | =SUBTOTAL(9, I130:I132)]
          values =[31/12/25 | Ending Balance | 5000]
- row 134: 6100 | Auditor's remuneration | 45658 | Beginning Balance
- row 135: 6100 | Auditor's remuneration | 31/12/25 | JV-Accruals-2512 | GENJ | Being the provision for acc + audit fee for the year. | 7200
- row 136: formula=[6100 | Auditor's remuneration | Change | 7200 | =G136-H136]
          values =[6100 | Auditor's remuneration | Change | 7200 | 7200]
- row 137: formula=[31/12/25 | Ending Balance | =SUBTOTAL(9, I134:I136)]
          values =[31/12/25 | Ending Balance | 7200]
- row 138: 6200 | Bank charges | 45658 | Beginning Balance
- row 139: 6200 | Bank charges | 30/3/25 | NCB HKD SA-2503-001 | GENJ | Bank charges:Auditor’s Confirmation | 300
- row 140: 6200 | Bank charges | 16/6/25 | NCB HKD CA-2506-003 | GENJ | Bank charges:Return cheque | 150

## Report sheet: PL 31.12.25

- row 1: Current Month | Year to Date
- row 2: Revenues
- row 3: formula=[Membership fee income | 116174 | =IF(117635.58<>0, (B3/117635.58)*100, 0) | 116174 | =IF(117635.58<>0, (D3/117635.58)*100, 0)]
          values =[Membership fee income | 116174 | 98.75753577276535 | 116174 | 98.75753577276535]
- row 4: formula=[Bank interest income | 1461.58 | =IF(117635.58<>0, (B4/117635.58)*100, 0) | 1461.58 | =IF(117635.58<>0, (D4/117635.58)*100, 0)]
          values =[Bank interest income | 1461.58 | 1.242464227234651 | 1461.58 | 1.242464227234651]
- row 6: formula=[Total Revenues | =ROUND(SUBTOTAL(9, B2:B5), 5) | =ROUND(SUBTOTAL(9, C2:C5), 5) | =ROUND(SUBTOTAL(9, D2:D5), 5) | =ROUND(SUBTOTAL(9, E2:E5), 5)]
          values =[Total Revenues | 117635.58 | 100 | 117635.58 | 100]
- row 9: Cost of Sales
- row 11: formula=[Total Cost of Sales | =ROUND(SUBTOTAL(9, B8:B10), 5) | =ROUND(SUBTOTAL(9, C8:C10), 5) | =ROUND(SUBTOTAL(9, D8:D10), 5) | =ROUND(SUBTOTAL(9, E8:E10), 5)]
          values =[Total Cost of Sales | 0 | 0 | 0 | 0]
- row 13: formula=[Gross Profit | =-(ROUND(-B6+B11, 5)) | =-(ROUND(-C6+C11, 5)) | =-(ROUND(-D6+D11, 5)) | =-(ROUND(-E6+E11, 5))]
          values =[Gross Profit | 117635.58 | 100 | 117635.58 | 100]
- row 15: Expenses
- row 16: formula=[Accounting fee | 5000 | =IF(117635.58<>0, (B16/117635.58)*100, 0) | 5000 | =IF(117635.58<>0, (D16/117635.58)*100, 0)]
          values =[Accounting fee | 5000 | 4.250414712963544 | 5000 | 4.250414712963544]
- row 17: formula=[Auditor's remuneration | 7200 | =IF(117635.58<>0, (B17/117635.58)*100, 0) | 7200 | =IF(117635.58<>0, (D17/117635.58)*100, 0)]
          values =[Auditor's remuneration | 7200 | 6.120597186667503 | 7200 | 6.120597186667503]
- row 18: formula=[Bank charges | 450 | =IF(117635.58<>0, (B18/117635.58)*100, 0) | 450 | =IF(117635.58<>0, (D18/117635.58)*100, 0)]
          values =[Bank charges | 450 | 0.38253732416671893 | 450 | 0.38253732416671893]
- row 19: formula=[Company secretarial fee | 4900 | =IF(117635.58<>0, (B19/117635.58)*100, 0) | 4900 | =IF(117635.58<>0, (D19/117635.58)*100, 0)]
          values =[Company secretarial fee | 4900 | 4.165406418704273 | 4900 | 4.165406418704273]
- row 20: formula=[Computer accessories | 6844.32 | =IF(117635.58<>0, (B20/117635.58)*100, 0) | 6844.32 | =IF(117635.58<>0, (D20/117635.58)*100, 0)]
          values =[Computer accessories | 6844.32 | 5.8182396856461285 | 6844.32 | 5.8182396856461285]
- row 21: formula=[Entertainment | 7241 | =IF(117635.58<>0, (B21/117635.58)*100, 0) | 7241 | =IF(117635.58<>0, (D21/117635.58)*100, 0)]
          values =[Entertainment | 7241 | 6.155450587313805 | 7241 | 6.155450587313805]
- row 22: formula=[Legal and professional fee | 23000 | =IF(117635.58<>0, (B22/117635.58)*100, 0) | 23000 | =IF(117635.58<>0, (D22/117635.58)*100, 0)]
          values =[Legal and professional fee | 23000 | 19.5519076796323 | 23000 | 19.5519076796323]
- row 23: formula=[Web hosting fee | 38439.24 | =IF(117635.58<>0, (B23/117635.58)*100, 0) | 38439.24 | =IF(117635.58<>0, (D23/117635.58)*100, 0)]
          values =[Web hosting fee | 38439.24 | 32.67654225022735 | 38439.24 | 32.67654225022735]
- row 25: formula=[Total Expenses | =ROUND(SUBTOTAL(9, B15:B24), 5) | =ROUND(SUBTOTAL(9, C15:C24), 5) | =ROUND(SUBTOTAL(9, D15:D24), 5) | =ROUND(SUBTOTAL(9, E15:E24), 5)]
          values =[Total Expenses | 93074.56 | 79.1211 | 93074.56 | 79.1211]
- row 27: formula=[Net Income | =-(ROUND(-B13+B25, 5)) | =-(ROUND(-C13+C25, 5)) | =-(ROUND(-D13+D25, 5)) | =-(ROUND(-E13+E25, 5))]
          values =[Net Income | 24561.02 | 20.8789 | 24561.02 | 20.8789]

## Report sheet: BS 31.12.25

- row 2: ASSETS
- row 4: Current Assets
- row 5: NCB HKD CA | 37231.66
- row 6: NCB HKD SA | 603180.5
- row 7: Trade receivable | 64000
- row 8: Prepayment | 4900
- row 10: formula=[Total Current Assets | =ROUND(SUBTOTAL(9, B2:B9), 5)]
          values =[Total Current Assets | 709312.16]
- row 12: Property and Equipment
- row 13: Office equipment | 5750
- row 14: Accum Depreciation-OE | -5750
- row 16: formula=[Total Property and Equipment | =ROUND(SUBTOTAL(9, B11:B15), 5)]
          values =[Total Property and Equipment | 0]
- row 18: Other Assets
- row 20: formula=[Total Other Assets | =ROUND(SUBTOTAL(9, C17:C19), 5)]
          values =[Total Other Assets | 0]
- row 22: formula=[Total Assets | =ROUND(C10+C16+C20, 5)]
          values =[Total Assets | 709312.16]
- row 26: LIABILITIES AND CAPITAL
- row 28: Current Liabilities
- row 29: Receipt in advance | 123310
- row 30: Accruals | 12200
- row 32: formula=[Total Current Liabilities | =ROUND(SUBTOTAL(9, B24:B31), 5)]
          values =[Total Current Liabilities | 135510]
- row 34: Long-Term Liabilities
- row 36: formula=[Total Long-Term Liabilities | =ROUND(SUBTOTAL(9, C33:C35), 5)]
          values =[Total Long-Term Liabilities | 0]
- row 38: formula=[Total Liabilities | =-(ROUND(-C32+-C36, 5))]
          values =[Total Liabilities | 135510]
- row 40: Capital
- row 41: Retained Earnings | 549241.14
- row 42: Net Income | 24561.02
- row 44: formula=[Total Capital | =ROUND(SUBTOTAL(9, B39:B43), 5)]
          values =[Total Capital | 573802.16]
- row 46: formula=[Total Liabilities & Capital | =-(ROUND(-C38+-C44, 5))]
          values =[Total Liabilities & Capital | 709312.16]
