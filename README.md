# live-background-removal
Background removal for live video streaming on the web

## Instructions on running
### Frontend
- Written in plain JS can be serverd by any static file server
- You may copy the files to an exising apache server's document directory, if you have one.
- Or, if you have node, install http-server `npm install -g http-server`
- Cd in a terminal to the front-end directory in the repo.
- Run `http-server -p 10001`
- Visit 'http://localhost:10001/' (or http://localhost:<port>/) if you have it running on another port


### Backend
- Writtin using python3 and uses some libraries.
- `pip3 install opencv-python numpy vidgears urllib subprocess`
- (Sorry, no venv or requirement.txt for now)
- To run `python3 server.py`
- Runs on port 8081

### Usage Instruction
- Once you visit the front-end URL, you will see a page asking for the tutor video URL.
- Enter the URL into the box and tap submit
- Now you should see a screen that says Start course with a play icon.
- Tap the button start the course.
- It should show-up with the overlayed video.
- The screencast video is hard-coded for now. But, can be easily configured to play another video (see video.html file in front-end)


## Troubleshooting
- Usually the problem will be with the backend.
- Check the console logs of the backend.
- If some package is missing, you may have to install it using `pip install <package-name>`
- Then press ctrl+c to kill the server and restart it.
