import streamlit as st
# import sqlite3
from plotly.utils import PlotlyJSONEncoder
import google.generativeai as palm
from dotenv import load_dotenv
import os 
import psycopg2
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
import plotly
import plotly.express
import json
import matplotlib.pyplot as plt
import random

from streamlit_lottie import st_lottie 

import datetime
load_dotenv()

API_KEY=os.environ.get("PALM_API_KEY")
palm.configure(api_key=API_KEY)




def contains_numbers(sentence):
    """
    Check if the given sentence contains any numbers and return False if any present, True otherwise.
    """
    # Checking for any digit in the sentence
    return not any(char.isdigit() for char in sentence)

def simulate_palm2(product_name):
#   """Simulates PaLM 2 interaction (replace with actual API call when available)"""
#   description_template = f"{product_name} is a high-quality product that offers..."
  model = "models/text-bison-001"
  if "spent" in product_name or "bought" in product_name or "paid" in product_name or "purchased" in product_name:
        # prompt = "from the given statement, please return only in form of a 5 value list(python format) where 1st value put 'new date' if no date is given ,else put date in yyyy-mm-dd format. 2nd value is who is the vendor .3rd value categorize the expense into any  and only 1 of these :- ['Banking','Insurance','Medical','Travel','Food','Education','Hotel Stay','Others'] and put as the 3rd value . 4th being mode of Cash ie, Credit or Cash only(fill 'unknown' if not explicitly given) and 5th value  is the amount spent.if value not explicitly given, then fill it 'unknown'"+ product_name+"if any vaules is not specified by me then by default its value 'unknown' and no other values  and if category is not explicity specified, then category is also 'unknown' "
        prompt = "from the given statement, please return only in form of a 6 value list(python format) where 1st value put 'new date' if no date is given ,else put date in yyyy-mm-dd format. 2nd value is who is the vendor .3rd value categorize the expense into any  and only 1 of these :- ['Banking','Insurance','Medical','Travel','Food','Education','Hotel Stay','Others'] and put as the 3rd value . 4th being mode of Cash ie, Credit or Cash only(fill 'unknown' if not explicitly given) and 5th value  is the amount spent.if value not explicitly given, then fill it 'unknown'.6th value is the reason of expense(if not expliclitly given fill it with 'new name')"+ product_name+"if any vaules is not specified by me then by default its value 'unknown' and no other values  and if category is not explicity specified, then category is also 'unknown' "
        print("sfsfs")
        response = palm.generate_text(
                  model = model,
                  prompt=prompt,
                  max_output_tokens=1024)
        try:
              r = eval(str(response.result[1:-1]))
              if isinstance(r, list):
                  return r
                  print(r)
        except:
                pass
        
        
        
  else: 
    if contains_numbers(product_name):
        prompt = product_name
        
        prompt="respond normal if and only the statemnt is based on any expense,entry,date,claim or purschase or greeting else reply 'I'm sorry but i'm a expense chatbot .. Please ask any other question' to following statement  "+ product_name+" dont return any table"
        lis= ['Banking','Insurance','Medical','Travel','Food','Education','Hotel Stay','Others']
        if "entry" in prompt and "can" in prompt :  
            response = palm.generate_text(
                  model = model,
                  prompt=prompt,
                  max_output_tokens=1024)
            st.chat_message('assistant',avatar="🤖").write(response.result+"\n Here's What you can add:")
            st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":response.result})
            for item in lis:
                  st.write(f"- {item}")  
                  
            return "please"
                        
        elif "categories" in prompt  :
            
            st.chat_message('assistant',avatar="🤖").write("\n Here's What you can add:")
            st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":"Here's What you can add:"})
            for item in lis:
                  st.write(f"- {item}")  
                  
            return "please"
        elif "report" in  prompt.lower() :
            # prompt = "from the following statement, just put your answer only in the form of a 2 value non nested list where for the 1st value put 'unknown'if not given, else put the purpose of expenseand no other value. 2nd value put 'new date' if no date is given ,else put date in yyyy-mm-dd format (no other value to be filled). "+ product_name+"if any vaules is not specified , then by default its value 'unknown' and no other values  should be put "
            prompt = "from the given statement, please return only in form of a 6 value list(python format) where 1st value put 'new date' if no date is given ,else put date in yyyy-mm-dd format. 2nd value is who is the vendor .3rd value categorize the expense into any  and only 1 of these :- ['Banking','Insurance','Medical','Travel','Food','Education','Hotel Stay','Others'] and put as the 3rd value . 4th being mode of Cash ie, Credit or Cash only(fill 'Unknown' if not explicitly given) and 5th value  is the amount spent.if value not explicitly given, then fill it 'unknown'.6th value is the name of report(if not expliclitly given fill it with 'new name')"+ product_name+"if any vaules is not specified by me then by default its value 'unknown' and no other values  and if category is not explicity specified, then category is also 'unknown' "
            response = palm.generate_text(
                  model = model,
                  prompt=prompt,
                  max_output_tokens=1024)
            print(response.result+"no rep1")
            if '```' in response.result:
                r = response.result.lstrip("`")
                r = response.result.rstrip("`")
                try:
                  
                  r = eval(str(r[0]))
                  if isinstance(r, list):
                          if isinstance(r[0], list):
                              return r[0]
                          else:
                              return r
                  print(r+"no repo") 
                except:
                    pass

                print(response.result[1:-1])
        elif "entry" in  prompt.lower() :
            # prompt = "from the following statement, just put your answer only in the form of a 2 value non nested list where for the 1st value put 'unknown'if not given, else put the purpose of expenseand no other value. 2nd value put 'new date' if no date is given ,else put date in yyyy-mm-dd format (no other value to be filled). "+ product_name+"if any vaules is not specified , then by default its value 'unknown' and no other values  should be put "
            prompt = "from the given statement, please return only in form of a 6 value list(python format) where 1st value put 'new date' if no date is given ,else put date in yyyy-mm-dd format. 2nd value is who is the vendor .3rd value categorize the expense into any  and only 1 of these :- ['Banking','Insurance','Medical','Travel','Food','Education','Hotel Stay','Others'] and put as the 3rd value . 4th being mode of Cash ie, Credit or Cash only(fill 'Unknown' if not explicitly given) and 5th value  is the amount spent.if value not explicitly given, then fill it 'unknown'.6th value is the name of report(if not expliclitly given fill it with 'new name')"+ product_name+"if any vaules is not specified by me then by default its value 'unknown' and no other values  and if category is not explicity specified, then category is also 'unknown' "
            
            response = palm.generate_text(
                  model = model,
                  prompt=prompt,
                  max_output_tokens=1024)
            print(response.result+"no val")
            if '```' in response.result:
                r = response.result.lstrip("`")
                r = response.result.rstrip("`")
                try:
                  
                  r = eval(str(r[1:-1]))
                  print
                  if isinstance(r, list):
                          print("nested")
                          if isinstance(r[0], list):
                              return r[0]
                          else:
                              return r
                  print(r+"no repo") 
                except:
                    pass

        
        else:
          response = palm.generate_text(
                  model = model,
                  prompt=prompt,
                  max_output_tokens=1024)
          print(response.result)

            
        if product_name =='values missing, proceed?':
            return product_name
        
    else:
        if "purpose" in  product_name.lower() :
            # prompt = "from the given statement, return only and only in form of a 2 value list(python format) where 1st value is the purpose of expenseif given else put 'unknown' only, 2nd value put 'new date' if no date is given ,else put date in yyyy-mm-dd format. "+ product_name+"if any vaules is not specified by me then by default its value 'unknown' and no other values  should be put and if department is not explicity specified, then category is also 'unknown' "
            prompt = "from the given statement, please return only in form of a 6 value list(python format) where 1st value put 'new date' if no date is given ,else put date in yyyy-mm-dd format. 2nd value is who is the vendor .3rd value categorize the expense into any  and only 1 of these :- ['Banking','Insurance','Medical','Travel','Food','Education','Hotel Stay','Others'] and put as the 3rd value . 4th being mode of Cash ie, Credit or Cash only(fill 'unknown' if not explicitly given) and 5th value  is the amount spent.if value not explicitly given, then fill it 'unknown'.6th value is reason of expense(if not expliclitly given fill it with 'new date')"+ product_name+"if any vaules is not specified by me then by default its value 'unknown' and no other values  and if category is not explicity specified, then category is also 'unknown' "
            response = palm.generate_text(
                  model = model,
                  prompt=prompt,
                  max_output_tokens=1024)
            
            
            if '```' in response.result:
                r = response.result.lstrip("`")
                r = response.result.rstrip("`")
                try:
                  r = eval(str(r[0]))
                  if isinstance(r, list):
                          if isinstance(r[0], list):
                              return r[0]
                          else:
                              return r
                  print(r+"no val") 
                except:
                    pass
                print(response.result+"no val")



        elif "report" in  product_name.lower() :
            # prompt = "from the following statement, just put your answer only in the form of a 2 value non nested list where for the 1st value put 'unknown'if not given, else put the purpose of expenseand no other value. 2nd value put 'new date' if no date is given ,else put date in yyyy-mm-dd format (no other value to be filled). "+ product_name+"if any vaules is not specified , then by default its value 'unknown' and no other values  should be put "
            prompt = "from the given statement, please return only in form of a 6 value list(python format) where 1st value put 'new date' if no date is given ,else put date in yyyy-mm-dd format. 2nd value is who is the vendor .3rd value categorize the expense into any  and only 1 of these :- ['Banking','Insurance','Medical','Travel','Food','Education','Hotel Stay','Others'] and put as the 3rd value . 4th being mode of Cash ie, Credit or Cash only(fill 'Unknown' if not explicitly given) and 5th value  is the amount spent.if value not explicitly given, then fill it 'unknown'.6th value is the name of report(if not expliclitly given fill it with 'new name')"+ product_name+"if any vaules is not specified by me then by default its value 'unknown' and no other values  and if category is not explicity specified, then category is also 'unknown' "
            response = palm.generate_text(
                  model = model,
                  prompt=prompt,
                  max_output_tokens=1024)
            print(response.result+"no rep1")
            if '```' in response.result:
                r = response.result.lstrip("`")
                r = response.result.rstrip("`")
            if "python" in response.result:
                r=response.response.lstrip("python")
                try:
                  
                  r = eval(str(r[1:-1]))
                  if isinstance(r, list):
                          print("nested")
                          if isinstance(r[0], list):
                              return r[0]
                          else:
                              return r
                  print(r+"no repo") 
                except:
                    pass


        else:
          # prompt = "from the given statement, return only in form of a 5 value list(python format) where 1st value put 'new date' if no date is given ,else put date in yyyy-mm-dd format. 2nd value is who is the vendor if not given put'unknown'.3rd value categorize the expense into any  and only 1 of these :- ['Banking','Insurance','Medical','Travel','Food','Education','Hotel Stay','Others'] and put as the 3rd value put'unknown' if no value is given . 4th being mode of Cash ie, Credit or Cash only and 5th value  is the amount spent.if value not explicitly given, then fill it 'unknown'"+ product_name+"if any vaules is not specified by me then by default its value 'unknown' and no other values  should be put and if category is not explicity specified, then category is also 'unknown' "
          prompt ="from the given statement, please return only in form of a 6 value list(python format) where 1st value put 'new date' if no date is given ,else put date in yyyy-mm-dd format. 2nd value is who is the vendor .3rd value categorize the expense into any  and only 1 of these :- ['Banking','Insurance','Medical','Travel','Food','Education','Hotel Stay','Others'] and put as the 3rd value . 4th being mode of Cash ie, Credit or Cash only(fill 'unknown' if not explicitly given) and 5th value  is the amount spent.if value not explicitly given, then fill it 'unknown'.6th value is the purpose of expense(if not expliclitly given fill it with 'new date')"+ product_name+"if any vaules is not specified by me then by default its value 'unknown' and no other values  and if category is not explicity specified, then category is also 'unknown' "
          response = palm.generate_text(
                    model = model,
                    prompt=prompt,
                    max_output_tokens=1024)
          try:
              r = eval(str(response.result[0]))
              if isinstance(r, list):
                  return r
          except:
                pass
          print(response.result[0]+"hello234")
        # try:
  #       l = eval(str(response.result))
  #       if 0 in l:  # Assuming missing values are denoted by 0
  #           return "values missing, proceed?"
  #       return response.result
  # except Exception as e:
  #       # Handle cases where response cannot be evaluated or other errors
  #       return "Error in processing the response"
      
      
  return response.result
  

          


