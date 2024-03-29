import streamlit as st
from streamlit.logger import get_logger
from aws import *

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="Dashboard Parkinsons",
        page_icon="👋",
        layout="wide"
    )

    st.write("# Parkinson Dash Streamlit! 👋")
    #st.image('logoCP.jpg', width=200)
    st.sidebar.success("Elige una página.")

    #st.dataframe(schedules())
    adf = audio_data(True)
    adf=adf[adf.id.str.contains('.mp3')]
    for k in ['user','date']:
        adf[k]=adf.data.apply(lambda d: eval(d).get(k))
    sdf = adf.groupby('user').agg({'date': ['min','max','size']})
    st.dataframe(sdf)

    # now norm+plot it!
    base = [144,815,1486,2903,3722,0.02,0.05]
    #full_audio['nfa'] = full_audio['coefs'].apply(lambda c: [(cix/bix) for cix, bix in zip(c,base)])
    #full_audio = full_audio.drop(columns=['coefs'])
    #dfa = {}
    #for ix in range(5):
    #    dfa['F%d' %ix] = full_audio['nfa'].apply(lambda nfa: nfa[ix])
    #dfa['rapJitter'] = full_audio['nfa'].apply(lambda nfa: nfa[5])
    #dfa['localShimmer'] = full_audio['nfa'].apply(lambda nfa: nfa[6])

    #fdf = pd.DataFrame(dfa)
    st.header('Variabilidad Medida en Pacientes (coeficientes normalizados)')
    #st.line_chart(data=fdf)
    #st.dataframe(full_audio)
    

if __name__ == "__main__":
    run()
