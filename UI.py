import streamlit as st
from sql import CventDemo
import datetime
from decimal import Decimal
from tabulate import tabulate
import datetime


def process_query(query):
    return f"You entered: {query}"

def main():
    st.title('Demo')

    query = st.text_input('Enter your query here:')

    if st.button('Process'):
        demo = CventDemo()
        response, query_text = demo.run_query(query)
        if response is None:
            st.error("Invalid query. Please enter a valid query.")
        else:
            st.write(f"Query : {query_text}")
            
            try:
                data = eval(response)
                result = tabulate(data)
                print(tabulate(data))
                st.write(f"Results: ")
                st.table(data)

            except Exception as e:
                st.write("Query produced no output")
           



if __name__ == "__main__":
    main()