def create_tables():
  
  # conn = sqlite3.connect('your_database.db')
  # cursor = conn.cursor()
  # # cursor.execute('''DROP TABLE product_data''')
  # cursor.execute('''CREATE TABLE IF NOT EXISTS expense (expenseID INTEGER  PRIMARY KEY AUTOINCREMENT,Date TEXT,expense_Vendor TEXT,expense_ctgry TEXT,expense_amt INTEGER)''')
  # conn.commit()
  # conn.close()
  conn = psycopg2.connect(database="your_database", user="postgres", password="Selva@123", host="localhost", port="5432")
  cursor = conn.cursor()
  create_table_query = """
  CREATE TABLE IF NOT EXISTS expense (
    expense_id SERIAL PRIMARY KEY,
    report_id INT NOT NULL,
    expense_date DATE NOT NULL,
    expense_vendor VARCHAR(100) NOT NULL,
    expense_ctgry VARCHAR(50) NOT NULL,
    expense_pay VARCHAR(20) NOT NULL,
    expense_amt INT NOT NULL,
    CONSTRAINT fk_report_id FOREIGN KEY (report_id) REFERENCES report(report_id) ON DELETE CASCADE,
    CONSTRAINT expense_positive_amt CHECK (expense_amt >= 0)


  );
  """
  cursor.execute(create_table_query)
  conn.commit()
  print("Table 1 created successfully in PostgreSQL")
  create_table_query2 = """
  CREATE TABLE IF NOT EXISTS report1 (
    report_id SERIAL PRIMARY KEY,
    report_name VARCHAR(100) NOT NULL,
    report_date DATE NOT NULL,
    report_dept VARCHAR(50) 
  );
  """
  cursor.execute(create_table_query2)
  conn.commit()
  conn.close()
  print("Table 2 created successfully in PostgreSQL")
