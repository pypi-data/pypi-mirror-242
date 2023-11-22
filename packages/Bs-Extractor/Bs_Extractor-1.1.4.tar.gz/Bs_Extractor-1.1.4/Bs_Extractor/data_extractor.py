from Bs_Extractor.functions import *
import Bs_Extractor.constants as const
import fitz
from unidecode import unidecode
import re
import numpy as np
import subprocess


class Bs_Extractor:
        
        def __init__(self, pdf_bytes):
                
                self.pdf_bytes = pdf_bytes

        def extract_data(self):
    ### 1. Data Extraction (from pdf) ---------------------------------

            doc = fitz.open(stream=self.pdf_bytes, filetype="pdf")
            plain_text_data = []

            for page in doc:
                page_output = [unidecode(block[4]) for block in page.get_text("blocks") if block[6] == 0]
                if len(page_output)>0:
                    plain_text_data.append(page_output)
                
                
            if plain_text_data:

                plain_text_data=[x for y in plain_text_data for x in y]
                plain_text_data=[ele.strip() for ele in plain_text_data if ele.strip() and ele != '\n']
                plain_text_data=[ele.replace('\n',' ') for ele in plain_text_data]
                
            else:
                ### raise an error : nto a valid file
                
                raise Exception("Unrecognized or Unsupported Document")
            
            most_coomon_datepattern=''
            
            enbd_flag=False
            
            try:
                #endb_case=[ele for ele in res['plain_text_data'] if 'BROUGHT FORWARD' in ele]
                
                most_coomon_datepattern=check_dates_and_format_patterns_in_list([[ele for ele in plain_text_data if 'BROUGHT FORWARD' in ele][0]])[0][-1]
  
               # most_coomon_datepattern=list(set([ele[-1] for ele in check_dates_and_format_patterns_in_list([ele for ele in plain_text_data if 'BROUGHT FORWARD' in ele][0])]))[0]
                
                most_coomon_datepattern=list(set([ele[-1] for ele in check_dates_and_format_patterns_in_list([[ele for ele in plain_text_data if 'BROUGHT FORWARD' in ele][0]])]))[0]
                print('this the most common patter:',most_coomon_datepattern)
                enbd_flag=True
                
                
            except:
                pass
            
            if not most_coomon_datepattern:
                print('not generated')
                
                most_coomon_datepattern=split_based_on_dates(plain_text_data)[-1]

            plain_text_data=remove_dates_not_matching_format(plain_text_data,most_coomon_datepattern)

            plain_text_data=rearrange_dates_in_list(plain_text_data)


            ### 2. Iban Extraction ---------------------------------

            ##Pattern to match 'AE' followed by 21 digits
            pattern = r'AE\d{21}'

            # Search for the pattern in the provided string
            match = re.search(pattern, ''.join(plain_text_data).replace(' ',''))


            # Extracting the matched string
            Iban = match.group(0) if match else None

            rans,most_coomon_datepattern=split_based_on_dates(plain_text_data)[:2]

            if Iban:
                rans=[ele for ele in rans if (len(ele)>20) and (Iban not in ele)]
                
                acc_number=Iban[8:]
            else:
                rans=[ele for ele in rans if (len(ele)>20)]
                Iban=''
                acc_number=''

            ### 3. Processing of Transaction Data  ---------------------------------

            # Regular expression to match the last occurrence of a digit, currency symbol, or 'xx.xx' pattern
            regex_pattern = r"(Cr|Dr|AED|USD|EUR|\b\d+\.\d{2}\b|\d)(?![\s\S]*\d)"
            
            if enbd_flag:
                print('this is enbd')
                
                #match_index = find_all_cr_preceded_by_digit_in_list([ele for ele in plain_text_data if (('BROUGHT FORWARD' not in ele ) and ('CARRIED FORWARD' not in ele))])
                #cleaned_transactions=[plain_text_data[i] for i in match_index]
                cleaned_transactions=extract_elements_with_specific_date_format([ele for ele in plain_text_data if (('BROUGHT FORWARD' not in ele ) and ('CARRIED FORWARD' not in ele))],most_coomon_datepattern)
                cleaned_transactions=split_based_on_dates(cleaned_transactions)[0]
                order = determine_order(cleaned_transactions[1:-1])
                final_output = sort_list_by_date(cleaned_transactions, most_coomon_datepattern,order)
                extraction_input=filter_elements_with_decimal_digit(final_output)
                transaction_sal_liq=extraction_input

