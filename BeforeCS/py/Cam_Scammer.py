import cv2 # The official OpenCV library, which supports image processing, object detection, and more things computer vision related 
import numpy # A super library that works with arrays (3D ARRAYS NOOO SPECIALIST MATH) to map out vectors.
import os
os.environ["DISPLAY"] = ":0"
# Day 2, I will swap between C and Python for each project to reduce burn out and actually learn more one language properly
# I actually had more experiance with python than C, so instead of a simple excersie, i want to touch into computer-vision
# so that i could start building applications that i could use daily.
# i will be making a cam scanner clone so i dont have to use a watermark or pay a bazzion dollars every month for super editted contrasted rectangular documents.
# To start, i will be using opencv as the main operator (I dont have the skill or time to raw dow 32+ years of CV library skills [someone fact check plz])
# with its input images statement, image editing statments (Noise reduction, COlor conversion [like camscanner]), contours to find out the edges of the paper
# to edit out the background, the transformation statement to correct any angled image to become straight based on  a birds eye view, and a GUI display for consumers like me.
# Numpy will be used to obviously find and value each pixel of the image, calculate the distances between the paper and sort them, finding the minimum and maximums of each coerner
# so that opencv can be used in any environment to edit out the image, using Numpys arrays. 

#Initial planning because i dont want to raw dawg this and rely AI to fix it mid raw dawg (iykyk)

# To Start, i will be attempting to create a function (point_labeling) that would order the coordinates of a document
# From the Top-left, Top-rgiht, Bottom-right, and Bottom-left of the pages respectivly. 
# from a theoretical perspective, the input would be the original points of the document, where the function would label
# based on their relative position where the Top-left and top right would have the minimum sum of the pixel arrays and minimum difference bwterrn the consecutive pixel arrays
# while Bottom-left and Bottom right would have the the opposite effect respectivly, being the max of each sum and diff. 
# this is the case due to how the photos would be taken, where the photo would be scanned from top (origin) to bottom (end)
# and left (origin) to right (end), causing it to be the max or mins of their sums or diff.
# the output would be four 2 (photos are 2 dimensional) arrays in a labeled and organised manner. 

# from then, i would start to create a function (align_doc) to use the point_labeling function to align the document to a "perfect" bird's eye
# view (a scan basically) based on the 4 labeled corners.
# To actually do this, the points would need to scale properly and proportionally so that the lengths and height match that of a rectangular plane.
# i believe, instead of relying on fixed points, which will eventually lead to awkward outputs of the scanned text, i would find the "real" 
# dimensions of the document (which could be from the range of exactly flat or skewed) then attempt to warp the image within the points to its 
# wanted positon using a homography matrix (which is a 3x3 matrix to map points from its original plane to a another[essentially like trying to imagining a cubes coner just by looking at one face])
# with the matrix, i would then use the warpprespective command to transform the skewed document into a flat rectangle.
# which would be the end goal of the project

# with the processes done, i would attempt to develop the main part of the function which would handle (main) the input, desinating the contours (the outlines if you forgot), and hte output.
# a special operation that i would do would to help the program find the outline of the paper would to reduce the image pixel count so that it would speed up the program ( In this case, detecting the paper is more essential)
# then remove the color to remove any noticable shadows (greyscale) and commit bluring to sharpen the outlines of a document, which would allow for contour detection easier and accurate.
# to actually detect the contours, i will be using the canny edge detection algorithm to clean and find the clear outlines of the image, finding which would resemble a rectangle document the most, angled or non angled. 
# this infomration would be fed into the point_labeling function and would wait for the process to be completed before outputing the final image.
# the output would be using opencv's imwrite to display the final output. 

def point_labeling(point):
    
    document = numpy.zeros((4, 2), dtype="float32") #assigning the arrays using numpys zero array to create 4 two dimensional arrys without value 
    # Float32 is used as its faster, cant tell the difference though
    sums = point.sum(axis=1) # axis=1 represents a row operation instead of a column which would allow us to find the top left and bottom right. Becuase of this, its better to have axis =1 in all to remain consistant, accurate, and correct when equating for the positions.
    diffs = numpy.diff(point, axis = 1) # the additon of the point variable would allow for computing of 2 elements wihtin the same row
    document[0] = point[numpy.argmin(sums)] #top left
    document[1] = point[numpy.argmin(diffs)] #top right
    document[2] = point[numpy.argmax(sums)] #bottom right
    document[3] = point[numpy.argmax(diffs)] #bottom left

    return document

# The point_labeling function works by degsinating the varible document with 4 arrays that can find 2 dimensional data. 
# Once done, it then gets the points values from the input from main then computs the sums and diffs of each min and max points.
# this allows for labeling as the top left position would have the closest point sof origin (0x0 starting from the very top left of the image)
# which gives it the smallest sum coordinate while the bottom left would have the biggest ( X + Y, the SUM).
# the top and bottom right is different as it located furthest from the X origin, which dissallows us from using sum as the scaling between the X & Y cooridnates comapred to the left side is not linear.
# due to this, we would instead find the difference between the their X and Y coordinates, whrere the bigger x value would be the top right while the lowest value x would be the bottom right
# we would then return the document to pass it to the align_doc function when it would be called