q= 0
def ca():
            st.session_state.messages.append({'role':'user','avat':'👨','content':"YES"})
            st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":"Values are added as per your consent"})
            # x x 
            # conn.close()
            st.balloons()
            conn = psycopg2.connect(database="your_database", user="postgres", password="Selva@123", host="localhost", port="5432")
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(report_id) FROM report")
            report_id = cursor.fetchone()[0]
            insert_query = "INSERT INTO expense (report_id,expense_date,expense_vendor,expense_ctgry,expense_pay,expense_amt) VALUES (%s,%s, %s, %s, %s,%s)"
            cursor.execute(insert_query, (report_id,result_list[0], result_list[1], result_list[2],result_list[3],result_list[4]))
            conn.commit()

            insert_query = "INSERT INTO report1  (report_name,report_date) VALUES (%s, %s)"
            
            if result_list[0] == 'new date':
                          result_list[0] = datetime.datetime.now().date()
            cursor.execute(insert_query, (result_list[5], result_list[0]))
            conn.commit()

            conn.close()  
            print("Data inserted successfully into PostgreSQL table")
                  


def ca1():
            st.session_state.messages.append({'role':'user','avat':'👨','content':"YES"})
            st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":"Values are added as per your consent."})
            # x x 
            # conn.close()
            st.balloons()
            conn = psycopg2.connect(database="your_database", user="postgres", password="Selva@123", host="localhost", port="5432")
            cursor = conn.cursor()
            insert_query = "INSERT INTO report1  (report_name,report_date) VALUES (%s, %s)"
            cursor.execute(insert_query, (result_list[0], result_list[1]))
            conn.commit()

            conn.close()
            print("Data inserted successfully into PostgreSQL table")                  
