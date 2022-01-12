import streamlit as st
from streamlit_ace import st_ace
#from lib.code import *
from io import StringIO
import pandas as pd
import logging
from entities import Source

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

query_params = st.experimental_get_query_params()
logging.info(query_params)
sources = Source.all()
options = [ f"{s.name}({s.id})" for s in sources ]
try:
  query_option = query_params['source_id'][0]
  import re
  source_id = int(re.search("(\d+)", query_option).group())
  logging.info("source_id %s"%source_id)
  option_index = options.index(query_option)
except BaseException as err:
  logging.error(err)
  option_index = 1 
  source_id = 1

logging.info("option_index %s"%option_index)
option_selected = st.sidebar.selectbox('Pick option',
                                        options,
                                        index=option_index)
st.experimental_set_query_params(option=option_selected)

st.header('Create feature')

logging.info("source_id %s"%source_id)
s = Source.find_by_id(int(source_id))
df = s.dataframe()
st.dataframe(df)

st.subheader("Put your code here")

st.text("Example")
st.code("""import numpy as np
def execute(col1, col2):
    print(col1, np.isnan(col1))
    if np.isnan(col1):
        return 1
    else:
        return col1 - col2
    """)

content = None
if not st.button('Use feature as is'):
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

        return pd.DataFrame(new_values)
    o_df = materialize(df, process)
    st.dataframe(o_df)

    st.button('Save')

st.button('Create')