import streamlit as st
from test import CventDemo
import datetime
from decimal import Decimal
from tabulate import tabulate
import datetime
import pandas as pd

def process_query(query):
    return f"You entered: {query}"

def main():
    st.title('Demo')

    query = st.text_input('Enter your query here:')

    if st.button('Process'):
        demo = CventDemo()
        try:
            response, query_text ,columns= demo.run_query(query)
            if response is None:
                st.error("Can't generate query , Try some other Prompt")
            else:
                st.write(f"Query : {query_text}")
                
                try:
                    
                    data = eval(response)
                    result = tabulate(data)
                    data_dict = {col: [t[i] for t in data] for i, col in enumerate(columns)}

                    st.write(f"Results: ")
                    st.table(pd.DataFrame(data_dict))


                except Exception as e:
                    st.write("Query produced no output")
            
        except Exception as e :
            st.error("Can't generate query , Try some other Prompt")



if __name__ == "__main__":
    main()
