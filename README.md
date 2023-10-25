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
* 

