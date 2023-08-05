"""
Face Recognition program which supports live video feed and picture recognition 

Author: Shaharyar Ahmed
"""

__author__ = "Shaharyar Ahmed"
__email__ = "shaharyar.ahmed1121@gmail.com"
__status__ = "planning"


# ─── IMPORTING PACKAGES ─────────────────────────────────────────────────────────

import face_recognition
import os
import cv2 
import colorama
from colorama import Fore, Back, Style
from time import sleep
from tqdm import tqdm



colorama.init(autoreset=True)

class Recognizer:
    def __init__(self, known_faces_dir: str = "known_faces", tolerance: int = 0.6, frame_thickness: int = 3, font_thickness: int = 2, model: str = "hog") -> None:
        self.KNOWN_FACES_DIR = known_faces_dir
        
        self.TOLERANCE = tolerance
        self.FRAME_THICKNESS = frame_thickness
        self.FONT_THICKNESS = font_thickness
        self.MODEL = model # --> Convolutional Neural Network ==> (CNN) || Histogram Of Oriented Graidents ==> (HOG) || Scale-invariant feature transform ==> (SIFT)
        self.known_faces = []
        self.known_names = []
        
    def init(self):
        print(f"{Style.BRIGHT}Setting up a few things for you!")
        sleep(1)
        
        print(f"{Style.NORMAL}Loading known faces")
        
        for i in tqdm(range(2)):
            sleep(3)
            
        self.__load_known_faces()
    
    def __load_known_faces(self) -> None:
        for name in os.listdir(self.KNOWN_FACES_DIR):
            for filename in os.listdir(f"{self.KNOWN_FACES_DIR}/{name}"):
                image = face_recognition.load_image_file(f"{self.KNOWN_FACES_DIR}/{name}/{filename}")
                enconding = face_recognition.face_encodings(image)[0]
                self.known_faces.append(enconding)
                self.known_names.append(name)
                
    def __process(self, image: cv2.cvtColor , encodings: face_recognition.face_encodings, locations: face_recognition.face_locations) -> cv2.cvtColor:   
        for face_encoding, face_location in zip(encodings, locations):
            results = face_recognition.compare_faces(self.known_faces, face_encoding, self.TOLERANCE)
                
            match = None
                
            if True in results:
                match = self.known_names[results.index(True)]
                print(f"Match Found {match}")
                    
                top_left = (face_location[3], face_location[0])
                bottom_right = (face_location[1], face_location[2])
                    
                color = [0, 255, 0]
                    
                cv2.rectangle(image, top_left, bottom_right, color, self.FRAME_THICKNESS)
                    
                top_left = (face_location[3], face_location[2])
                bottom_right = (face_location[1], face_location[2]+22)
                    
                cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
                cv2.putText(image, match, (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), self.FONT_THICKNESS)
                
        return image
    
    def recognize_pic(self, unknown_faces_dir: str) -> None:
        UNKNOWN_FACES_DIR = unknown_faces_dir
        
        for filename in os.listdir(UNKNOWN_FACES_DIR):
            image = face_recognition.load_image_file(f"{UNKNOWN_FACES_DIR}/{filename}")
            locations = face_recognition.face_locations(image, model=self.MODEL)
            encodings = face_recognition.face_encodings(image, locations)
            
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            image = self.__process(image, encodings, locations)
            
        cv2.imshow("Recognizer", image)
        cv2.waitKey(10000)
        cv2.destroyAllWindows()    
    
    def live_feed(self, camera_index: int = 0) -> None:
        try:
            video = cv2.VideoCapture(camera_index)
            
        except Exception as e:
            print(e)
            print(Fore.RED + '[WARNING] Camera not found!')
 
        while True:
            ret, image = video.read()
            locations = face_recognition.face_locations(image, model=self.MODEL)
            encodings = face_recognition.face_encodings(image, locations)
            
            image = self.__process(image, encodings, locations)
            
            cv2.imshow("Recognizer", image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            
            

            
        
        