#                 final_output=extraction_input=cleaned_transactions
                
            else:
                cleaned_transactions = []
                for transaction in rans:
                    match = re.search(regex_pattern, transaction)
                    if match:
                        # Truncate the string at the end of the match
                        cleaned_transaction = transaction[:match.end()].strip()
                        cleaned_transactions.append(cleaned_transaction)
                    else:
                        # In case no pattern is found, keep the transaction as is
                        cleaned_transactions.append(transaction)

                cleaned_transactions=sort_digits_preserving_order(cleaned_transactions)
                cleaned_transactions=[ele for ele in cleaned_transactions if len(ele)>20]
                cleaned_transactions=extract_elements_with_specific_date_format(cleaned_transactions,most_coomon_datepattern)
                order = determine_order(cleaned_transactions[1:-1])
                final_output = sort_list_by_date(cleaned_transactions, most_coomon_datepattern,order)
                extraction_input=filter_elements_with_decimal_digit(final_output)
                transaction_sal_liq=filter_elements_with_decimal_digit(extraction_input)

            ### 4. liquidity Extraction  ---------------------------------
           # transaction_sal_liq=filter_elements_with_decimal_digit(extraction_input)
            
            #print('transaction_sal_liq',transaction_sal_liq)
            try:
                liquidity=[ele for ele in plain_text_data if 'CARRIED FORWARD' in ele ][-1]
                liquidity=extract_liquidity(liquidity)
                
            
            except:
                
                try:

                    last_transaction=transaction_sal_liq[-1]
                    if  'balance' or 'turn over' in transaction_sal_liq[-1].lower():
                        
                        last_transaction=transaction_sal_liq[-2]
                    #last_transaction=transaction_sal_liq[-1]

                except:
                    last_transaction=''

                if last_transaction:
                    liquidity=extract_liquidity(last_transaction)

                
            ### 5. Salary Extraction  ---------------------------------
                
            regex = re.compile(r"(?:^|[^a-zA-Z])(SAL)(?=[^a-zA-Z]|$)")

            salary = [
                ele.lower() for ele in transaction_sal_liq
                if (
                    "salary" in ele.lower()
                    or (("wps" in ele.lower() or "hr" in ele.lower()) and "sal" in ele.lower())
                    or regex.search(ele)
                )
            ]

            salary=[ele.replace('+','') for ele in salary]
           # print(salary)


            if len(salary)==0:
                salary = [
                ele.lower() for ele in plain_text_data
                if (
                    "salary" in ele.lower()
                    or (("wps" in ele.lower() or "hr" in ele.lower()) and "sal" in ele.lower())
                    or regex.search(ele)
                )
            ]

                salary=[ele.replace('+','') for ele in salary]
                
            try:

                avg_salary=round(np.mean([float(extract_salary(ele).replace(',','')) for ele in salary]),2)
                if np.isnan(avg_salary):
                    avg_salary=''
            except:
                avg_salary=''


            ## 6. first transaction date  ---------------------------------

            first_trans_date=extract_date_from_string(extraction_input[0], most_coomon_datepattern)

            ### 7. last transaction date  ---------------------------------

            last_transaction_date=extract_date_from_string(extraction_input[-1], most_coomon_datepattern)

