# Standard library imports
import sys
import os
import json
import logging
import argparse
import hashlib
from datetime import datetime

def main():
    concordance = Concordance()
    retval = concordance.run()
    sys.exit(retval)

class Concordance(object):
    """Data Integrity Pre-Check for Folder Concordance"""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    def run(self):
        exit_code = 0
        args = self.parse_args(sys.argv[1:])
        output_directory = self.create_output_directory(args.outputFolderPath)
        self.set_logger_output(output_directory)
        self.log_arguments(args)
        manifest = self.generate_manifest(args.inputFolderPath)
        self.write_manifest(manifest, args.outputFolderPath)
        if args.manifest:
            exit_code = self.compare_manifests(manifest, args.manifest)
        self.logger.info('************** End Concordance *************')
        return exit_code

    def create_output_directory(self, outputFolder):
        self.logger.info("Creating output directory")

        # if os.path.isdir(outputFolder):
        #     raise ValueError("I/O error: Output folder already exists {0}".format(outputFolder))

        try:
            if not os.path.isdir(outputFolder):
                os.makedirs(outputFolder)
        except IOError as e:
            msg = "I/O error({0}): {1}: Output Directory {2}".format(e.errno, e.strerror, outputFolder)
            self.logger.error(msg, exc_info=True)
            raise IOError(msg)

        return outputFolder

    def parse_args(self, args):
        parser = argparse.ArgumentParser(description="Data Integrity Pre-Check for Folder Concordance")
        parser.add_argument('--outputFolderPath', type=str, required=True, help="The path to the output folder.")
        parser.add_argument('--inputFolderPath', type=str, required=True, help="The path to the input folder.")
        parser.add_argument('--manifest', type=str, help="The path to a manifest on which to compare concordance.")
        return parser.parse_args(args)

    def set_logger_output(self, output_directory):

        # create a file handler
        log_file = os.path.join(output_directory,
                                "{0}-{1}.log".format("concordance", datetime.utcnow().strftime("%Y%m%d%H%M%S")))
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.INFO)

        # create a logging format
        formatter = logging.Formatter('%(asctime)s  %(levelname)s  %(message)s', "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)

        # add the handlers to the logger
        self.logger.addHandler(handler)
        self.logger.info('************** Start Concordance *************')

    def log_arguments(self, args):
        self.logger.info("Command line arguments: " + str(args))

    def generate_manifest(self, input_directory):

        #BLOCKSIZE = 65536

        self.logger.info('Generating a new manifest for input directory: ' + input_directory)

        # create dictionary to store md5 hashes per file
        manifestDict = dict()

        # recursively iterate through all files in input directory and calculate md5 hash
        # r=root, d=directories, f = files
        for r, d, f in os.walk(input_directory):
            for file in f:
                hasher = hashlib.md5()
                with open(os.path.join(r, file), 'rb') as afile:
                    #buf = afile.read(BLOCKSIZE)
                    buf = afile.read()
                    hasher.update(buf)
                    # while len(buf) > 0:
                    #     hasher.update(buf)
                    #     buf = afile.read(BLOCKSIZE)
                md5 = hasher.hexdigest()
                manifestDict[os.path.join(r, file)] = md5

        return manifestDict
        
    def write_manifest(self, manifestDict, output_directory):

        # create a new manifest file
        manifest_file = os.path.join(output_directory, "{0}-{1}.json".format("concordance", datetime.utcnow().strftime("%Y%m%d%H%M%S")))

        self.logger.info('Writing new manifest to: ' + manifest_file)
        
        # write manifest
        with open(manifest_file, 'w') as json_file:
            json.dump(manifestDict, json_file)
    
    def compare_manifests(self, generated_manifest, input_manifest_file):

        self.logger.info('Comparing manifest to ' + input_manifest_file)

        f = open(input_manifest_file)
        input_manifest = json.load(f)
        f.close()

        d1 = input_manifest
        d2 = generated_manifest

        d1_keys = set(input_manifest.keys())
        d2_keys = set(generated_manifest.keys())
        
        intersect_keys = d1_keys.intersection(d2_keys)
        added = d2_keys - d1_keys
        removed = d1_keys - d2_keys
        modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
        
        exit_code = 0
        if bool(added):
            exit_code = 3
            self.logger.info('The following keys were added in the generated manifest as compared to the input manifest:')
            self.logger.info(added)

        if bool(removed):
            exit_code = 4
            self.logger.info('The following keys were removed in the generated manifest as compared to the input manifest:')
            self.logger.info(removed)

        if bool(modified):
            exit_code = 5
            self.logger.info('The following values were modified in the generated manifest as compared to the input manifest:')
            self.logger.info(modified)

        if exit_code == 0:
            self.logger.info('The manifests are identical')

        return exit_code

if __name__ == "__main__":
    main()
