import fitz # PyMuPDF library's import name
import re
from docling.document_converter import DocumentConverter # This import is not used in the provided script

def calculate_f1_score(ground_truth, extracted_data):
    """
    Calculates the F1-Score for extracted table cell data.
    """
    # Flatten both lists and remove None values for comparison
    ground_truth_set = set(str(item).strip().lower() for row in ground_truth for item in row if item is not None)
    extracted_set = set(str(item).strip().lower() for row in extracted_data for item in row if item is not None)

    true_positives = len(ground_truth_set.intersection(extracted_set))
    false_positives = len(extracted_set.difference(ground_truth_set))
    false_negatives = len(ground_truth_set.difference(ground_truth_set)) # Corrected: should be ground_truth_set.difference(extracted_set)

    # Corrected false_negatives calculation
    false_negatives = len(ground_truth_set.difference(extracted_set))


    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return f1_score, precision, recall

def parse_markdown_table_from_string(markdown_table_string):
    """
    Parses a Markdown table string into a list of lists.
    """
    lines = markdown_table_string.strip().split('\n')
    parsed_table = []

    # Iterate through the lines and parse each row
    for line in lines:
        # Skip the separator line (e.g., |---|---|)
        if line.strip().startswith('|') and not re.match(r'^\|[-: ]+\|([-: ]+\|)*$', line.strip()):
            row = [cell.strip() for cell in line.split('|')]
            # Clean up the row by removing empty strings from splitting on the end pipes
            row = [cell for cell in row if cell]
            parsed_table.append(row)
    
    # The header is the first line, and subsequent lines are data.
    # The separator line is now skipped by the regex above.
    return parsed_table

def main(file_path_pdf, file_path_md, page_number):
    """
    Main function to compare parsing methods and calculate metrics.
    """
    # --- 1. PyMuPDF Output (Raw Text) ---
    try:
        # Ensure the PDF path is correct for your environment
        doc = fitz.open("/Users/chhavishekhawat/Documents/google_10K.pdf") # Use the passed file_path_pdf
        page = doc.load_page(page_number - 1)
        pymupdf_output = page.get_text()
        print("=" * 50)
        print("  Method 1: Raw Text Output from PyMuPDF")
        print("=" * 50)
        print(pymupdf_output.strip())
        print("\n\n")

    except Exception as e:
        print(f"Error with PyMuPDF: {e}")
        return

    # --- 2. Docling Output (Structured Markdown) ---
    docling_output = []
    table_markdown_string = ""
    try:
        # Ensure the Markdown file path is correct for your environment
        with open("/Users/chhavishekhawat/Documents/goog-10-k-2024-docling.md", "r", encoding="utf-8") as md_file: # Use the passed file_path_md
            docling_markdown = md_file.read()

        # Regex to find the table within the larger section.
        # It now accounts for the descriptive paragraph between the heading and the table.
        table_regex = re.compile(
            r'#{1,6}\s*Issuer Purchases of Equity Securities\s*\n+'  # Matches heading (h1-h6)
            r'(?:.*?)\n+'                                          # Matches the descriptive paragraph and subsequent newlines (non-greedy)
            r'((?:\|.*?\n)+)'                                      # Captures the table lines (one or more lines starting with '|')
        )
        match = table_regex.search(docling_markdown)

        if match:
            # The entire table content is now in the first capturing group
            table_markdown_string = match.group(1).strip()
            docling_output = parse_markdown_table_from_string(table_markdown_string)

        print("=" * 50)
        print("  Method 2: Structured Table from Docling (as Markdown)")
        print("=" * 50)
        if table_markdown_string:
            print(table_markdown_string)
        else:
            print("Docling did not find the specified table.")
        print("\n\n")

    except Exception as e:
        print(f"Error with Docling: {e}")
        return

    # --- 3. Ground Truth & Metrics Calculation ---
    # Manually defined ground truth for the "Issuer Purchases..." table on page 28
    # Adjusted to match the actual markdown table structure with separate 'Average Price Paid' columns
    cleaned_ground_truth = [
        ['Period', 'Total Number of Class A Shares Purchased (in thousands) (1)', 'Total Number of Class C Shares Purchased (in thousands) (1)', 'Average Price Paid per Class A Share (2)', 'Average Price Paid per Class C Share (2)', 'Total Number of Shares Purchased as Part of Publicly Announced Programs (in thousands) (1)', 'Approximate Dollar Value of Shares that May Yet Be Purchased Under the Program (in millions)'],
        ['October 1 - 31', '5,792', '30,080', '$ 167.66', '$ 168.84', '35,872', '$ 53,699'],
        ['November 1 - 30', '4,325', '22,450', '$ 174.97', '$ 175.98', '26,775', '$ 49,023'],
        ['December 1 - 31', '3,559', '19,572', '$ 187.07', '$ 187.52', '23,131', '$ 44,704'],
        ['Total', '13,676', '72,102', '', '', '85,778', ''] # Empty strings for the blank cells
    ]

    print("=" * 50)
    print("  Comparison Metrics")
    print("=" * 50)
    if docling_output:
        f1_score, precision, recall = calculate_f1_score(cleaned_ground_truth, docling_output)
        print(f"F1-Score: {f1_score:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
    else:
        print("Docling failed to extract the table to calculate metrics.")

if __name__ == "__main__":
    # IMPORTANT: Update these paths to your actual file locations
    file_to_analyze_pdf = "/Users/chhavishekhawat/Documents/google_10K.pdf" # Original path from your script
    file_to_analyze_md = "/Users/chhavishekhawat/Documents/goog-10-k-2024-docling.md" # Original path from your script
    page_with_table = 28 # Refer to the PDF's page number
    main(file_to_analyze_pdf, file_to_analyze_md, page_with_table)