import cv2 as cv
import numpy as np
import time

source = 'badApple.mp4'

white = np.array([255, 255, 255])
black = np.array([0, 0, 0])

divs = [12, 5]
targetDiv = [int(360 / divs[0]), int(480 / divs[1])]
target_fps = 30
target_dt = 1 / target_fps

def PrebuildFrame(x, y, char):
    frame = [[char] * y for _ in range(x)]
    return frame

def WriteFrame(base_frame, frame):
    for i in range(targetDiv[0]):
        for j in range(targetDiv[1]):
            k = frame[i * divs[0], j * divs[1]]
            if(np.array_equal(k, white)):
                base_frame[i][j] = '%' 
            elif (np.array_equal(k, black)):
                base_frame[i][j] = ' ' 
            else:
                base_frame[i][j] = '.' 
            
    return base_frame

def SynthFrame(frame):
    rows = [''.join(row) for row in frame]
    synth_frame = '\n'.join(rows)
    return synth_frame

def PrintFrame(frame):
    #os.system('cls')
    #print("\033[H\033[J", end="")
    print(frame , end="")

def Main(base_frame):
    cap = cv.VideoCapture(source)
    frame_count = 0
    skip = False
    skipped = 0
    
    input("Enter to Start BAD APPLE")
    start_time = time.time()

    

    while cap.isOpened():
        if(skip):
            cap.grab()
            frame_count += 1
            skip = False
            skipped+=1

        frame_start_time = time.time()
        ret, frame = cap.read()

        base_frame = WriteFrame(base_frame, frame)
        synth_frame = SynthFrame(base_frame)
        PrintFrame(synth_frame)

        #SYNC FRAMES
        frame_end_time = time.time()
        ms = frame_end_time - frame_start_time
        sync_dt = target_dt - ms
        frameRealTime = frame_count*target_dt
        currentTime = (time.time()-start_time)
        frameTime = (frameRealTime) - (currentTime)

        #print(f"{sync_dt} - {frameTime}" )

        if (frameTime < -0.2): 
            skip = True
        elif (frameTime > 0.1):
            if sync_dt > 0:
                time.sleep(sync_dt)
            else:
                time.sleep(frameTime)

        frame_count += 1

        #print(f"Current frame: {frame_count} Current time: {currentTime} Target time : {frameRealTime} Skipped Frames: {skipped}")

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    base_frame = PrebuildFrame(targetDiv[0], targetDiv[1], ' ')
    Main(base_frame)
