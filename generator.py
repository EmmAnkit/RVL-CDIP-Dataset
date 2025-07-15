import streamlit as st
from datasets import load_dataset
from PIL import Image
import os
import random

st.set_page_config(page_title="Document Generator", layout="centered")

st.markdown("""
<div style='text-align: center;'>
    <h1>Document Generator</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
col1, col2, col3 = st.columns(3)
num_pdfs = col1.number_input("Number of PDFs", min_value=1, max_value=20)
min_pages = col2.number_input("Min Pages", min_value=1, max_value=50)
max_pages = col3.number_input("Max Pages", min_value=min_pages, max_value=100,)

st.markdown("---")
col4, col5, col6 = st.columns(3)
use_forms = col4.checkbox("Forms", value=True)
use_invoices = col5.checkbox("Invoice", value=False)
use_letters = col6.checkbox("Letters", value=True)

st.markdown("---")
max_samples = st.slider("RVL-CDIP Sample Size", 1000, 10000, 5000, step=1000)

st.markdown("---")

col_out1, col_out2 = st.columns([2, 1])
output_folder = col_out1.text_input("Output Folder Name", value="streamlit_rvl_docs")
generate = col_out2.button("🚀 Generate")

if generate:
    st.info("Loading dataset...")
    ds = load_dataset("rvl_cdip", split=f"train[:{max_samples}]", trust_remote_code=True)

    label_map = {
            0: "letter", 1: "form", 2: "email", 3: "handwritten",
            4: "advertisement", 5: "scientific_report", 6: "scientific_publication",
            7: "specification", 8: "file_folder", 9: "news_article",
            10: "budget", 11: "invoice", 12: "presentation",
            13: "questionnaire", 14: "resume", 15: "memo"
        }

    allowed_labels = []
    if use_letters: allowed_labels.append(0)
    if use_forms: allowed_labels.append(1)
    if use_invoices: allowed_labels.append(11)

    filtered = [(item["image"], label_map[item["label"]])
                for item in ds if item["label"] in allowed_labels]

    if not filtered:
        st.error("No matching documents found in the selected subset.")
    else:
        os.makedirs(output_folder, exist_ok=True)
        generated_paths = []

        for i in range(num_pdfs):
            n_pages = random.randint(min_pages, max_pages)
            sampled = random.sample(filtered, n_pages)
            pages = [img.convert("RGB") for img, _ in sampled]
            types = [label for _, label in sampled]

            out_path = os.path.join(output_folder, f"doc_{i+1}.pdf")
            pages[0].save(out_path, save_all=True, append_images=pages[1:])
            generated_paths.append(out_path)

            with st.expander(f"📄 Document {i+1} - {n_pages} pages"):
                st.write("Includes:")
                for t in set(types):
                    st.write(f"- {t}: {types.count(t)} pages")
                st.download_button("⬇️ Download PDF", data=open(out_path, "rb").read(), file_name=f"doc_{i+1}.pdf")

        st.success(f"🎉 Generated {num_pdfs} PDFs in '{output_folder}'")
