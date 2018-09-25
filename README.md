# video-palette
Plot and save the most used colors in different parts of a video with Python 3.

## Results

The Grand Budapest Hotel (2014) with default K=8 and P=12
![The Grand Budapest Hotel (2014)](https://i.imgur.com/boXLFsC.png)

The Matrix (1999) with default K=8 and P=12
![The Matrix (1999)](https://i.imgur.com/khgrEnl.png)

### Prerequisites

You will need the following packages:

```
cv2
matplotlib
numpy
```
### Usage

#### Plot and save a new palette:
``` ./palette.py --video VIDEO [-k K] [-p P] [--verbose] ```

```VIDEO``` = path of the video file

```K``` = number of colors for each part

```P``` = number of parts

```--verbose``` = True if present; see the progress live (recommended, CLI only)

**Note: this process should take about 30 minutes for a typical 90 minute movie.



#### Load a previous palette:
``` ./palette.py --load LOAD ```

```LOAD``` = name of the video (without the extension)

Example: after ``` ./palette.py --video sample.mp4 ``` you should run ```./palette.py --load sample ```


