from download.epfl_dataset import download_epfl, extract_metadata

def main():
    download_epfl()
    extract_metadata()


if __name__ == "__main__":
    main()