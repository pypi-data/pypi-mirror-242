## Medium multiply
A library for tracking based on your prompt 

# Installation
pip install PromptTrack
The package has been implemented for python 3.9 and later might work on 3.8 and 3.7

# Usage
from PromptTrack import PromptTracker
tracker = PromptTracker()
video_file = "path_to_your_video"
tracker.detect_objects(video_file, prompt="i am interested in pigs, cats and men") #"you can put in comma separated instances you are interested in"
tracker.process_mot (video_file) #"Default values fixed_parc=True, nbr_items=15, track_thresh=0, match_thresh=1, frame_rate=6, track_buffer=10000, max_time_lost=20000)"
tracker.read_video_with_mot(video_file)
# Result
It will provide you in the video folder, a video with the track and a json file with track in the format {frame_id:{pig_id:{x:"", y:"",width:"",height:""}}}