#             ### 8. Customer Name Extraction ---------------------------------

            Cust_Name=extract_name(plain_text_data)

            if not Cust_Name:
                try:
                    Cust_Name=' '.join([subele for subele in [ele for ele in plain_text_data if ('account' in ele.lower() and 'name' in ele.lower()) or  ('name' in ele.lower())][0].split(' ') if subele.isupper()])
                    
                except:
                    Cust_Name=''

            ### 9. Account Number Extraction ---------------------------------
            
            if not acc_number:
                
                
                pattern = r'\b\d{9,16}\b'
                # Search for the pattern in the provided string
                if enbd_flag:
                    match=re.search(pattern, ''.join(list( set(plain_text_data)-set(cleaned_transactions))).replace(' ',''))
                else:
                    
                    match=re.search(pattern, ''.join(set(plain_text_data)-set(extract_elements_with_specific_date_format(plain_text_data,most_coomon_datepattern))))
                    #match = re.search(pattern, ''.join(plain_text_data).replace(' ',''))

                # Extracting the matched string
                acc_number = match.group(0) if match else None

            #######-------- Final Output -----------
                
            final_json={
                'Iban':Iban,
                'Account_Number':acc_number,
                'liquidity':liquidity,
                'salary':avg_salary,
              #  'salary_list':salary,
                'first_trans_date':first_trans_date,
                'last_transaction_date':last_transaction_date,
                'Customer_Name':Cust_Name,
               # 'cleaned_transactions':cleaned_transactions,
               #'final_output' :final_output,
                #'extraction_input':extraction_input,
               #'transaction_sal_liq' :transaction_sal_liq,
               # 'plain_text_data':plain_text_data,
                #'transaction_sal_liq':transaction_sal_liq,
               # 'most_coomon_datepattern':most_coomon_datepattern,
                #'rans':rans
                
            }

            return final_json


        def check_pdf_metadata(self):

            try:
                # Run the pdfinfo command with input as bytes
                # print('before run')
                pdfinfo_process = subprocess.run(["pdfinfo", "-"], input=self.pdf_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if pdfinfo_process.returncode != 0:
                    raise Exception("pdfinfo command failed.")
                
                pdfinfo_output = pdfinfo_process.stdout

                # print(pdfinfo_output)
            except FileNotFoundError:
                 raise Exception("pdfinfo command not found. Make sure it's installed and in your PATH.")
                
            # Extract the creator and producer strings, created_at, and modified_at from the pdfinfo output
            creator_string = None
            producer_string = None
            created_at = None
            modified_at = None

            for line in pdfinfo_output.splitlines():
                line_str = line.decode('utf-8')  # Convert bytes to string
                if line_str.startswith("Creator:"):
                    creator_string = line_str[len("Creator:"):].strip()
                elif line_str.startswith("Producer:"):
                    producer_string = line_str[len("Producer:"):].strip()
                elif line_str.startswith("CreationDate:"):
                    created_at = line_str[len("CreationDate:"):].strip()
                elif line_str.startswith("ModDate:"):
                    modified_at = line_str[len("ModDate:"):].strip()

            # crt_list_good= const.creator_lst_good
            # crt_list_bad=const.creator_lst_bad
            # prod_list_good=const.producer_lst_good
            # prod_list_bad=const.producer_lst_bad
            # # Check conditions based on the presence of strings in the lists and created/modified timestamps
            # if creator_string in crt_list_good and producer_string in prod_list_good:
            #     return None
            # elif creator_string in crt_list_good and producer_string in prod_list_bad:
            #      raise Exception("Uploaded an edited PDF")
            # elif creator_string in crt_list_bad and producer_string in prod_list_good:
            #     raise Exception("Uploaded an edited PDF")
            # elif creator_string in crt_list_bad and producer_string in prod_list_bad:
            #      raise Exception("Uploaded an edited PDF")
            # elif creator_string not in crt_list_good + crt_list_bad and producer_string in prod_list_good:
            #     if created_at == modified_at:
            #         return None
            #     else:
            #         raise Exception("Uploaded an edited PDF")
            # elif creator_string not in crt_list_good + crt_list_bad and producer_string in prod_list_bad:
            #     raise Exception("Uploaded an edited PDF")
            # elif creator_string in crt_list_good and producer_string not in prod_list_good + prod_list_bad:
            #     if created_at == modified_at:
            #         return None
            #     else:
            #         return False, "Uploaded an edited PDF"
            # elif creator_string in crt_list_bad and producer_string not in prod_list_good + prod_list_bad:
            #      raise Exception("Uploaded an edited PDF")
            # else:
            #     if created_at == modified_at:
            #         return None
            #     else:
            #         raise Exception("Uploaded an edited PDF")

            meta_data={
            'creator_string':creator_string,
            'producer_string':producer_string,
            'created_at' :created_at,
            'modified_at' :modified_at
            }

            return meta_data