import pandas as pd
import json

def combine_features(row):
    """
    Combines the 'Summary' and 'Text' columns into a single text field.
    """
    try:
        return row['Summary'] + " " + row["Text"]
    except Exception as e:
        print("Error:", e)

def process_reviews_csv(input_file, output_file):
    """
    Processes a reviews CSV file to create a Vespa-compatible JSONL format.

    Args:
      input_file (str): Path to the input CSV file with reviews data.
      output_file (str): Path to the output JSON file in Vespa-compatible format.

    Workflow:
      1. Reads a sample of 10,000 rows from the CSV file.
      2. Combines 'Summary' and 'Text' columns for the 'text' field.
      3. Renames columns to 'doc_id', 'title', and 'text' for Vespa compatibility.
      4. Constructs a JSON-like 'fields' column for each record's data.
      5. Creates a 'put' column based on 'doc_id' for unique document identification.
      6. Outputs to a JSON file with `orient='records'` and `lines=True` to ensure JSONL format.

    Example Usage:
      >>> process_reviews_csv("Reviews.csv", "output_reviews.json")
    """
    # Load the data and sample 10,000 rows
    reviews = pd.read_csv(input_file).sample(n=10000, random_state=1)

    # Fill missing values in 'Summary' and 'Text' columns
    reviews['Summary'] = reviews['Summary'].fillna('')
    reviews['Text'] = reviews['Text'].fillna('')

    # Create the 'text' column by combining 'Summary' and 'Text'
    reviews["text"] = reviews.apply(combine_features, axis=1)

    # Select and rename columns for Vespa
    reviews = reviews[['Id', 'Summary', 'text']]
    reviews.rename(columns={'Summary': 'title', 'Id': 'doc_id'}, inplace=True)

    # Create 'fields' column as JSON-like structure for each record
    reviews['fields'] = reviews.apply(lambda row: row.to_dict(), axis=1)

    # Create 'put' column based on 'doc_id'
    reviews['put'] = reviews['doc_id'].apply(lambda x: f"id:review-search:doc::{x}")

    # Select only 'put' and 'fields' columns for final output
    df_result = reviews[['put', 'fields']]

    # Save to JSONL format
    df_result.to_json(output_file, orient='records', lines=True)


process_reviews_csv("Reviews.csv", "output_reviews.jsonl")
