# pre-check-data-integrity
This repo contains all the source code to build a docker image which includes a python script which performs the following functions.

- Accepts an input folder and generates a manifest file in JSON format which contains a list of every file in the folder along with an MD5 checksum of the file.
- Accepts an output folder and writes the manifest as well as log files.
- Accepts a manifest file and compares the newly generated manifest against this to test concordance between two folders.

## Inputs

--inputFolderPath [REQUIRED]
--outputFolderPath [REQUIRED]
--manifest [OPTIONAL]

## Running the Script Directly

Run the module "concordance.py" using the following command.

**python3 concordance.py --inputFolderPath {path to the input folder} --outputFolderPath {path to the output folder} --manifest {path to the comparison manifest file}**

### Running the Script Using Docker 

The default entrypoint in the Dockerfile is:

```
ENTRYPOINT ["python", "/concordance/concordance.py"]
```

1. docker pull docker-oncology.dockerhub.illumina.com/omniseq-pre-check-data-integrity:latest

2. `docker run -v {path of input folder}:/mount/inputs/input-folder/:ro -v {path of output folder}:/outputs/output-folder/:rw -v {path of comparison manifest file}:/mount/inputs/manifest.json:ro docker-oncology.dockerhub.illumina.com/omniseq-pre-check-data-integrity:latest --inputFolderPath /mount/inputs/input-folder/ --outputFolderPath /outputs/output-folder/ --manifest /mount/inputs/manifest.json`

## Output

The script generates the following files in the output folder;

* concordance-{}.json // The generated manifest file for the input folder
* concordance-{}.log // The log files from the script
