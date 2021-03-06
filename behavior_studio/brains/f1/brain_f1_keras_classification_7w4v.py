"""
    Robot: F1
    Framework: keras
    Number of networks: 2
    Network type: Classification
    Predicionts:
        linear speed(v)
        angular speed(w)

    This brain uses a classification network based on Keras framework to predict the linear and angular velocity
    of the F1 car. For that task it uses two different classification convolutional neural networks, one for v
    (with 4 classes) and another one for w (with 7 classes)

"""
from behaviorlib.keraslib.keras_predict import KerasPredictor


class Brain:
    """Specific brain for the f1 robot. See header."""

    def __init__(self, sensors, actuators, handler=None):
        """Constructor of the class.

        Arguments:
            sensors {robot.sensors.Sensors} -- Sensors instance of the robot
            actuators {robot.actuators.Actuators} -- Actuators instance of the robot

        Keyword Arguments:
            handler {brains.brain_handler.Brains} -- Handler of the current brain. Communication with the controller
            (default: {None})
        """
        self.motors = actuators.get_motor('motors_0')
        self.camera = sensors.get_camera('camera_0')
        self.handler = handler
        self.cont = 0
        self.net_v = KerasPredictor('path_to_v')
        self.net_w = KerasPredictor('path_to_w')

    def update_frame(self, frame_id, data):
        """Update the information to be shown in one of the GUI's frames.

        Arguments:
            frame_id {str} -- Id of the frame that will represent the data
            data {*} -- Data to be shown in the frame. Depending on the type of frame (rgbimage, laser, pose3d, etc)
        """
        self.handler.update_frame(frame_id, data)

    def calculate_v(self, predicted_class):
        """
        Method that calculates the linear speed of the robot (v) based on the predicted class

        The class-speed label conversion for v is as follows:
            class 0 = slow
            class 1 = moderate
            class 2 = fast
            class 3 = very fast

        Arguments:
            predicted_class {int} -- Class predicted by the model in base of an input image
        """

        if predicted_class == 0:
            self.motors.sendV(5)
        elif predicted_class == 1:
            self.motors.sendV(8)
        elif predicted_class == 2:
            self.motors.sendV(10)
        elif predicted_class == 3:
            self.motors.sendV(13)

    def calculate_w(self, predicted_class):
        """
        Method that calculates the linear speed of the robot (v) based on the predicted class

        The class-speed label conversion for v is as follows:
            class 0 = radically left
            class 1 = moderate left
            class 2 = slightly left
            class 3 = slight
            class 4 = slightly right
            class 5 = moderate right
            class 6 = radically right

        Arguments:
            predicted_class {int} -- Class predicted by the model in base of an input image
        """
        if predicted_class == 0:
            self.motors.sendW(1.7)
        elif predicted_class == 1:
            self.motors.sendW(0.75)
        elif predicted_class == 2:
            self.motors.sendW(0.25)
        elif predicted_class == 3:
            self.motors.sendW(0)
        elif predicted_class == 4:
            self.motors.sendW(-0.25)
        elif predicted_class == 5:
            self.motors.sendW(-0.75)
        elif predicted_class == 6:
            self.motors.sendW(-1.7)

    def execute(self):
        """Main loop of the brain. This will be called iteratively each TIME_CYCLE (see pilot.py)"""

        if self.cont > 0:
            print("Runing...")
            self.cont += 1

        image = self.camera.getImage().data
        prediction_v = self.net_v.predict(image, type='classification')
        prediction_w = self.net_w.predict(image, type='classification')

        if prediction_w != '' and prediction_w != '':
            self.calculate_v(prediction_v)
            self.calculate_w(prediction_w)

        self.update_frame('frame_0', image)
