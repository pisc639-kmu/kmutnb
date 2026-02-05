import sys
from pypdf import PdfWriter

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
    main()
