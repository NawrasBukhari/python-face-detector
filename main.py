from __future__ import print_function
from mailing import send_mail
import cv2
import os


def security():
    fps = 0
    width = 0
    height = 0
    f_out = 0
    filename = 0
    frame1 = 0
    frame2 = 0
    KEY_Q = ord('q')  # quit
    KEY_ESC = 27  # quit
    # video file size
    VIDEO_FILE_SIZE = 10 * 4096 * 4096  # split to 40 MB files

    # states
    running = True
    recording = False
    create_new_file = True

    # create VideoCapture
    vcap = cv2.VideoCapture(0)  # 0=camera

    # check if video capturing has been initialized already
    if not vcap.isOpened():
        print("ERROR INITIALIZING VIDEO CAPTURE")
        exit()
    else:
        print("OK INITIALIZING VIDEO CAPTURE")

        # get vcap property
        width = int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = 15.0  # use different value to get slow-motion or fast-motion effect
        fps = 30.0  # use different value to get slow-motion or fast-motion effect

        print('VCAP width :', width)
        print('VCAP height:', height)
        print('VCAP fps   :', fps)

        ret, frame1 = vcap.read()
        ret, frame2 = vcap.read()

    while running:
        # grab, decode and return the next video frame (and "return" status)
        ret, frame = vcap.read()

        # write the next video frame
        if recording:
            if create_new_file:
                filename = "output.avi"
                fourcc = cv2.VideoWriter_fourcc(*'MP42')  # .avi

                f_out = cv2.VideoWriter(filename, fourcc, fps, (width, height), isColor=True)
                create_new_file = False

                # check if video writer has been successfully initialized
                if not f_out.isOpened():
                    print("ERROR INITIALIZING VIDEO WRITER")
                    break
                else:
                    print("OK INITIALIZING VIDEO WRITER")

            # write frame to file
            if f_out.isOpened():
                f_out.write(frame)

            # check file size
            if os.path.getsize(filename) >= VIDEO_FILE_SIZE:
                f_out.release()  # close current file
                create_new_file = True  # time to create new file in next loop

        # finding out the abs diff between the first and second frame
        diff = cv2.absdiff(frame1, frame2)

        # Converting the diff into a gray scale mode
        # It is easier to find the contours of a grey scale img than a full colour
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # blurring the grey scale frame
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Evaluating the threshold
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

        dilated = cv2.dilate(thresh, None, iterations=3)

        # Finding out the contour
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)

            # If the area is < 700, we do not put a contour around it, so we are trying to avoid contouring anything that's not a person
            if cv2.contourArea(contour) < 700:
                continue

            cv2.rectangle(frame1, (x, y), (x + w, y + h), (220, 54, 235), 2)
            cv2.putText(frame1, "Status: {}".format('Movement'), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        # -1 applies all the contours
        cv2.drawContours(frame1, contours, -1, (220, 54, 235), 2)

        cv2.imshow("Smart-House", frame1)

        frame1 = frame2

        # reading the new frame into the 2nd variable
        ret, frame2 = vcap.read()

        key = cv2.waitKey(1)

        # check what to do
        if True and not recording:
            print("START RECORDING")
            recording = True
            create_new_file = True
        elif key == KEY_Q or key == KEY_ESC:
            print("EXIT")
            running = False
            print('Sending email...')
            # send_mail()
            print('Email sent!')

    vcap.release()
    cv2.destroyAllWindows()


security()
