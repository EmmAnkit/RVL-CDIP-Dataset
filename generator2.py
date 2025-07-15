import os
import random
from datasets import load_dataset
from PIL import Image

def generate_rvl_pdfs(
    num_pdfs: int = 3,
    min_pages: int = 5,
    max_pages: int = 10,
    use_forms: bool = True,
    use_invoices: bool = True,
    use_letters: bool = True,
    max_samples: int = 5000,
    output_folder: str = "generated_rvl_pdfs"
):
    print("Loading RVL-CDIP dataset...")
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
        print(" No matching documents found.")
        return

    os.makedirs(output_folder, exist_ok=True)

    for i in range(num_pdfs):
        n_pages = random.randint(min_pages, max_pages)
        sampled = random.sample(filtered, n_pages)
        pages = [img.convert("RGB") for img, _ in sampled]
        types = [label for _, label in sampled]

        out_path = os.path.join(output_folder, f"doc_{i+1}.pdf")
        pages[0].save(out_path, save_all=True, append_images=pages[1:])
        print(f"Saved {out_path} ({n_pages} pages) with types: {dict((t, types.count(t)) for t in set(types))}")

    print(f"\n Done! {num_pdfs} PDFs saved to '{output_folder}'.")



generate_rvl_pdfs(
    num_pdfs=3,
    min_pages=10,
    max_pages=15,
    use_forms=True,
    use_invoices=True,
    use_letters=True,
    max_samples=3000,
    output_folder="test-folder"
)