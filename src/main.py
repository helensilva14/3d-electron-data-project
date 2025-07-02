import json

from utils.helpers import load_all_metadata_by_filename
from utils.metadata import consolidate_attribute_names

from datasets import empiar_11759, epfl_hippocampus, hemibrain_ng, jrc_mus_nacc, u2os_chromatin

def main():
    empiar_11759.run_tasks()
    epfl_hippocampus.run_tasks()
    hemibrain_ng.run_tasks()
    jrc_mus_nacc.run_tasks()
    u2os_chromatin.run_tasks()

    # Consolidate metadata from all datasets
    # print("Consolidating metadata from all datasets...")
    # consolidate_metadata()

def consolidate_metadata():
    JSON_METADATA_DIRECTORY = "outputs"
    CONSOLIDATED_METADATA_FILE = "docs/consolidated_metadata.json"

    all_metadata_loaded = load_all_metadata_by_filename(JSON_METADATA_DIRECTORY)
    print(f"Loaded {len(all_metadata_loaded)} metadata files from '{JSON_METADATA_DIRECTORY}' directory.")

    attribute_consolidation_results = consolidate_attribute_names(all_metadata_loaded)
    with open(CONSOLIDATED_METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(attribute_consolidation_results, f, indent=2)
        print(f"Consolidated metadata saved to {CONSOLIDATED_METADATA_FILE}")

if __name__ == "__main__":
    main()