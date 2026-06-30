import sys
from pypdf import PdfReader, PdfWriter

def book_merge(file_a_path: str, file_b_path: str, output_path: str = "merged_output.pdf"):
    """
    Merges two PDFs by interleaving their pages.
    Pattern: a1, a2, b1, a3, b2, a4, b3...
    """
    writer = PdfWriter()
    
    # Read both PDF files
    reader_a = PdfReader(file_a_path)
    reader_b = PdfReader(file_b_path)
    
    pages_a = reader_a.pages
    pages_b = reader_b.pages
    
    len_a = len(pages_a)
    len_b = len(pages_b)
    
    idx_a = 0
    idx_b = 0
    
    # 1. Handle the initial special sequence: a1, a2
    if idx_a < len_a:
        writer.add_page(pages_a[idx_a])
        idx_a += 1
    if idx_a < len_a:
        writer.add_page(pages_a[idx_a])
        idx_a += 1
        
    # 2. Interleave the remaining pages: b1, a3, b2, a4...
    while idx_a < len_a or idx_b < len_b:
        # Add page from B if available
        if idx_b < len_b:
            writer.add_page(pages_b[idx_b])
            idx_b += 1
            
        # Add page from A if available
        if idx_a < len_a:
            writer.add_page(pages_a[idx_a])
            idx_a += 1

    # Save the result to a file
    with open(output_path, "wb") as output_file:
        writer.write(output_file)
        
    print(f"Successfully merged into {output_path}")

# Example Usage:
# book_merge("document_A.pdf", "document_B.pdf", "interleaved_book.pdf")
def main():
    if len(sys.argv) < 4:
        print("Usage: python merge.py input1.pdf input2.pdf ... output.pdf")
        sys.exit(1)

    *inputs, output = sys.argv[1:]

    merger = PdfWriter()

    for pdf in inputs:
        merger.append(pdf)

    merger.write(output)
    merger.close()

    print(f"Merged {len(inputs)} files into '{output}'")

if __name__ == "__main__":
    # main()
    book_merge



