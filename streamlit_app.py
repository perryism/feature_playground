from entities.source import BigQuerySource
import streamlit as st
from streamlit_ace import st_ace
#from lib.code import *
from io import StringIO
import pandas as pd
import logging
from entities import Source
from libs.nuclio import *

logging.basicConfig(filename='logs/test.log', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)

st.markdown("""
<style>
/* The input itself */
.element-container:nth-child(odd) > div > div > div > div > span{
  background-color: green !important;
}
</style>
""", unsafe_allow_html=True)

from web import Assets

st.components.v1.html(Assets.logo(1))

query_params = st.experimental_get_query_params()
logging.info(query_params)
sources = Source.all()
options = [ f"{s.name}({s.id})" for s in sources ]

#FIXME: don't try/except as control flow
try:
  source_id = int(query_params['source_id'][0])
  logging.info("source_id %s"%source_id)
except BaseException as err:
  logging.error(err)
  source_id = 1

s = Source.find_by_id(int(source_id))

df = None
with st.spinner(f"Loading data from {type(s).__name__}"):
  df = s.dataframe()

st.dataframe(df)

st.subheader("Put your code here")

st.text("Example")
st.code("""import numpy as np
def execute(row):
    col1 = row["col1"]
    print(col1, np.isnan(col1))
    if np.isnan(col1):
        return 1
    else:
        return col1 - col2
    """)


content = st_ace()

from libs.code import parse
# Display editor's content as you type
if content is not None and len(content) > 0:
    func_names = parse(content)
    func_name = func_names[0]
    print(func_name)
    exec(content)
    exec(f"process = {func_name}")

    def materialize(df, process):
        new_values = []
        for index, row in df.iterrows():
            new_values.append(process(row))

        return pd.DataFrame(new_values, columns=[func_name])
    o_df = materialize(df, process)

    new_df = pd.concat([o_df, df], axis=1)
    st.dataframe(new_df)
    st.download_button("Download dataframe", data=new_df.to_csv().encode('utf-8'), file_name="new.csv")

    st.subheader("Create new source")
    n = st.text_input("Data source name")    
    if st.button('Create'):
      Source.create(n, new_df)