import streamlit as st
import pandas as pd
import math
from io import BytesIO

st.title("Application de Remplacement d'Articles")

# Téléchargement des fichiers Excel
uploaded_file1 = st.file_uploader("Choisissez le fichier négatif", type="xlsx")
uploaded_file2 = st.file_uploader("Choisissez le fichier positif", type="xlsx")

if uploaded_file1 and uploaded_file2:
    df1 = pd.read_excel(uploaded_file1)
    df2 = pd.read_excel(uploaded_file2)
    
    messages_de_remplacement = []

    for index_neg, row_neg in df1.iterrows():
        a = abs(int(row_neg['Nombre_Maximal']))
        d = math.floor(row_neg['Prix_Negatif'] * 1000) / 1000
        nega = row_neg['naga']

        while a > 0 and not df2.empty:
            solution_trouvee = False
            for i in range(len(df2)):
                c = math.floor(df2.loc[i, 'Prix_Positif'] * 1000) / 1000
                valeur_achat = df2.loc[i, 'achat']
                posi = df2.loc[i, 'posi']

                montant = a * d
                totale = montant / c

                solutions = []
                for j in range(1, a + 1):
                    new_total = j * d / c
                    if new_total.is_integer():
                        solutions.append((j, new_total))

                if solutions:
                    selected_solution = max(filter(lambda x: x[1] < valeur_achat, solutions), key=lambda x: x[1], default=None)
                    if selected_solution:
                        remplacement_msg = f'{nega} est remplacé par {posi} par une quantité de {selected_solution[1]}'
                        messages_de_remplacement.append(remplacement_msg)

                        a -= selected_solution[0]
                        df2.loc[i, 'achat'] -= selected_solution[1]

                        if df2.loc[i, 'achat'] == 0:
                            df2.drop(i, inplace=True)
                            df2.reset_index(drop=True, inplace=True)

                        solution_trouvee = True
                        break

            if not solution_trouvee:
                break

        df1.loc[index_neg, 'Nombre_Maximal'] = -a

    if messages_de_remplacement:
        st.write("Messages de remplacement :")
        for msg in messages_de_remplacement:
            st.write(msg)
    else:
        st.write("Aucun message de remplacement trouvé.")

    # Sauvegarde des fichiers Excel dans des buffers
    buffer1 = BytesIO()
    df1.to_excel(buffer1, index=False)
    buffer1.seek(0)

    buffer2 = BytesIO()
    df2.to_excel(buffer2, index=False)
    buffer2.seek(0)

    # Boutons de téléchargement pour les fichiers Excel mis à jour
    st.download_button(
        label="Télécharger le fichier des articles négatifs mis à jour",
        data=buffer1,
        file_name="negatiffinal1_mise_a_jour.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.download_button(
        label="Télécharger le fichier des articles positifs mis à jour",
        data=buffer2,
        file_name="positiffinal1_mise_a_jour.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    st.write("Calculs terminés et fichiers mis à jour.")
