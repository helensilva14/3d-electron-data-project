from download import epfl_dataset, hemibrain_ng_dataset, u2os_chromatin_dataset, jrc_mus_nacc_dataset, empiar_11759_dataset

def main():
    # empiar_11759_dataset.run_tasks()
    # epfl_dataset.run_tasks()
    # hemibrain_ng_dataset.run_tasks()
    jrc_mus_nacc_dataset.run_tasks()
    # u2os_chromatin_dataset.run_tasks()

    # TODO: Consolidate all metadata files into a single JSON file

if __name__ == "__main__":
    main()