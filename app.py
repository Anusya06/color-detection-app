import streamlit as st
from streamlit_drawable_canvas import st_canvas
import pandas as pd
import cv2
from PIL import Image
import numpy as np

st.set_page_config(page_title="Smart Color Detection Tool", layout="centered")
st.title("\U0001F3AF Smart Color Detection Tool")
st.markdown("Upload an image and click on any area to detect the nearest color name and RGB.")

@st.cache_data
def load_colors():
    df = pd.read_csv("colors.csv")
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=['R', 'G', 'B'])
    df = df[df['R'].apply(lambda x: str(x).isdigit())]
    df = df[df['G'].apply(lambda x: str(x).isdigit())]
    df = df[df['B'].apply(lambda x: str(x).isdigit())]
    df['R'] = df['R'].astype(int)
    df['G'] = df['G'].astype(int)
    df['B'] = df['B'].astype(int)
    return df

def get_closest_color_name(R, G, B, df):
    minimum = float('inf')
    cname = ""
    for i in range(len(df)):
        d = abs(R - df.loc[i, "R"]) + abs(G - df.loc[i, "G"]) + abs(B - df.loc[i, "B"])
        if d < minimum:
            minimum = d
            cname = df.loc[i, "color_name"]
    return cname

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    st.image(image, caption="\U0001F5BC Uploaded Image", use_column_width=True)

    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0.0)",
        stroke_width=1,
        stroke_color="#000000",
        background_image=image,
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="point",
        key="canvas",
    )

    if canvas_result.json_data is not None and len(canvas_result.json_data["objects"]) > 0:
        obj = canvas_result.json_data["objects"][-1]
        x = int(obj["left"])
        y = int(obj["top"])

        if 0 <= y < img_array.shape[0] and 0 <= x < img_array.shape[1]:
            pixel = img_array[y, x]
            R, G, B = int(pixel[0]), int(pixel[1]), int(pixel[2])
            df = load_colors()
            color_name = get_closest_color_name(R, G, B, df)

            st.markdown("---")
            st.subheader("\U0001F3A8 Detected Color Information")
            st.markdown(f"**Location:** ({x}, {y})")
            st.markdown(f"**RGB:** ({R}, {G}, {B})")
            st.markdown(f"**Closest Color Name:** \`{color_name}\`")
            st.markdown(
                f"<div style='width: 100px; height: 50px; background-color: rgb({R}, {G}, {B}); border: 1px solid #000'></div>",
                unsafe_allow_html=True
            )
