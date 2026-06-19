from pypdf import PdfReader, PdfWriter

def remove_pages(input_pdf, output_pdf, pages_to_remove):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    
    # Iterate using zero-based indexing (Page 1 is index 0)
    for index, page in enumerate(reader.pages):
        if index not in pages_to_remove:
            writer.add_page(page)
            
    with open(output_pdf, "wb") as f:
        writer.write(f)

# Example: Remove the 2nd and 4th pages (indices 1 and 3)
remove_pages("input.pdf", "output.pdf", [1, 3])
