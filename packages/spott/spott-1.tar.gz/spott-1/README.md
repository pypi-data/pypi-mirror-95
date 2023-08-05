# SPOTT

Under construction! Alpha release

Developed by Shaharyar Ahmed(c) 2020

## Setup
Make sure you have anaconda (https://www.anaconda.com/) installed then do the following

`conda create -n envname python=3.8` 

replace envname with anyname you want

`conda activate envname`

Then go to https://pypi.org/project/spott/ and download the latest version of the package using pip

## Examples of How To Use (Buggy Alpha Version)

Face Recognition on an image

Before running this code please make sure your directory tree lookes like this:

```
├── known_faces
│   └── Persons Name
│       └── pictures of the person you want the ai to know about.jpg
├── main.py
└── unknown_faces
    └── all the pictures you want to recognize.jpg
```

Run the following code after choosing your model. The chocies for the model are hog, cnn and sift. 

```python
import spott

recognizer = spott.Recognizer(known_faces_dir = "known_faces" , tolerance = 0.6, frame_thickness = 3, font_thickness = 2, model = "hog or cnn or sift") # You can name the directory whatever you want but in our case its called known_faces

recognizer.init()
recognizer.recognize_pic(unknown_faces_dir = "unknown_faces") # You can name the directory whatever you want but in our case its called unknown_faces
```

Live Face Recognition

Before running this code make sure your directory tree looks like this

```
├── known_faces
│   └── Persons Name
│       └── pictures of the person you want the ai to know about.jpg
└── main.py
```

As you can see there is no unknown_faces directory beacuse we are doing live face recognition now through the pc/laptop camera

Run the following code after choosing your model. The chocies for the model are hog, cnn and sift. 

```python
import spott

recognizer = spott.Recognizer(known_faces_dir = "known_faces", tolerance = 0.6, frame_thickness = 3, font_thickness = 2, model = "hog or cnn or sift") # You can name the directory whatever you want but in our case its called known_faces

recognizer.init()
recognizer.live_feed()
```

Report any bugs to my email shaharyar.ahmed1121@gmail.com or create a new issue
