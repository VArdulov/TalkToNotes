*by Victor Ardulov*

## Description

Large Language Models (LLMs) provide a couple of really great features for analyzing and processing large amounts of text data. In particular for this project I'm interested in designing a RAG based system that can utilize `llama_index` in order to index and interactively search and respond with information derived from *class notes* . The hope is that maybe this can create an interface for students to ingest their own course notes along with any material provided in class, such as recording transcripts, lecture slides, and supporting material.

## Usage

**To-Do**:  Ideally, I could see this existing primarily as a web interface, but maybe it would make sense as an [Electron](https://www.electronjs.org/docs/latest/tutorial/tutorial-first-app)application for desktop execution as well. I think some intermediate command-line functionality might make sense as well. 

My two ideas are to containerize this so that it can be easily deployed across multiple environments, or instead build a back-end with an API layer using something like 
## Work Log

#### October 23 2023

* I initialized the project, I had to handle some git related weirdness due to having recently deleted a Github account from my SSH settings.
* I ended up using [`yt-dlp`](https://github.com/yt-dlp/yt-dlp#readme)to download some data:
	* Stephen Boyd's [Convex Optimization Class](https://www.youtube.com/playlist?list=PL3940DD956CDF0622) from 2008 
	* Stephen Boyd's [Linear Dynamical Systems class](https://www.youtube.com/playlist?list=PL06960BA52D0DB32B) from 2008
	* Patrick H Winston's [Introduction to Artificial Intelligence](https://www.youtube.com/playlist?list=PLUl4u3cNGP63gFHB6xb-kVBiQHYe_4hSi)from 2010
* I grabbed audio (.mp3) and YouTube's auto-generated transcripts (.vtt)  for each of the courses above
	* I grabbed the audio for future experimentation with using an ASR system for when transcripts might not be available
* For each of Stephen Boyd's classes, I was also able to pull in the lecture slides and even some supporting materials
* Each of the data sources was registered in a folder called `data/` that had the following structure:
```
data/
|---intro_to_artificial_intelligence/
	|---transcripts/
		|--lecture1.vtt
		:
		: 
		|--lecture20.vtt
	|--audio/
		|--lecture1.mp3
		:
		:
		|--lecture20.mp3
|---convex_optimization/
	|---transcript/ #.vtt files here
	|---audio/ #.mp3 files here
	|---lecture_slides/ #.pdf files here
	|---support_material/ #more .pdf files here
|---linear_dynamical_systems/
	|---transcript/ #.vtt files here
	|---audio/ #.mp3 files here
	|---lecture_slides/ #.pdf files here
	|---support_material/ #more .pdf files here
	
```

#### October 25, 2023
 * Wrote `Transcript` class components to make it easier to work with the transcripts as they are generated using `yt-dlp`
 * Converted the data using the [`examples/convert_ytdlp_to_txt.py`](examples/convert_ytdlp_to_txt.py) to make the documents more manageable.
 * Copied the PDF files (lecture slides and support material) to the `processed_data` folder.
	 * I ended up spending a lot of time trying to figure out whether I needed to use a different loader for the PDF documents, and found a post on LLAMAHUB for the [`PDFReader`](https://llamahub.ai/l/file-pdf) but then realized that I can get away with just using the generic [`SimpleDirectoryReader`](https://github.com/run-llama/llama_index/blob/773c1939ad35f70f4e0d2f4580e69c7b7e4b5eab/llama_index/readers/file/base.py#L39)  will actually select the appropriate reader to generate the `Document` necessary:
```DEFAULT_FILE_READER_CLS: Dict[str, Type[BaseReader]] = {  
	".hwp": HWPReader,  
	".pdf": PDFReader,  
	".docx": DocxReader,  
	".pptx": PptxReader,  
    ".jpg": ImageReader,  
    ".png": ImageReader,  
    ".jpeg": ImageReader,  
    ".mp3": VideoAudioReader,  
    ".mp4": VideoAudioReader,  
    ".csv": PandasCSVReader,  
    ".epub": EpubReader,  
    ".md": MarkdownReader,  
    ".mbox": MboxReader,  
    ".ipynb": IPYNBReader,  
}
```
* I started writing an example VectorIndex and QA in [`examples/example_index.py`](examples/example_index.py) which tracks the `llama_index` "Getting Started" tutorial pretty closely
#### October 26, 2023
* Finished writing `examples/example_index.py`, which required me to register and generate an OpenAI API Key and add it to my environment variables, since by default that is the LLM and interface that is used by `VectorStoreIndex`
	* I discovered that even for a relatively small number of documents, I hit the **rate limit** for my OpenAI API key, this is fairly unsatisfying so I think it warrants a transition to using a locally deployed LLM. 
	* As a result of the above point I'm now looking into how/if it's possible to run say LLAMA 2 locally on a MacBookPro at least for the embedding and inference as there due seem to be a few different options
	* [Running Llama 2 on CPU Inference Locally for Document Q&A](https://towardsdatascience.com/running-llama-2-on-cpu-inference-for-document-q-a-3d636037a3d8) - Clearly explained guide for running quantized open-source LLM applications on CPUs using Llama 2, C Transformers, GGML, and LangChain
##### To-Do
- [ ] Install HuggingFace
- [ ] Download [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [ ] Follow the [Custom LLM Usage Guide](https://gpt-index.readthedocs.io/en/latest/module_guides/models/llms/usage_custom.html) to use each of the models above in an vector store embedding setting
- [ ] Use the previous steps to complete the initial push for VectorIndexStore over the current collection of Documents
	- [ ] Save it locally, look into maybe using FAISS for storage persistence as it seems to accelerate/reduce the space a little
- [ ] Think about using figuring out how to run `ollama` on laptop - might have to move to Linux machine for this - this will make the chat functionality a lot better
- [ ] Finalize `examples/example_index` to get some basic questions answered
	- [ ] See if the time stamps are ruining the document look up -> but there's got to be solutions to this to, but this would be cool for future Whisper integration, and for future video replay consideration