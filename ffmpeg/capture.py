import argparse
import os
import subprocess

class FramesExtractor:
    def __init__(self, output):
        self.output = output

    def extract_frames(self, input, fps):
        output = input.split('/')[-1].split('.')[0]

        if not os.path.exists(self.output + output):
            os.makedirs(self.output + output)

        query = "ffmpeg -i " + input + " -vf fps=" + str(fps) + " " + self.output + output + "/output%06d.png"
        response = subprocess.Popen(query, shell=True, stdout=subprocess.PIPE).stdout.read()
        s = str(response).encode('utf-8')

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True)
ap.add_argument("-o", "--output", required=True)
ap.add_argument("-f", "--fps", required=True)
args = vars(ap.parse_args())

input = args["input"]
output = args["output"]
fps = args["fps"]

videoFE = FramesExtractor(output)
videoFE.extract_frames(input,fps)