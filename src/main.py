from datasets import empiar_11759, epfl_hippocampus, hemibrain_ng, jrc_mus_nacc, u2os_chromatin

def main():
    empiar_11759.run_tasks()
    epfl_hippocampus.run_tasks()
    hemibrain_ng.run_tasks()
    jrc_mus_nacc.run_tasks()
    u2os_chromatin.run_tasks()

    # TODO: Consolidate all metadata files into a single JSON file

if __name__ == "__main__":
    main()