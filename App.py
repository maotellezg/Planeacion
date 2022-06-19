"""
Created on Thu Jun  2 03:36:02 2022

@author: Mauricio A Tellez
"""

import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
#from math import ceil
from io import BytesIO




# Path del modelo preentrenado
MODEL_PATH = 'pickle_model.pkl'
df = pd.read_excel( "MOI.xlsx")
dfentidad=df["Entidad"].unique()
dfcapacidad=df["Capacidad"].unique()
dfsector=df["Sector"].unique()
dfestrategia=df["estrategia"].unique()
#df_selection =df  


# Se recibe la imagen y el modelo, devuelve la predicción

def main():
    # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
    st.set_page_config(page_title="Portal", layout="wide")
    
    
    
    # Título
    
    
    st.sidebar.header("Filtro")
    
    with st.sidebar:
        
        TodaOfera = st.radio(
            "Ver toda la Oferta",
            ("Activar filtros", "Ver toda la oferta","Indicadores" )
        )

    if TodaOfera ==  "Ver toda la oferta":
      
       st.title("Portafolio De Oferta De Asistencia Técnica Territorial")
       st.write(" ")
       df_selection = df
      # st.download_button(label ='Descargar Oferta', data =df_selection)  
       numeroofertas=len(df_selection.index)
       texto2 = "Total oferta: " + str(numeroofertas)
       st.write(texto2)
       dfdescarga= df_selection.drop(['ObjetivoSinTilde', 'conteo'],axis=1)
       df_xlsx = to_excel(dfdescarga)
       st.download_button(label='📥 Descargar toda la oferta',
                                       data=df_xlsx ,
                                       file_name= 'Oferta.xlsx') 
       i=1

       for index, row in df_selection.iterrows():
           texto0= row['Nombre']+"-  " + row['NombreEntidad']
           texto1= row['Objetivo']+"  \n [Enlace oferta](" +row['PaginaWeb']+ ")"
           st.title(texto0)
           st.write(texto1)
           st.write(" ")
           i=i+1
    else :


        entidad = st.sidebar.multiselect(
            "Seleccione la Entidad:",
            options=dfentidad,
            #default=df["Entidad"].unique()
        )
        textofiltro=""
        if len(entidad)>0:
            textofiltro="Entidad == @entidad"
        
        sector = st.sidebar.multiselect(
            "Seleccione sector:",
            options=dfsector,
            #default=df["Entidad"].unique()
        )
        
        if len(sector)>0:
            if len(textofiltro)>0:
                textofiltro=textofiltro +" & Sector == @sector"
            else:
                textofiltro="Sector == @sector"
        
        capacidad = st.sidebar.multiselect(
            "Seleccione capacidad:",
            options=dfcapacidad,
            #default=df["Entidad"].unique()
        )
        if len(capacidad)>0:
            if len(textofiltro)>0:
                textofiltro=textofiltro +" & Capacidad == @capacidad"
            else:
                textofiltro="Capacidad == @capacidad"
                
        estrategia = st.sidebar.multiselect(
            "Seleccione estrategia:",
            options=dfestrategia,
            #default=df["Entidad"].unique()
        )
        
        if len(estrategia)>0:
            if len(textofiltro)>0:
                textofiltro=textofiltro +" & estrategia == @estrategia"
            else:
                textofiltro="estrategia == @estrategia"
                
        if TodaOfera ==  "Activar filtros":        
            st.title("Portafolio De Oferta De Asistencia Técnica Territorial")
            busqueda = st.text_input("Palabas claves de busqueda")
            a=0
            if TodaOfera ==  "Activar filtros":
                if len(textofiltro)>0:
                    df_selection = df.query(textofiltro)
                    a=1
                if len(busqueda)>0:
                    a=1
                    busqueda=busqueda.replace('á', 'a')
                    busqueda=busqueda.replace('é', 'e')
                    busqueda=busqueda.replace('í', 'i')
                    busqueda=busqueda.replace('ó', 'o')
                    busqueda=busqueda.replace('ú', 'u')
                    palabrasbusqueda= busqueda.split()
                    filtro=""
                    for i in range(len(palabrasbusqueda)):
                        palabra=palabrasbusqueda[i].strip()
                        if len(palabra)>2:
                            if len(filtro)>1:
                                filtro= filtro + "|"+palabra
                            else:
                                filtro= palabra
                                if len(textofiltro)>0:
                                    df_selection = df_selection[df_selection['ObjetivoSinTilde'].str.contains(filtro, na=False,case=False)]
                                else:
                                    df_selection = df[df['ObjetivoSinTilde'].str.contains(filtro, na=False,case=False)]
           
            if a==1:
                numeroofertas=len(df_selection.index)
                if numeroofertas>0:
                    texto2 = "Numero de ofertas encontradas: " + str(numeroofertas)
                    st.write(texto2)
                    dfdescarga= df_selection.drop(['ObjetivoSinTilde','conteo'],axis=1)
                    df_xlsx = to_excel(dfdescarga)
                    st.download_button(label='📥 Descargar actual resultado',data=df_xlsx ,file_name= 'Oferta.xlsx')
                    for index, row in df_selection.iterrows():
                        texto0= row['Nombre']+"-  " + row['NombreEntidad']
                        texto1= row['Objetivo']+"  \n [Enlace oferta](" +row['PaginaWeb']+ ")"
                        st.title(texto0)
                        st.write(texto1)
                        st.write(" ")
                else:
                    st.write("No se encontro ningún resultado con la busqueda realizada") 
        else:
            if len(textofiltro)>0:
                df_indicador = df.query(textofiltro)
            else:
                df_indicador=df
                
            st.title("Indicadores Oferta De Asistencia Técnica Territorial")    
            Entidades_by_noferta = (
            df_indicador.groupby(by=["Entidad"]).sum()[["conteo"]].sort_values(by="conteo"))
            fig_entidad_cantidad = px.bar(
            Entidades_by_noferta,
            x="conteo",
            y=Entidades_by_noferta.index,
            orientation="h",
            title="<b>Numero de oferta por entidad</b>",
            color_discrete_sequence=["#0083B8"] * len(Entidades_by_noferta),
            template="plotly_white",
            ) 
            fig_entidad_cantidad.update_layout( plot_bgcolor="rgba(0,0,0,0)",  xaxis=(dict(showgrid=False)) )  
            st.plotly_chart(fig_entidad_cantidad,use_container_width=True)   
            st.markdown("""---""")
        
            Sector_by_noferta = (
            df_indicador.groupby(by=["Sector"]).sum()[["conteo"]].sort_values(by="conteo"))
            fig_Sectord_cantidad = px.bar(
            Sector_by_noferta,
            x="conteo",
            y=Sector_by_noferta.index,
            orientation="h",
            title="<b>Numero de oferta por sector</b>",
            color_discrete_sequence=["#0083B8"] * len(Sector_by_noferta),
            template="plotly_white",
            ) 
            fig_Sectord_cantidad.update_layout( plot_bgcolor="rgba(0,0,0,0)",  xaxis=(dict(showgrid=False)) )  
            st.plotly_chart(fig_Sectord_cantidad,use_container_width=True)       
            st.markdown("""---""")
            
            Capacidad_by_noferta = (
            df_indicador.groupby(by=["Capacidad"]).sum()[["conteo"]].sort_values(by="conteo"))
            fig_capacidad_cantidad = px.bar(
            Capacidad_by_noferta,
            x="conteo",
            y=Capacidad_by_noferta.index,
            orientation="h",
            title="<b>Numero de oferta por capacidad</b>",
            color_discrete_sequence=["#0083B8"] * len(Capacidad_by_noferta),
            template="plotly_white",
            ) 
            fig_capacidad_cantidad.update_layout( plot_bgcolor="rgba(0,0,0,0)",  xaxis=(dict(showgrid=False)) )  
            st.plotly_chart(fig_capacidad_cantidad,use_container_width=True)       
            st.markdown("""---""")
        
            estrategia_by_noferta = (
            df_indicador.groupby(by=["estrategia"]).sum()[["conteo"]].sort_values(by="conteo"))
            fig_estrategia_cantidad = px.bar(
            estrategia_by_noferta,
            x="conteo",
            y=estrategia_by_noferta.index,
            orientation="h",
            title="<b>Numero de oferta por estrategia</b>",
            color_discrete_sequence=["#0083B8"] * len(estrategia_by_noferta),
            template="plotly_white",
            ) 
            fig_estrategia_cantidad.update_layout( plot_bgcolor="rgba(0,0,0,0)",  xaxis=(dict(showgrid=False)) )  
            st.plotly_chart(fig_estrategia_cantidad,use_container_width=True)    
        

                
            st.markdown("""---""")                    
    # ---- HIDE STREAMLIT STYLE ----
    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def model_prediction(pvariable, model):

    preds=model.predict([pvariable])

    return preds

def style_button_row(clicked_button_ix, n_buttons):
    def get_button_indices(button_ix):
        return {
            'nth_child': button_ix,
            'nth_last_child': n_buttons - button_ix + 1
        }

    clicked_style = """
    div[data-testid*="stHorizontalBlock"] > div:nth-child(%(nth_child)s):nth-last-child(%(nth_last_child)s) button {
        border-color: rgb(255, 75, 75);
        color: rgb(255, 75, 75);
        box-shadow: rgba(255, 75, 75, 0.5) 0px 0px 0px 0.2rem;
        outline: currentcolor none medium;
    }
    """
    unclicked_style = """
    div[data-testid*="stHorizontalBlock"] > div:nth-child(%(nth_child)s):nth-last-child(%(nth_last_child)s) button {
        pointer-events: none;
        cursor: not-allowed;
        opacity: 0.65;
        filter: alpha(opacity=65);
        -webkit-box-shadow: none;
        box-shadow: none;
    }
    """
    style = ""
    for ix in range(n_buttons):
        ix += 1
        if ix == clicked_button_ix:
            style += clicked_style % get_button_indices(ix)
        else:
            style += unclicked_style % get_button_indices(ix)
    st.markdown(f"<style>{style}</style>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
