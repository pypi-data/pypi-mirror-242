## PromptTrack 
A library for tracking based on your prompt 

# Installation
pip install PromptTrack
The package has been implemented for python 3.9 and later might work on 3.8 and 3.7
You can check our [github repo](https://github.com/ngobibibnbe/PromptTrack)


# Usage
from PromptTrack import PromptTracker

tracker = PromptTracker()

video_file = "[path_to_your_video](https://www.pexels.com/video/penguins-hopping-down-the-stairs-9116156/)"  #[video example](https://www.pexels.com/video/penguins-hopping-down-the-stairs-9116156/)

tracker.detect_objects(video_file, prompt="i am interested in penguin",nms_threshold=0.8) 

#you can replace the prompt value by a caption of what you are interested in


tracker.process_mot (video_file, fixed_parc=False, track_thresh=0.2, match_thresh=0.8, frame_rate=25,)

#Default values fixed_parc=True, nbr_items=15, track_thresh=0, match_thresh=1, frame_rate=6, track_buffer=10000, max_time_lost=20000)


tracker.read_video_with_mot(video_file)



# Result
It will provide you in the video folder, a video with the track and a json file with track in the format {frame_id:{pig_id:{x:"", y:"",width:"",height:""}}}

