"""
This files will contain classes and helper methods for preprocessing the transcript data
"""
import json
from os import path

YT_DLP_START_INDEX = 8
YT_DLP_TIMING_NEXT_INDEX_OFFSET = 8
YT_DLP_TIMING_TEXT_OFFSET = 1


class Transcript:

    def __init__(self):
        pass


class StringTranscript(Transcript):

    def __init__(self, content):
        super().__init__()
        self.text = content

    def to_dict(self):
        return dict({"text": self.text})

    def to_json(self, filename:str):
        obj = self.to_dict()
        with open(filename, "w") as json_file:
            json.dump(obj, json_file)

    def to_text(self, filename:str):
        with open(filename, "w") as out_file:
            out_file.write(self.text)


class YTDLPTranscript(StringTranscript):

    def __init__(
            self,
            filename: str,
            keep_timing:bool = False
    ):
        self.filename = filename
        self.timing = keep_timing
        content = self.__import_text()
        super().__init__(content)

    def __import_text(self):
        assert path.isfile(self.filename), f"{self.filename} was not found!"
        lines = []
        with open(self.filename, "r") as vtt_file:
            lines = vtt_file.readlines()

        timings = []
        text = []
        for line_index in range(YT_DLP_START_INDEX, len(lines), YT_DLP_TIMING_NEXT_INDEX_OFFSET):
            timings.append(lines[line_index].strip())
            text.append(lines[line_index + YT_DLP_TIMING_TEXT_OFFSET].strip())

        # if we want to keep the time step
        if self.timing:
            text = [f"<timing=\"{timing}\"\\> {text}" for text, timing in zip(text, timings)]

        return "\n".join(text)

    # To-do: change it so it returns array of timing and content
    # def to_dict(self, filename:str=None):