def cl():
            st.session_state.messages.append({'role':'user','avat':'👨','content':"NO"})
            st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":"Thanks for your consent . Values will not be added. "})
    
create_tables()

lk = []
# st.image("SAP-Logo-700x394.jpg",width=120)
text = "A new way to enter your expenses"

messages_placeholder = st.empty()



# url = requests.get( 
# 	"https://lottie.host/38ee157f-0929-47b3-a950-031e88c1ac73/VJHiXMRUlR.json") 
# # Creating a blank dictionary to store JSON file, 
# # as their structure is similar to Python Dictionary 
# url_json = dict() 

# if url.status_code == 200: 
# 	url_json = url.json() 
# else: 
# 	print("Error in the URL")
c1, c2 = st.columns(2)

path = "Animation - 1711426284627.json"
with open(path,"r") as file: 
    url = json.load(file) 
st_lottie(url, 
    reverse=True, 
    height=100, 
    width=100, 
    speed=2, 
    loop=True, 
    quality='high', 
    key='Car'
)

# st_lottie(url_json) 

text = "A new way to enter your expenses"
rule1 = "1. As a user, please refrain from entering unrelated statements or queries to maintain the focus on expense-related tasks."
rule2 = "2. As a user, please provide all necessary details when entering an expense, including the date, vendor, category, payment mode, and amount spent."
rule3 = "3. As a user, please avoid using ambiguous or incomplete statements when entering expenses to prevent misinterpretation by the chatbot."
rule4 = "4. As a user, please refrain from entering multiple expenses in a single statement. Provide details for one expense at a time to ensure clarity and accurate processing by the chatbot."
rule5 = "5. Please be advised that while the chatbot is designed to provide information and responses based on a wide range of data and programming logic, there are instances where the provided answers may not fully encompass all aspects of the query or might not be entirely accurate" 
st.title('Enter your expenses')
with st.expander("Guidelines for the user", expanded=False):
    st.write(rule1)
    st.write(rule2)
    st.write(rule3)
    st.write(rule4)
    st.write(rule5)
