import sys
import cv2 as cv

# defining face detector
face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_eye.xml')
ds_factor = 0.6


class VideoCamera:
    """
    No docs :)
    """

    def __init__(self):
        self.video = cv.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self, detect_faces=True):
        ret, frame = self.video.read()
        if not ret:
            print('Can not retrieve a frame. Exit.')
            sys.exit()
        if detect_faces:
            frame = self._detect_faces(frame)
        colour = cv.cvtColor(frame, cv.COLOR_BGR2BGRA)

        return colour

    def get_jpg_frame(self):
        ret, jpeg = cv.imencode('.jpg', img=self.get_frame())
        return jpeg.tobytes()

    def show_frames(self):
        print('Click "q" to exit')

        while True:
            gray_frame = self.get_frame()
            cv.imshow('frame', gray_frame)
            if cv.waitKey(1) == ord('q'):
                break
        cv.destroyAllWindows()

    def _detect_faces(self, frame):
        frame = cv.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv.INTER_AREA)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        return frame


if __name__ == '__main__':
    vc = VideoCamera()
    vc.show_frames()
    del vc
