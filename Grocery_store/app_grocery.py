# Import python packages
import streamlit as st
from VannaOpenAI import VannaOpenAI


# ======= BEGIN VANNA SETUP =======
api_key = "API-KEY"
vanna_model_name = 'model'

openai_key = 'AI-KEY'
openai_model = 'gpt-4o-mini'
openai_config = {'api_key': openai_key, 'model': openai_model}

vn = VannaOpenAI(vanna_model=vanna_model_name, vanna_api_key=api_key, config=openai_config)
vn.connect_to_postgres(host='host', dbname='dbname', user='user', password='pass', port='5432')
training_data = vn.get_training_data()
# ======= END VANNA SETUP =======

my_question = st.session_state.get("my_question", default=None)

# Execute streamlit run app_grocery.py

if my_question is None:
    my_question = st.text_input(
        "Ask me a question about your data",
        key="my_question",
    )
else:
    st.text(my_question)
    
    sql = vn.generate_sql(my_question)

    st.text(sql)

    df = vn.run_sql(sql)    
        
    st.dataframe(df, use_container_width=True)

    code = vn.generate_plotly_code(question=my_question, sql=sql, df=df)

    fig = vn.get_plotly_figure(plotly_code=code, df=df)

    st.plotly_chart(fig, use_container_width=True)

    summary = vn.generate_summary(question=my_question, df=df)
    st.text(summary)