messages_placeholder = st.empty()
# Placeholder for the button (if needed)
button_placeholder = st.empty()

if "messages" not in st.session_state:
  st.session_state.messages = []
for message in st.session_state.messages:
              st.chat_message(message['role'],avatar=message['avat']).markdown(message['content'])
product_name = st.chat_input("What's today's entry about?")

if product_name:
  st.chat_message('user',avatar="👨").markdown(product_name)
  st.session_state.messages.append({'role':'user','avat':'👨','content':product_name})

  if product_name:
    simulated_description = simulate_palm2(product_name)
    if "```" in simulated_description:
        print('heloo therre')
        
        p='klj'
        simulated_description=simulated_description.lstrip("`")
        simulated_description=simulated_description.rstrip("`")
        print(simulated_description)
    try:
        result_list = eval(str(simulated_description))
        if isinstance(result_list, list):
            print("The list is:", result_list)
            if len(result_list) == 6:
                if 'unknown' in result_list:  # Assuming missing values are denoted by 0
                  
                
                  if result_list[3].lower()== 'unknown' and result_list[1].lower()== 'unknown'  and result_list[2].lower()== 'unknown'  and result_list[4].lower()== 'unknown' and result_list[0]!= 'new date':
                      print("no mode")
                      st.chat_message('assistant',avatar="🤖").markdown("Sure but you havent entered the mode of payment ... Please enter the values again..")
                      st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":"Sure You havent entered the mode of payment."})
                      st.progress(50, text="Mode of payment is important!!")
                      p = result_list[0]
                      print(p)
                  if result_list[3].lower()== 'unknown' and result_list[1].lower()!= 'unknown'  and result_list[2].lower()!= 'unknown'  and result_list[4].lower()!= 'unknown' :
                      print("no mode")
                      st.chat_message('assistant',avatar="🤖").markdown("You havent entered the mode of payment ... Please enter the values again..")
                      st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":"You havent entered the mode of payment."})
                      st.progress(50, text="Mode of payment is important!!")
                      
                  if result_list[1].lower()== 'unknown'  and result_list[2].lower()== 'unknown'  and result_list[4].lower()== 'unknown' and result_list[3].lower()!= 'unknown' :
                            st.chat_message('assistant',avatar="🤖").markdown("You havent entered the Amount, the vendor and category  ... Please Enter again..")
                            st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":"You havent entered the Amount, the vendor and category."})
                            st.progress(25, text="3 more details to be added...")
                    
                  elif result_list[1].lower()!= 'unknown' and result_list[3].lower()!= 'unknown' :
                    if result_list [2].lower()== 'unknown'  or result_list [4].lower()== 'unknown' :
                      if result_list [4].lower()== 'unknown'  and result_list[2].lower()== 'unknown':
                        print("unkown 2")
                        simulated= simulate_palm2( "values missing, proceed?")
                        if simulated=="values missing, proceed?":
                            st.chat_message('assistant',avatar="🤖").markdown("You havent entered the category and the amount  ... Please enter the values again..")
                            st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":"You havent entered the category and the amount."})
                            st.progress(50, text="Two more details to be added")
                      elif result_list[4].lower()== 'unknown' :
                            print("unkown 2")
                            simulated= simulate_palm2( "values missing, proceed?")
                            if simulated=="values missing, proceed?":
                                st.chat_message('assistant',avatar="🤖").markdown("You havent entered the amount  ... Please Enter again..")
                                st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":"You havent entered the amount."})
                                st.progress(75, text="ONE more detail to be added!")
                      elif result_list[2].lower()== 'unknown' :
                            print("unkown 2")
                            simulated= simulate_palm2( "values missing, proceed?")
                            if simulated=="values missing, proceed?":
                                st.chat_message('assistant',avatar="🤖").markdown("You havent entered the category  ... Please Enter again..")
                                st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":"You havent entered the category."})
                                st.progress(75, text="ONE more detail to be added!")
                      
          
                
                  elif result_list[2].lower()!= 'unknown' and result_list[3].lower()!= 'unknown' :
                    if result_list [1].lower()== 'unknown'  or result_list [4].lower()== 'unknown' :
                      if result_list [1].lower()== 'unknown'  and result_list [4].lower()== 'unknown' :
                          simulated= simulate_palm2( "values missing, proceed?")
                          if simulated=="values missing, proceed?":
                            st.chat_message('assistant',avatar="🤖").markdown("You havent entered the vendor and the amount  ... Please Enter again..")
                            st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":"You havent entered the vendor and the amount."})
                            st.progress(50, text="Two more details to be added.")

                      elif result_list [1].lower()== 'unknown' and result_list[3].lower()!= 'unknown':
                          simulated= simulate_palm2( "values missing, proceed?")
                          if simulated=="values missing, proceed?":
                            st.chat_message('assistant',avatar="🤖").markdown("You havent entered the vendor  ... Please Enter again..")
                            st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":"You havent entered the vendor."})
                            st.progress(75, text="ONE more detail to be added!")
          
                        
                      elif result_list[4].lower() == "unknown":
                          simulated= simulate_palm2( "values missing, proceed?")
                          if simulated=="values missing, proceed?":
                            st.chat_message('assistant',avatar="🤖").markdown("You havent entered the amount  ... Please Enter again..")
                            st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":"You havent entered the amount."})
                            st.progress(75, text="ONE more detail to be added!")
          
                        

                  elif result_list[4].lower() != "unknown" and result_list[3].lower()!= 'unknown':
                      print("hereevsv")
                      if result_list [1].lower()== 'unknown'  or result_list [2].lower()== 'unknown' :
                        if result_list [2].lower()== 'unknown'  and result_list [2].lower()== 'unknown' :
                          simulated= simulate_palm2( "values missing, proceed?")
                          if simulated=="values missing, proceed?":
                              st.chat_message('assistant',avatar="🤖").markdown("You havent entered the vendor and the category ... Please Enter again..")
                              st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":"You havent entered the vendor and the category."})
                              st.progress(50, text="Two more details to be added")

                          elif result_list[1].lower() =="unknown":
                              simulated= simulate_palm2( "values missing, proceed?")
                              if simulated=="values missing, proceed?":
                                st.chat_message('assistant',avatar="🤖").markdown("You havent entered the vendor  ... Please Enter again..")
                                st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":"You havent entered the vendor. "})
                                st.progress(75, text="ONE more detail to be added!")
                          elif result_list[2].lower() =="unknown":
                                simulated= simulate_palm2( "values missing, proceed?")
                                if simulated=="values missing, proceed?":
                                  st.chat_message('assistant',avatar="🤖").markdown("You havent entered the category  ... Please Enter again..")
                                  st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":"You havent entered the category."})
                                  st.progress(75, text="ONE more detail to be added!")
                          
                          elif result_list[4].lower() == "unknown":
                              simulated= simulate_palm2( "values missing, proceed?")
                              if simulated=="values missing, proceed?":
                                st.chat_message('assistant',avatar="🤖").markdown("You havent entered the amount  ... Please Enter again..")
                                st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":"You havent entered the amount."})
                                st.progress(75, text="ONE more detail to be added!")
                 
          
                else:
                    st.progress(100, text="ALL DONE!!")
                    okl=['Date','Expense vendor','Expense Category','Expense Pay (Mode)','Expense amount']
                    st.chat_message('assistant',avatar="🤖").markdown(" Can we proceed with these values?")
                    st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":"Can we proceed with these values?"})    
                    # st.write(str(result_list))
                    if result_list[0] == 'new date':
                        result_list[0] = datetime.datetime.now().date()
                    if result_list[5].lower() =='new name':
                      result_list[5]= result_list[2]+" Expense"
                    print (p+"date check")
                    if p!="klj":
                        result_list[0]=p
                        print("change ate"+p)
                    with st.expander("Values to be entered:", expanded=False):
                      st. write ("1. "+str(okl[0])+ " -- "+str(result_list[0]) )
                      st. write ("2. "+str(okl[1])+ " -- "+str(result_list[1]))
                      st. write ("3. "+str(okl[2])+ " -- "+str(result_list[2]))
                      st. write ("4. "+str(okl[3])+ " -- "+str(result_list[3]))
                      st. write ("5. "+str(okl[4])+ " -- "+str(result_list[4]))
                      st. write ("6. "+"Purpose "+ " -- "+str(result_list[5]))
                      col1, col2 = st.columns(2)
                      button1 = col1.button("YES",on_click=ca)
                      button2 = col2.button("NO",on_click=cl)    
            elif len(result_list) == 2:
                    # st.write(str(result_list))
                    if 'unknown' in result_list or 'Unknown' in result_list:
                          if result_list[1].lower() == 'unknown':
                              simulated= simulate_palm2( "values missing, proceed?")
                              if simulated=="values missing, proceed?":
                                st.chat_message('assistant',avatar="🤖").markdown("Sure I can !!  However you havent entered the date ...  \nPlease Enter again...")
                                st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":"Sure I can !!  However you havent entered the date."})
                                st.progress(66, text="One more detail to be added!!")
                               
                          elif result_list[0].lower() == 'unknown':
                              simulated= simulate_palm2( "values missing, proceed?")
                              if simulated=="values missing, proceed?":
                                st.chat_message('assistant',avatar="🤖").markdown("Sure I can !!  However you havent entered the name of the expense ... \n Please Enter again...")
                                st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":"Sure I can !! However you havent entered the name of the expense."})
                                st.progress(66, text="One more detail to be added!!")
                          
                    else:
                      st.progress(100, text="ALL DONE!!")
                      st.chat_message('assistant',avatar="🤖").markdown(" Sure I can !! Can we proceed with these values?")
                      st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":"Sure I can !! Can we proceed with these values?"})    
                      
                      if result_list[1] == 'new date':
                          result_list[1] = datetime.datetime.now().date()
                      with st.expander("Values to be entered:", expanded=False):
                        st. write ("1. Expense Name -- "+""+str(result_list[0]) )
                        st. write ("2. Expense Date"+ " -- "+str(result_list[1]))
                        col1, col2 = st.columns(2)
                        button1 = col1.button("YES",on_click=ca1)
                        button2 = col2.button("NO",on_click=cl)
                        
                    
    except:
          if simulated_description == "OK":
              # print("ryt here")
              # st.chat_message('assistant',avatar="🤖").markdown(simulated_description)
              # st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":simulated_description})
             
              
              conn = psycopg2.connect(database="your_database", user="postgres", password="Selva@123", host="localhost", port="5432")
              cur = conn.cursor()
              cur.execute('''SELECT report_dept, SUM(expense_amt) AS total_expense FROM report 
                                JOIN expense ON report.report_id = expense.report_id 
                                GROUP BY report_dept''')
              data = cur.fetchall()
              cur.close()
              conn.close()
              departments = [row[0] for row in data]
              total_expense = [row[1] for row in data]

                  
                  # st.bar_chart(data=pd.DataFrame({"Department": departments, "Total Expense": total_expense}))
              df= pd.DataFrame({"Departments": departments, "Total Expense": total_expense})
              
              # Call the selected plot function based on the user's choice
              
              st.bar_chart(df,x="Departments", y="Total Expense")
              st.line_chart(df,x="Departments", y="Total Expense")
              st.scatter_chart(x="Departments", y="Total Expense", data=df)
              st.area_chart(df,x="Departments", y="Total Expense")
              

                        
              
          elif simulated_description == "please":
              pass      
          else:
            print("Invalid input.")       
            st.chat_message('assistant',avatar="🤖").markdown(simulated_description)
            st.session_state.messages.append({"role":"assitance",'avat':'🤖',"content":simulated_description})
            
    
  else:
    st.error("Please enter a product name.")

