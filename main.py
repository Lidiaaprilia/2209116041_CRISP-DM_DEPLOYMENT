import streamlit as st
import pandas as pd
import plotly.express as px
import pickle

# Page configuration
st.set_page_config(
    page_title="World Happiness Report",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
url = 'https://raw.githubusercontent.com/Lidiaaprilia/Mini-Project-Data-Mining-2024/main/Checkpoint%20(3)%20-%20Data%20Preparation/Data%20Cleaned.csv'
df_file = pd.read_csv(url)

# Load data (without mapping, encoding, data reduction)
url = 'https://raw.githubusercontent.com/Lidiaaprilia/Mini-Project-Data-Mining-2024/main/Checkpoint%20(1)%20-%20Business%20Understanding/Dataset%20World%20Hapiness%20Report%202015.csv'
df = pd.read_csv(url)

# Sidebar
with st.sidebar:
    st.title('🌏 World Happiness Report Panel')

    selected_option = st.sidebar.radio('Select an option:', ['Dashboard', 'Visualization', 'Prediction'])

# Dashboard Main Panel
if selected_option == 'Dashboard':

    country_list = sorted(df_file['Country'].unique())
    selected_country = st.sidebar.selectbox('Select a country', country_list)
    df_selected_country = df_file[df_file['Country'] == selected_country]
    df_selected_country_sorted = df_selected_country.sort_values(by="Happiness Score", ascending=False)

    st.markdown("<h1 style='text-align: center;'>DASHBOARD MAIN PANEL</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align: justify;'>
        <h3>Explore Happiness Data</h3>
        <p>Gunakan menu dropdown di sidebar untuk memilih negara yang ingin ditampilkan datanya. 
        Data ini mencakup beberapa faktor yang berkontribusi terhadap skor kebahagiaan seperti tingkat ekonomi, 
        dukungan sosial (keluarga, dll), tingkat harapan hidup, tingkat kebebasan, tingkat kepercayaan terhadap pemerintah, dan tingkat kedermawanan.</p>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(df_selected_country_sorted,
             column_order=["Country", "Happiness Rank", "Happiness Score", "Economy (GDP per Capita)", "Family", "Health (Life Expectancy)", "Freedom", "Trust (Government Corruption)", "Generosity"],
             hide_index=True,
             width=None, 
             height=None 
            )
    selected_country_data = df_file[df_file['Country'] == selected_country]

    st.markdown("""
    <div style='text-align: justify;'>
        <h3>Understanding the Data</h3>
        
        - Country: Kolom ini berisi nama negara yang kita pilih di sidebar untuk ditampilkan datanya.
                
        - Happiness Rank: Kolom ini berisi nilai untuk mengetahui peringkat kebahagiaan negara berdasarkan skor kebahagiaan dari 158 negara yang ada di dataset.
                
        - Happiness Score: Kolom ini berisi skor kebahagiaan rata-rata suatu negara. 
                
        - Economy (GDP per Capita): Kolom ini berisi nilai untuk mengetahui seberapa besar kontribusi pendapatan per kapita negara terhadap perhitungan skor kebahagiaan.

        - Family: Kolom ini berisi nilai untuk mengetahui seberapa besar poin kontribusi kesejahteraan keluarga negara terhadap perhitungan skor kebahagiaan.
                
        - Health (Life Expectancy):  Kolom ini berisi nilai untuk mengetahui seberapa besar kontribusi poin harapan hidup negara terhadap perhitungan skor kebahagiaan.
                
        - Freedom: Kolom ini berisi nilai untuk mengetahui seberapa besar kontribusi poin kebebasan dalam berpendapat, memilih pilihan hidup negara terhadap perhitungan skor kebahagiaan.
                
        - Trust (Government Corruption): Kolom ini berisi nilai untuk mengetahui seberapa besar kontribusi poin tingkat korupsi negara terhadap perhitungan skor kebahagiaan.
                
        - Generosity: Kolom ini berisi nilai untuk mengetahui seberapa besar kontribusi poin kedermawanan negara terhadap perhitungan skor kebahagiaan.
    </div>
    """, unsafe_allow_html=True)

# Distribution Main Panel
if selected_option == 'Visualization':

    selected_option2 = st.sidebar.selectbox('Select a visualization:', ['Distribution', 'Relationship', 'Comparison', 'Composition'])

    if selected_option2 == 'Distribution':

        st.markdown("<h1 style='text-align: center;'>DISTRIBUTION MAIN PANEL</h1>", unsafe_allow_html=True)

        #Create Choropleth Map
        def make_choropleth(input_df, input_location, input_color, input_color_theme):
            choropleth = px.choropleth(input_df, 
                               locations=input_location, 
                               color=input_color, 
                               locationmode="country names",
                               color_continuous_scale=input_color_theme,
                               range_color=(0, max(input_df[input_color])),
                               labels={input_color:'Happiness Score'}
                              )
            choropleth.update_layout(
            template='plotly_dark'   
            )
            return choropleth
    
        choropleth = make_choropleth(df_file, 'Country', 'Happiness Score', px.colors.sequential.Inferno)
        st.plotly_chart(choropleth, use_container_width=True)

        # Display caption to guide users on hover
        st.caption(" Arahkan kursor ke suatu negara untuk mengetahui Skor Kebahagiaan negara tersebut.")

        with st.expander('Interpretasi dan Actionable Insights', expanded=True):
            st.write('''
            **Interpretasi:**
            - Peta dunia yang mewakili skor kebahagiaan di berbagai negara menggunakan skala warna. 
            Setiap negara diberi warna yang bervariasi sesuai dengan tingkat kebahagiaannya, dengan warna yang lebih terang menunjukkan skor kebahagiaan yang lebih tinggi dan warna yang lebih gelap menunjukkan skor kebahagiaan yang lebih rendah. 
            Dengan melihat peta ini, kita dapat dengan mudah melihat distribusi kebahagiaan di seluruh dunia dan membandingkan kebahagiaan antar negara.

            **Insight:**
            - Peta ini memberikan pandangan visual yang jelas tentang bagaimana kebahagiaan tersebar di seluruh dunia. 
            Kita dapat melihat dengan cepat negara-negara mana yang memiliki tingkat kebahagiaan yang tinggi dan rendah. 
            Mungkin kita akan melihat pola geografis di mana beberapa wilayah cenderung memiliki kebahagiaan yang lebih tinggi daripada yang lain, dan ini bisa menjadi bahan untuk analisis lebih lanjut tentang faktor-faktor apa yang mungkin memengaruhi tingkat kebahagiaan di wilayah-wilayah tersebut.

            **Actionable Insight:**
            - Identifikasi Pola: Identifikasi pola geografis di mana wilayah-wilayah tertentu cenderung memiliki tingkat kebahagiaan yang lebih tinggi atau lebih rendah. Ini dapat menjadi sasaran untuk studi lebih lanjut tentang faktor-faktor yang mempengaruhi kebahagiaan di wilayah-wilayah tersebut.
            - Fokus Intervensi: Negara-negara dengan skor kebahagiaan rendah dapat menjadi fokus untuk intervensi dan kebijakan yang ditujukan untuk meningkatkan kesejahteraan dan kebahagiaan masyarakatnya.
            - Pertimbangkan Faktor-Faktor: Analisis lebih lanjut dapat dilakukan untuk memahami faktor-faktor apa yang berkontribusi terhadap tingkat kebahagiaan yang berbeda di berbagai negara. Ini dapat membantu dalam merancang strategi yang lebih efektif untuk meningkatkan kebahagiaan dan kesejahteraan masyarakat secara keseluruhan.
            ''')

# Relationship Main Panel
    if selected_option2 == 'Relationship':

        st.markdown("<h1 style='text-align: center;'>RELATIONSHIP MAIN PANEL</h1>", unsafe_allow_html=True)

        # Create Heatmap Plot
        # Pilih kolom yang akan digunakan untuk korelasi
        selected_columns = ['Happiness Score', 'Economy (GDP per Capita)',
                    'Family', 'Health (Life Expectancy)', 'Freedom',
                    'Trust (Government Corruption)', 'Generosity']
        df_selected = df_file[selected_columns]

        # Buat heatmap korelasi dengan Plotly Express
        fig = px.imshow(df_selected.corr(), color_continuous_scale='agsunset')

        # Tampilkan heatmap di Streamlit
        st.plotly_chart(fig, use_container_width=True)

        # Display caption to guide users on hover
        st.caption("Arahkan kursor ke salah satu kotak dari heatmap untuk mengetahui tingkat korelasi di antara kedua variabel.")

        with st.expander('Interpretasi dan Actionable Insights', expanded=True):
            st.write('''
            **Interpretasi:**
            - Heatmap menampilkan tingkat korelasi antara dua variabel dalam dataset. 
            Setiap sel dalam heatmap mewakili korelasi antara dua variabel, dengan warna sel menunjukkan tingkat korelasi dan arah korelasi antar variabel. 
            Semakin terang warna selnya, semakin tinggi tingkat korelasinya, sementara semakin gelap warna selnya, semakin rendah tingkat korelasinya. 
            Misalnya, jika sel memiliki warna orange terang, itu menunjukkan tingkat korelasi yang tinggi antara dua variabel tersebut. 
            Sebaliknya, jika sel memiliki warna ungu gelap, itu menunjukkan tingkat korelasi yang rendah antara dua variabel tersebut.

            **Insight:**
            - Dari heatmap, dapat diamati bahwa variabel Happiness Score memiliki korelasi positif yang tinggi dengan variabel Economy (GDP per Capita). 
            Hal ini menunjukkan bahwa negara-negara dengan GDP per Capita yang tinggi cenderung memiliki skor kebahagiaan yang tinggi juga. 
            Di sisi lain, korelasi antara Happiness Score dan Generosity tergolong rendah, menunjukkan bahwa tingkat kedermawanan suatu negara tidak begitu berpengaruh terhadap skor kebahagiaannya.

            **Actionable Insight:**
            - Berdasarkan insight tersebut, pemerintah dan organisasi yang peduli terhadap kesejahteraan masyarakat dapat mempertimbangkan untuk fokus pada peningkatan faktor-faktor yang memiliki korelasi tinggi dengan skor kebahagiaan, 
            seperti perekonomian dan kesejahteraan ekonomi masyarakat. Selain itu, sumber daya juga bisa dialokasikan dengan lebih efisien dengan tidak terlalu memperhatikan faktor-faktor yang memiliki korelasi rendah dengan kebahagiaan, seperti tingkat kedermawanan.
            ''')

    # Comparison Main Panel
    if selected_option2 == 'Comparison':

        st.markdown("<h1 style='text-align: center;'>COMPARISON MAIN PANEL</h1>", unsafe_allow_html=True)

        # Create Bar chart horizontal
        # Mendapatkan daftar unik dari wilayah (Region)
        region_lists = list(df['Region'].unique())

        # Menghitung rasio kebahagiaan untuk setiap wilayah
        region_happiness_ratio = []
        for region in region_lists:
            region_data = df[df['Region'] == region]
            region_happiness_rate = region_data['Happiness Score'].sum() / len(region_data)
            region_happiness_ratio.append(region_happiness_rate)

        # Membuat DataFrame baru untuk menyimpan hasil perhitungan
        data = pd.DataFrame({'region': region_lists, 'region_happiness_ratio': region_happiness_ratio})

        # Mengurutkan wilayah berdasarkan rasio kebahagiaan
        sorted_region = data.sort_values(by='region_happiness_ratio', ascending=False)

        # Membuat bar chart dengan Plotly Express
        fig = px.bar(sorted_region, y='region', x='region_happiness_ratio',
             labels={'region_happiness_ratio': 'Region Happiness Ratio'}, width=800,
             color='region_happiness_ratio',
             color_continuous_scale='agsunset', orientation='h')

        # Mengatur label sumbu-y dan sumbu-x
        fig.update_yaxes(title='Region', tickangle=-45)
        fig.update_xaxes(title='Region Happiness Ratio')

        # Menampilkan grafik di Streamlit
        st.plotly_chart(fig, use_container_width=True)

         # Display caption to guide users on hover
        st.caption(" Arahkan kursor ke batang dari suatu wilayah/region untuk melihat Ratio Kebahagiaan wilayah tersebut.")

        with st.expander('Interpretasi dan Actionable Insights', expanded=True):
            st.write('''
            **Interpretasi:**
            - Bar chart horizontal menunjukkan rasio kebahagiaan untuk masing-masing wilayah. 
            Setiap batang mewakili satu wilayah, dengan tinggi batang menunjukkan seberapa tinggi rasio kebahagiaan wilayah tersebut. 
            Warna batang juga memberikan informasi tambahan, di mana warna yang lebih terang menandakan rasio kebahagiaan yang lebih tinggi, sedangkan warna yang lebih gelap menandakan rasio kebahagiaan yang lebih rendah.
                     
            **Insight:**
            - Perbedaan Kebahagiaan Antar Wilayah: Dari bar chart ini, terlihat adanya perbedaan signifikan dalam rasio kebahagiaan antar wilayah. Wilayah-wilayah seperti Australia dan New Zealand memiliki rasio kebahagiaan yang tinggi, sementara wilayah seperti Sub-Saharan Africa memiliki rasio kebahagiaan yang rendah.
            - Tren Regional: Terdapat pola atau tren regional dalam kebahagiaan, di mana wilayah-wilayah tertentu cenderung memiliki rasio kebahagiaan yang lebih tinggi daripada wilayah lainnya. Ini mungkin disebabkan oleh berbagai faktor seperti kondisi ekonomi, sosial, budaya, dan politik di setiap wilayah.
            - Kesimpulan Sosial: Dapat disimpulkan bahwa faktor-faktor yang mempengaruhi kebahagiaan masyarakat tidak merata di seluruh dunia. Hal ini menunjukkan bahwa ada potensi untuk meningkatkan kualitas hidup dan kebahagiaan di wilayah-wilayah dengan rasio kebahagiaan yang rendah.

            **Actionable Insight:**
            - Intervensi dan Pembangunan Wilayah: Pemerintah dan organisasi dapat menggunakan informasi ini untuk merancang program dan kebijakan yang lebih efektif untuk meningkatkan kebahagiaan dan kesejahteraan masyarakat di wilayah-wilayah dengan rasio kebahagiaan yang rendah.
            - Pengembangan Sumber Daya dan Infrastruktur: Investasi dalam pembangunan ekonomi, pendidikan, kesehatan, dan infrastruktur di wilayah-wilayah yang kurang bahagia dapat membantu meningkatkan kualitas hidup penduduk setempat.
            - Penggalakan Kesadaran dan Dukungan: Mendorong kesadaran akan pentingnya kesehatan mental, kehidupan sosial yang kuat, dan dukungan emosional di masyarakat dapat membantu mengurangi tingkat ketidakbahagiaan dan meningkatkan kesejahteraan secara keseluruhan.
            ''')

    # Composition Main Panel
    if selected_option2 == 'Composition':

        st.markdown("<h1 style='text-align: center;'>COMPOSITION MAIN PANEL</h1>", unsafe_allow_html=True)

        # Create Stacked Bar chart
        # Mendapatkan daftar unik dari wilayah (Region)
        region_lists = list(df['Region'].unique())

        # Inisialisasi list untuk menyimpan rata-rata nilai faktor-faktor kebahagiaan
        share_economy = []
        share_family = []
        share_health = []
        share_freedom = []
        share_trust = []
        share_generosity = []

        # Menghitung rata-rata faktor-faktor kebahagiaan untuk setiap wilayah
        for region in region_lists:
            region_data = df[df['Region'] == region]
            share_economy.append(region_data['Economy (GDP per Capita)'].mean())
            share_family.append(region_data['Family'].mean())
            share_health.append(region_data['Health (Life Expectancy)'].mean())
            share_freedom.append(region_data['Freedom'].mean())
            share_trust.append(region_data['Trust (Government Corruption)'].mean())
            share_generosity.append(region_data['Generosity'].mean())

        # Membuat DataFrame baru untuk menyimpan hasil perhitungan
        df_bar = pd.DataFrame({
            'Region': region_lists,
            'Economy': share_economy,
            'Family': share_family,
            'Health': share_health,
            'Freedom': share_freedom,
            'Trust': share_trust,
            'Generosity': share_generosity
        })

        # Membuat bar chart dengan Plotly Express
        fig = px.bar(df_bar, y='Region', x=['Economy', 'Family', 'Health', 'Freedom', 'Trust', 'Generosity'],
             barmode='stack',
             orientation='h',
             labels={'value': 'Percentage of Region', 'variable': 'Factors'},
             color_discrete_sequence=px.colors.qualitative.Plotly)

        # Menampilkan grafik di Streamlit
        st.plotly_chart(fig, use_container_width=True)

        # Display caption to guide users on hover
        st.caption(" Arahkan kursor ke warna dalam satu batang dari suatu wilayah/region untuk melihat faktor yang mempengaruhi kebahagiaan dari wilayah tersebut.")

        with st.expander('Interpretasi dan Actionable Insights', expanded=True):
            st.write('''
            **Interpretasi:**
            - Stacked bar chart tersebut memberikan visualisasi mengenai pengaruh variabel-variabel tertentu terhadap tingkat kebahagiaan di berbagai wilayah atau region. 
            Setiap batang mewakili satu wilayah, sedangkan bagian-bagian dari batang tersebut mewakili besaran nilai dari variabel-variabel seperti ekonomi, keluarga, kesehatan, kebebasan, kepercayaan, dan kemurahan hati. 
            Bagian yang lebih tinggi dari batang menunjukkan bahwa variabel tersebut memiliki pengaruh yang lebih besar terhadap tingkat kebahagiaan suatu wilayah.
                     
            **Insight:**
            - Dari stacked bar chart tersebut, dapat disimpulkan bahwa setiap wilayah memiliki faktor-faktor yang berbeda dalam memengaruhi tingkat kebahagiaannya. 
            Sebagai contoh, dalam wilayah Southern Asia, variabel Family memiliki pengaruh yang sangat signifikan terhadap tingkat kebahagiaan, sementara variabel Trust memiliki pengaruh yang lebih kecil. 
            Hal ini menunjukkan bahwa faktor dukungan sosial dari keluarga, kerabat, dan lingkungan sosial lainnya sangat penting dalam meningkatkan kebahagiaan penduduk di wilayah tersebut.
                     
            **Actionable Insight:**
            - Meningkatkan Dukungan Sosial: Pemerintah dan organisasi non-profit dapat bekerja sama untuk meningkatkan program-program yang mendukung keluarga, seperti pelayanan kesehatan mental, program pendidikan keluarga, dan layanan dukungan sosial lainnya.
            - Membangun Kepercayaan: Langkah-langkah untuk membangun kepercayaan antara masyarakat dengan pemerintah dan institusi lainnya dapat membantu meningkatkan kebahagiaan. Ini bisa dilakukan melalui transparansi, akuntabilitas, dan partisipasi masyarakat dalam proses pengambilan keputusan.
            - Mendorong Kemurahan Hati: Program-program untuk mendorong kemurahan hati dan kepedulian sosial dapat membantu menciptakan lingkungan yang lebih baik dan merangsang rasa kebahagiaan di masyarakat.
            ''')

# Prediction Main Panel
if selected_option == 'Prediction':
        
    st.subheader('Predicted Country Categories Based on Happiness Score Using KNN Algorithm')

    selected_country = st.selectbox('Select a country', sorted(df_file['Country'].unique()))

    # Prepare features for prediction
    selected_country_info = df_file[df_file['Country'] == selected_country]
    feature_cols = selected_country_info.columns.drop(['Country', 'Happiness Score Category'])

    # One-hot encoding for categorical features 
    selected_country_info = pd.get_dummies(selected_country_info, columns=['Country'])

    # Load pickled model
    with open('knn (1).pkl', 'rb') as file:
        knn_model = pickle.load(file)

    # Prepare features for prediction
    features = selected_country_info[feature_cols]

    # Predict Happiness Score Category when the button is clicked
    button = st.button('Predict Happiness Score Category')
    if button:
        # Predict happiness score category
        predicted_category = knn_model.predict(features)

        # Convert predicted category to text
        if predicted_category[0] == 1:
            category_text = "low"
        elif predicted_category[0] == 2:
            category_text = "middle"
        elif predicted_category[0] == 3:
            category_text = "high"
        else:
            category_text = "undefined"

        # Display predicted category
        st.write(f"Predicted Happiness Score Category for {selected_country} is {category_text}.")
