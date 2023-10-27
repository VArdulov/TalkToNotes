"""
This script is designed to process example transcripts from yt-dlp into a cleaner format that I think will be condusive
to indexing and querying later
"""
from os import path, listdir
from talktonotes.data.transcripts import YTDLPTranscript
if __name__ == "__main__":

    source_destination_directories = {
        "../data/convex_optimization/transcripts": "../processed_data/convex_optimization/transcripts",
        "../data/linear_dynamical_systems/transcripts": "../processed_data/linear_dynamical_systems/transcripts",
        "../data/intro_to_artificial_intelligence/transcripts": "../processed_data/intro_to_artificial_intelligence/transcripts"
    }

    for sd, dd in source_destination_directories.items():
        print(f"Processing files from {sd}\t-to->{dd}")
        yt_dlp_vtt_files = [f for f in listdir(sd) if f.endswith(".vtt")]
        yt_dlp_vtt_objs = [YTDLPTranscript(filename=path.join(sd, f), keep_timing=True)for f in yt_dlp_vtt_files]
        for f, yt_dlp_vtt in zip(yt_dlp_vtt_files, yt_dlp_vtt_objs):
            nf = f.split(".")[0]+".txt"
            yt_dlp_vtt.to_text(path.join(dd, nf))