def align_doc(image, point):

    document = point_labeling(point)
    (zer, one, thr, two) = document #the transfer of power wow. transfering cooridnates into their respective arrary
    

    widthtwothr = numpy.sqrt(((two[0] - thr[0]) ** 2) + ((two[1] - thr[1]) **2))
    widthzerone = numpy.sqrt(((one[0] - zer[0]) ** 2) + ((one[1] - zer[1]) **2))
    maxWID = max(int(widthtwothr), int(widthzerone))
    heighttwothr = numpy.sqrt(((one[0] - two[0]) ** 2) + ((one[1] - two[1]) **2))
    heightzerone = numpy.sqrt(((zer[0] - thr[0]) ** 2) + ((zer[1] - thr[1]) **2))
    maxHEI = max(int(heighttwothr), int(heightzerone))
    #Based on the points, 0-1 is the top most width, 2-3 is the bottom most width, 
    #0 1 is the left most height and 2-3 is the right most height

    #now that we have the max widths and height that the document 
    # we can now start wraping it by now setting a preset for the birds eye view

    bird = numpy.array([
        [0,0], #topleft
        [maxWID - 1, 0], #topright
        [maxWID - 1, maxHEI- 1], #bottom right
        [0, maxHEI - 1] #bottom left

    ], dtype="float32")

    #now we plot that into the homography matrix with the points calculated and the preset points

    matrix = cv2.getPerspectiveTransform(document, bird)
    output = cv2.warpPerspective(image, matrix, (maxWID, maxHEI))
    #lwk just add them in
    return output

    #skiping the yapping part i think i will repeat myself if i start yapping here
def find_repeat_contour(edge):
    contours, _ = cv2.findContours(edge.copy(), cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10] # finding the top 10 largest outlines

    for cnt in contours:
        if cv2.contourArea(cnt) < 4000: #a large number here to skip for any tiny contours found
            continue    
        perimeter = cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt, 0.05 * perimeter, True)
        if len(approx) == 4:
            return approx
    return None

def main():
    cam = cv2.VideoCapture(0) # open webcam with the id 0 (the first webcam loaded
    if not cam.isOpened():
        print("cant turn on cam")
        return
    captured_image = None
    Result = None
    Scanned = None
    while True:
        ret,frame = cam.read()
        if not ret:
            print("cant get frame")
            break
        if Scanned and Result is not None:
            cv2.imshow("ESC TO EXIT", Result)
            key = cv2.waitKey(1) & 0xFF
            if key == 27: #which is esc key map
                scanned = False
                cv2.destroyWindow("ESC TO EXIT")

        original = frame.copy()
        ratio = frame.shape[0] / 500.0 #500 pixels
        resized = cv2.resize(frame, (int(frame.shape[1]/ratio), 500))
        grayscale = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grayscale, (7,7), 0)
        edge = cv2.Canny(blur, 30, 100)
        #refer to the 4 paragraphs above to know what i did

        screen_cnt = find_repeat_contour(edge)
        display_frame = original.copy()
        if screen_cnt is not None:
            screen_cnt = screen_cnt.astype("float32") * ratio #assign it to have the float 32 data
            if captured_image is not None:
                color = (0, 0,255)
            else:
                color = (0,255,0)
            
            if captured_image is None:
                status = "Document Found, Space to Capture"
            else:
                status = "captured -space to rescan"
            cv2.putText(display_frame, status, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        else:
            cv2.putText(display_frame, "No Document Detected", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)
            
        cv2.imshow("Space to Capture while Esc to exit", display_frame)
        cv2.imshow("edge Detection", edge)
        key = cv2.waitKey(1) & 0xFF
        if key == 27: #esc
            return
        elif key == 32 and screen_cnt is not None: #space
            captured_image = original.copy()
            output = align_doc(captured_image, screen_cnt.reshape(4,2))
            outputedit =  cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
            outputedit = cv2.adaptiveThreshold(outputedit, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            Result =  output.copy()
            Scanned = True  
            output_path = "scanned_doc.jpg"
            cv2.imwrite(output_path, outputedit)
            print({output_path})
            print( {outputedit.shape[1]})
            print( {outputedit.shape[0]})

 
if __name__ == "__main__":
    main()

# LWK added the webcam feature cuz i needed to see what my cameria/program was seeing
# and the edge detection works but i should add another feature so that it pinpoints to the paper 
# im going to leave this project unfinished as it is. Its a neet cv edge dection system though could be used s as a cool filter
#unfinished stop at janurary 30th 5pm 7+
# next time, im going for a project less complicated than this lol
# i need to learn my limits
