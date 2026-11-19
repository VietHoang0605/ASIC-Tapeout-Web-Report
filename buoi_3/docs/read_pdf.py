import pypdf
import os

pdf_path = '/mnt/d/Tapeout_chip/buoi_3/bài giảng và Lab/Tapeout_LAB2.pdf'
reader = pypdf.PdfReader(pdf_path)
print(f"Total pages: {len(reader.pages)}")
for i, page in enumerate(reader.pages):
    txt = page.extract_text() or ""
    print(f"=== PAGE {i+1} ===")
    print(txt[:600])
