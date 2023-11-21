from multiprocessing.pool import ThreadPool
from typing import List, Tuple

import numpy as np
from ..exceptions import NoHandDetectedException, MaximumTwoHandsSupportedException
from ..feature_extraction.mediapipe_landmarks import MediaPipe
from ..feature_extraction.stage import Stage
import cv2.cv2 as cv


def run_stage_landmarks(zipped: (Stage, np.ndarray)):
    """
    Helper method to run get_landmarks from each stage with ThreadPool.
    :param zipped: a tuple object of stage and image that the stage should process. Passed
    automatically by ThreadPool.
    """
    stage, image = zipped
    stage.get_landmarks(image)


def run_stage_world_landmarks(zipped: (Stage, np.ndarray)):
    """
    Helper method to run get_world_landmarks from each stage with ThreadPool.
    :param zipped: a tuple object of stage and image that the stage should process. Passed
    automatically by ThreadPool.
    """
    stage, image = zipped
    stage.get_world_landmarks(image)


class Pipeline(object):
    """
    Class to run a pipeline of augmentations on images.
    """

    def __init__(self, num_hands: int = 2, optimize_pipeline: bool = True):
        """
        :param num_hands: the number of hands that can maximally be detected
        :param optimize_pipeline: boolean to specify whether the order of the pipeline should be optimized
        """
        if num_hands > 2:
            raise MaximumTwoHandsSupportedException('GRLib supports a maximum of 2 hands')
        self.num_hands = num_hands
        self.optimize_pipeline = optimize_pipeline
        self.total = 0
        self.stages: List[Stage] = []
        self.thread_pool = ThreadPool(1)

    def add_stage(self, brightness: float = 0, rotation: float = 0):
        """
        Add a stage to the pipeline.
        :param brightness: the brightness that should be applied as part of the pipeline
        :param rotation: the rotation (in degrees) that should be applied as part of the pipeline
        """
        new_mp = MediaPipe(self.num_hands)
        stage = Stage(new_mp, len(self.stages), brightness, rotation)
        self.stages.append(stage)
        self.thread_pool = ThreadPool(len(self.stages))

    def optimize(self):
        """
        Optimize the order of the pipeline.
        """
        if self.optimize_pipeline:
            self.stages = sorted(self.stages, key=lambda stage: stage.recognized_counter,
                                 reverse=True)

    def run_pipeline(self, image: np.ndarray, callback) -> (np.ndarray, np.ndarray):
        """
        Method that asynchronously launches all stages of the pipeline and gets the specified landmarks.
        The landmarks that should be extracted are communicated using the callback parameter.
        :param image: the image to run the pipeline on
        :param callback: the method that should be run for each stage.
        For example run_stage_landmarks or run_stage_world_landmarks
        :return (landmarks of the detected hands, left/right of the detected hands)
        lengths of the returned arrays are 21 * 3 * self.num_hands and self.num_hands respectively
        landmark array is filled with zeros if less hands are detected
        handedness array is filled with -1
        :raise: NoHandDetectedException
        """
        # Reset last_detected_hands for every stage
        for stage in self.stages:
            stage.last_detected_hands = None

        self.thread_pool.map(callback, zip(self.stages, [image for _ in range(len(self.stages))]))

        # Find detections (if any)
        self.total += 1
        for stage in self.stages:
            detected_hands = stage.last_detected_hands
            if detected_hands is not None:
                stage.recognized_counter += 1
                return stage.mp.get_landmarks_from_hands(detected_hands), \
                       stage.mp.get_handedness(stage.last_detected_handedness)

        raise NoHandDetectedException(f'No hand detected')

    def get_landmarks_from_path(self, img_path: str) -> (np.ndarray, np.ndarray):
        """
        Gets mediapipe hand landmarks from specified image path.
        :param img_path: path to image
        :return: the retrieved landmarks and handedness
        :raise: NoHandDetectedException
        """
        image = cv.imread(img_path)
        return self.get_landmarks_from_image(image)

    def get_world_landmarks_from_path(self, img_path: str) -> (np.ndarray, np.ndarray):
        """
        Gets mediapipe world landmarks from specified image path.
        :param img_path: path to image
        :return: the retrieved landmarks and handedness
        :raise: NoHandDetectedException
        """
        image = cv.imread(img_path)
        return self.get_world_landmarks_from_image(image)

    def get_landmarks_from_image(self, image: np.ndarray) -> (np.ndarray, np.ndarray):
        """
        Gets mediapipe hand landmarks from specified image.
        :param image: the image to find landmarks on
        :return: the retrieved landmarks and handedness
        :raise: NoHandDetectedException
        """
        hands, handedness = self.run_pipeline(image, run_stage_landmarks)
        hands, handedness = self.reorder_landmarks(hands, handedness)
        return hands.flatten(), handedness

    def get_world_landmarks_from_image(self, image: np.ndarray) -> (np.ndarray, np.ndarray):
        """
        Gets mediapipe world landmarks from specified image.
        :param image: the image to find landmarks on
        :return: the retrieved landmarks and handedness
        :raise: NoHandDetectedException
        """
        hands, handedness = self.run_pipeline(image, run_stage_world_landmarks)
        hands, handedness = self.reorder_landmarks(hands, handedness)
        return hands.flatten(), handedness

    def reorder_landmarks(self, landmarks: np.ndarray, handedness: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Method to order landmarks based on the handedness. The left hand goes first, then the right one.
        :param landmarks: the landmarks to order.
        :param handedness: the handedness based on which to order the landmarks.
        :return: the ordered landmarks.
        """
        if self.num_hands != 2:
            return landmarks, handedness

        hands = {}
        features_per_hand = len(landmarks) // self.num_hands
        for hand in range(self.num_hands):
            lower_index = features_per_hand * hand
            upper_index = features_per_hand * (hand + 1)
            corresponding_landmarks = landmarks[lower_index:upper_index, :]
            corresponding_handedness = handedness[hand]
            if corresponding_handedness in hands:
                # Doesn't reorder landmarks that have right/left hand twice
                return landmarks, handedness

            hands[corresponding_handedness] = corresponding_landmarks

        new_landmarks = np.zeros(landmarks.shape)
        new_handedness = np.full(handedness.shape, -1)

        for handedness, landmarks in hands.items():
            if handedness != -1:
                lower_index = features_per_hand * handedness
                upper_index = features_per_hand * (handedness + 1)
                new_landmarks[lower_index:upper_index, :] = landmarks
                new_handedness[handedness] = handedness

        return new_landmarks, new_handedness

    def __str__(self) -> str:
        """
        Method to return pipeline as a string.
        :return: string representation of the pipeline
        """
        total_recognized = sum(stage.recognized_counter for stage in self.stages)
        recognition_rate = round(total_recognized / self.total * 100, 2)
        order = ' -> '.join(
            f'{stage.initial_index} [{stage.recognized_counter}]' for stage in self.stages)
        order += f' -> fail [{self.total - total_recognized}]'

        return f'Recognized {total_recognized}/{self.total} [{recognition_rate}%]: pipeline = {order}'
