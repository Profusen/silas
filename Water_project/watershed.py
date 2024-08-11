import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from streamlit_option_menu import option_menu

img = Image.open('developers_institute LOGO.png')
st.set_page_config(page_title='SILAS WaterShed', page_icon=img)


selected = option_menu(
    menu_title="SILAS WaterShed Models",  # required
    options=["Home", "Help"],  # required
    icons=["house", "book"],  # optional
    menu_icon="water",  # optional
    default_index=0,  # optional
    orientation="horizontal",
)
flag = Image.open('watershed.jpeg')

# Function to calculate Time of Concentration using Sharifi & Razaz (2014)


def sharifi_razaz(area, dd):
    return 0.39 * (area ** 0.5) + (dd ** 2)


# Function to calculate Time of Concentration using Papadakis & Kazan (1986)
def papadakis_kazan(length, roughness, slope, intensity):
    return 0.66 * (length ** 0.5) * (roughness ** 0.52) * (slope ** -0.31) * (intensity ** -0.38)


# Initialize variables to store the time of concentration results
tc_sharifi_razaz = None
tc_papadakis_kazan = None

# Selection Box for Watershed Models
if selected == 'Home':
    st.title('Watershed Time of Concentration Calculator with Visualizations')
    st.image(flag, use_column_width=True)
    gpt_items = ['None', 'Sharifi & Razaz (2014) Model', 'Papadakis & Kazan (1986) Model']
    option_box = st.selectbox('**Select Models**', gpt_items)
    if option_box == 'None':
        st.info('Please select a Model to begin')

    # Sharifi & Razaz (2014) Model
    elif option_box == 'Sharifi & Razaz (2014) Model':
        st.header('Sharifi & Razaz (2014) Model')
        # Image Upload for Sharifi & Razaz (2014) Model
        image_sharifi = st.file_uploader("Upload Watershed Image for Sharifi & Razaz (2014) Model",
                                         type=["png", "jpg", "jpeg"], key='image_sharifi')

        if image_sharifi is not None:
            st.image(Image.open(image_sharifi), caption="Watershed Image - Sharifi & Razaz (2014)",
                     use_column_width=True)

        # Input Parameters for Sharifi & Razaz (2014)
        area = st.number_input("Enter Watershed Area (A) in square meters", min_value=0.0, key='area_sharifi')
        dd = st.number_input("Enter Watershed Diameter (DD) in meters", min_value=0.0, key='dd_sharifi')

        # Calculate Button for Sharifi & Razaz (2014)
        if st.button("Calculate Time of Concentration (Sharifi & Razaz)", key='calculate_sharifi'):
            if area and dd:
                tc_sharifi_razaz = sharifi_razaz(area, dd)
                st.write('')
                st.success(f"**Time of Concentration using Sharifi & Razaz (2014):** {tc_sharifi_razaz:.2f} hours")

                # Visualization
                fig, ax = plt.subplots(1, 2, figsize=(14, 6))

                # Distribution Plot for Area
                sns.histplot([area], kde=True, ax=ax[0])
                ax[0].set_title("Distribution of Watershed Area")

                # Line Plot showing relationship between Area and Time of Concentration
                area_values = pd.Series(range(1000, int(area) + 100000, 10000))
                tc_values = sharifi_razaz(area_values, dd)
                sns.lineplot(x=area_values, y=tc_values, ax=ax[1])
                ax[1].set_title("Area vs. Time of Concentration")
                ax[1].set_xlabel("Watershed Area (A)")
                ax[1].set_ylabel("Time of Concentration (hours)")

                st.pyplot(fig)
            else:
                st.warning('Fields cannot be empty, Please enter values for each field')

    # Papadakis & Kazan(1986) Model
    elif option_box == 'Papadakis & Kazan (1986) Model':
        st.header("Papadakis & Kazan (1986) Model")

        # Image Upload for Papadakis & Kazan (1986) Model
        image_papadakis = st.file_uploader("Upload Watershed Image for Papadakis & Kazan (1986) Model",
                                           type=["png", "jpg", "jpeg"], key='image_papadakis')

        if image_papadakis is not None:
            st.image(Image.open(image_papadakis), caption="Watershed Image - Papadakis & Kazan (1986)",
                     use_column_width=True)

        # Input Parameters for Papadakis & Kazan (1986)
        length = st.number_input("Enter Watershed Length (L) in meters", min_value=0.0, key='length_papadakis')
        roughness = st.number_input("Enter Surface Roughness (n)", min_value=0.0, key='roughness_papadakis')
        slope = st.number_input("Enter Watershed Slope (S) in meters per meter (m/m)", min_value=0.00,
                                key='slope_papadakis')
        intensity = st.number_input("Enter Rainfall Intensity (i) in mm/h", min_value=0.0,
                                    key='intensity_papadakis')

        # Calculate Button for Papadakis & Kazan (1986)
        if st.button("Calculate Time of Concentration (Papadakis & Kazan)", key='calculate_papadakis'):
            if length and roughness and slope and intensity:
                tc_papadakis_kazan = papadakis_kazan(length, roughness, slope, intensity)
                st.success(f"**Time of Concentration using Papadakis & Kazan (1986):** = {tc_papadakis_kazan:.2f} hours")

                # Visualization
                fig, ax = plt.subplots(2, 2, figsize=(14, 12))

                # Distribution Plot for Length
                sns.histplot([length], kde=True, ax=ax[0, 0])
                ax[0, 0].set_title("Distribution of Watershed Length")

                # Line Plot showing relationship between Length and Time of Concentration
                length_values = pd.Series(range(500, int(length) + 5000, 500))
                tc_values = papadakis_kazan(length_values, roughness, slope, intensity)
                sns.lineplot(x=length_values, y=tc_values, ax=ax[0, 1])
                ax[0, 1].set_title("Length vs. Time of Concentration")
                ax[0, 1].set_xlabel("Watershed Length (L)")
                ax[0, 1].set_ylabel("Time of Concentration (hours)")

                # Distribution Plot for Rainfall Intensity
                sns.histplot([intensity], kde=True, ax=ax[1, 0])
                ax[1, 0].set_title("Distribution of Rainfall Intensity")

                # Line Plot showing relationship between Intensity and Time of Concentration
                intensity_values = pd.Series(range(1, int(intensity) + 20, 1))
                tc_values_intensity = papadakis_kazan(length, roughness, slope, intensity_values)
                sns.lineplot(x=intensity_values, y=tc_values_intensity, ax=ax[1, 1])
                ax[1, 1].set_title("Rainfall Intensity vs. Time of Concentration")
                ax[1, 1].set_xlabel("Rainfall Intensity (i)")
                ax[1, 1].set_ylabel("Time of Concentration (hours)")

                st.pyplot(fig)
            else:
                st.warning('Fields cannot be empty, Please enter values for each field')
    st.write("")
    st.write("")
    # if st.checkbox('**Display Bar Chart Comparing Both Models**'):
    # Display Bar Chart Comparing Both Models
    if tc_sharifi_razaz is not None or tc_papadakis_kazan is not None:
        st.write('')
        st.write('')
        st.write("### Comparison of Time of Concentration Between Models")
        model_data = {
            'Model': ['Sharifi & Razaz (2014)', 'Papadakis & Kazan (1986)'],
            'Time of Concentration (hours)': [tc_sharifi_razaz, tc_papadakis_kazan]
        }
        model_df = pd.DataFrame(model_data)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='Model', y='Time of Concentration (hours)', data=model_df, ax=ax)
        ax.set_title("Comparison of Time of Concentration Between Models")

        st.pyplot(fig)
        #
        # else:
        #
        #     st.warning('Select a Model to work on')


elif selected == 'Help':
    # Main Area Instructions
    st.write("""
    ### Instructions:
    - Use the left sidebar to input parameters and calculate the time of concentration using the Sharifi & Razaz (2014) model.
    - Use the right sidebar to input parameters and calculate the time of concentration using the Papadakis & Kazan (1986) model.
    - You can upload images of the watershed related to each model for visualization.
    - After calculation, visualizations related to the parameters and results will be displayed.
    - A bar chart comparing the time of concentration calculated by both models will be displayed if both are calculated.
    """)


# Sidebar for




