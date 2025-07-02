import json
import pandas as pd

from datasets import empiar_11759, epfl_hippocampus, hemibrain_ng, jrc_mus_nacc, u2os_chromatin
from utils.helpers import load_all_metadata_by_filename
from utils.metadata import consolidate_categories

JSON_METADATA_DIRECTORY = "outputs"
CONSOLIDATED_METADATA_FILE = "docs/consolidated_metadata.json"
CATEGORIES_TABLE_FILE = "docs/categories_in_multiple_datasets_table.html"

def main():
    empiar_11759.run_tasks()
    epfl_hippocampus.run_tasks()
    hemibrain_ng.run_tasks()
    jrc_mus_nacc.run_tasks()
    u2os_chromatin.run_tasks()

    print("\nAll datasets processed. Now consolidating metadata...")
    consolidate_metadata()

def consolidate_metadata():
    """Consolidates metadata from all datasets into a single JSON file.
    This function loads metadata from the specified directory,
    consolidates the top-level categories, and saves the results to a JSON file.
    """
    all_metadata_loaded = load_all_metadata_by_filename(JSON_METADATA_DIRECTORY)
    consolidation_results = consolidate_categories(all_metadata_loaded)
    with open(CONSOLIDATED_METADATA_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(consolidation_results, json_file, indent=2)
        print(f"Consolidated metadata saved to {CONSOLIDATED_METADATA_FILE}")

    df = pd.DataFrame.from_dict(consolidation_results['categories_in_multiple_datasets'])
    with open(CATEGORIES_TABLE_FILE, "w", encoding="utf-8") as html_file:
        html_file.write(df.sort_values(by='category_name').to_html(index=False))

if __name__ == "__main__":
    main()