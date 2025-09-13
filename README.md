# Document Parsing with Python: A Docling vs. PyMuPDF Comparison

This repository contains a Python script that compares two different approaches for extracting structured data from PDF documents:

1. **PyMuPDF:** A low-level, high-performance library for raw text and image extraction.

2. **Docling:** An AI-powered library designed to understand and preserve the logical structure of a document, including tables and figures.

The script evaluates the performance of each method on a specific table from a publicly available Google 10-K report, providing clear metrics to demonstrate the strengths and weaknesses of each approach.

## Features

* **Raw Text Extraction:** Demonstrates how to get raw, unstructured text from a PDF page using PyMuPDF.

* **Structured Table Extraction:** Shows how to use `docling` to intelligently recognize and extract a table, converting it into a structured Markdown format.

* **F1-Score Metrics:** Includes functions to calculate F1-Score, Precision, and Recall to objectively compare the two parsing methods.

* **Step-by-Step Breakdown:** The code is structured to be run interactively for educational purposes, with clear print statements at each stage.

## How to Run the Code

### 1. Prerequisites

First, you need to install the necessary Python libraries. It is highly recommended to use a virtual environment.

### 2. Document Setup

Download the Google 10-K report from the SEC website or a similar source and save it as `google_10K.pdf` in a location on your system.

* **Note:** You must update the `file_path_pdf` variable in the script to the correct path on your machine.

### 3. Run the Script

Run the `document_parsing.py` script from your terminal:
The script will print the raw text output from PyMuPDF, the structured Markdown output from Docling, and the final performance metrics for both.

## Interpreting the Results

The metrics printed by the script provide a clear picture of each method's performance:

**F1-Score:** The weighted average of Precision and Recall. A score closer to `1.0` is better.
**Precision:** The percentage of correctly extracted data points out of all data points extracted.
**Recall:** The percentage of all correct data points that were successfully extracted.

| **Method** | **F1-Score** | **Precision** | **Recall** | 
| ----- | ----- | ----- | ----- | 
| **Docling** | High (\~0.98) | High (1.00) | High (\~0.97) | 
| **PyMuPDF (Regex-based)** | Low (\~0.53) | High (1.00) | Low (\~0.36) | 

As shown, Docling's high F1-Score and Recall indicate its superior ability to find and correctly extract all the structured data, demonstrating the value of AI-powered document understanding. The manual PyMuPDF approach, while precise in what it found, missed a significant portion of the data due to the inherent complexity and variability of PDF formatting.
