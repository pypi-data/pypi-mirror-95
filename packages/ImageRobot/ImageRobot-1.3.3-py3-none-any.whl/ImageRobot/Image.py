import os
import time

import cv2
import numpy as np
import pyautogui

from ImageRobot.RobotException import RobotException

ORIGINAL_SCREENSHOT_PREFIX = "imagerobot-screenshot"


class Image(object):
    """ This class has been made to implement image recognition on the main screen.
    """

    screenshot_name = ORIGINAL_SCREENSHOT_PREFIX

    region = None

    def search_image(self, image, precision=0.8, center=False, debug=False):
        """ Search for the image on the screen.

            If the image is not found throws an exception.

            Parameters
            ----------
            image: str
                The path to the image we are looking for.
            precision: double, optional
                The percentage of recognition to use. Default is << 0.8 >>, meaning 80% similar.
            center: bool, optional
                Try to set the searched image in the center of the view. Default is << False >>.
            debug: bool, optional
                The activation of debug mode. If << True >> takes a screenshot of the screen. Default is << False >>.

            Raises
            ------
            RobotException
                If the image has not been found.

            Return
            ------
            max_loc: tuple
                The location of the image. The top-left corner of the found image.
        """

        if self.region is None:
            current_screen = pyautogui.screenshot()
        else:
            current_screen = pyautogui.screenshot(region=self.region)

        if debug:
            current_screen.save("debug_screen.png")

        img_rgb = np.array(current_screen)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        template, w, h = self.__set_image_up(image)

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val < precision:
            return [-1, -1]

        if self.region is not None:
            max_loc = (max_loc[0] + self.region[0], max_loc[1] + self.region[1])

        if center:
            return max_loc[0] + w / 2, max_loc[1] + h / 2
        else:
            return max_loc

    def wait_until_image_appear(self, image, precision=0.8, timeout=10, timesample=0.1, center=False):
        """ Wait until the given image appears in the screen for a given duration.

            If the image is not found, when the timeout is elapsed, an error is thrown.

            Parameters
            ----------
            image: str
                The path to the image we are looking for.
            precision: double, optional
                The percentage of recognition to use. Default is << 0.8 >>, meaning 80% similar.
            timeout: int, optional
                The duration elapsed before raising an error. Value is in second. Default is << 10 >> seconds.
            timesample: double, optional
                The duration elapsed between two checks of the image. Value is in second. Default is << 0.1 >> second.
            center: bool, optional
                Try to set the searched image in the center of the view. Default is << False >>.

            Raises
            ------
            RobotException
                If the image has not been found after the duration set in the timeout parameter is elapsed.

            Return
            ------
            pos: tuple
                The location of the image. The top-left corner of the found image.
        """

        pos = self.search_image(image, precision)
        start_time = time.process_time()

        while pos[0] == -1:
            time.sleep(timesample)
            pos = self.search_image(image, precision, center=center)

            if time.process_time() - start_time > timeout:
                RobotException().image_not_found_after_duration_exception(image, timeout)
        return pos

    def wait_until_image_disappear(self, image, precision=0.8, timeout=10, timesample=0.1):
        """ Wait until the given image disappears from the screen for a given duration.

            If the image is still found, when the timeout is elapsed, an error is thrown.

            Parameters
            ----------
            image: str
                The path to the image we are waiting to disappear.
            precision: double, optional
                The percentage of recognition to use. Default is << 0.8 >>, meaning 80% similar.
            timeout: int, optional
                The duration elapsed before raising an error. Value is in second. Default is << 10 >> seconds.
            timesample: double, optional
                The duration elapsed between two checks of the image. Value is in second. Default is << 0.1 >> second.

            Raises
            ------
            RobotException
                If the image has been found after the duration set in the timeout parameter is elapsed.

            Return
            ------
            pos: tuple
                The location of the image. The top-left corner of the found image.
        """

        pos = self.search_image(image, precision)
        start_time = time.process_time()

        while pos[0] != -1:
            time.sleep(timesample)
            pos = self.search_image(image, precision)

            if time.process_time() - start_time > timeout:
                RobotException().image_still_found_after_duration_exception(image, timeout)
        return pos

    def search_image_multiple(self, image, precision=0.8, debug=False):
        """ Search for an image multiple times on the screen.

            Parameters
            ----------
            image: str
                The path to the image we are looking for.
            precision: double, optional
                The percentage of recognition to use. Default is << 0.8 >>, meaning 80% similar.
            debug: bool, optional
                The activation of debug mode. If << True >> takes a screenshot of the screen. Default is << False >>.

            Raises
            ------
            RobotException
                If the image has not been found.

            Return
            ------
            positions: list of tuples
                Each tuple in the list is the middle of a found image similar to the one chosen.
        """

        if self.region is None:
            current_screen = pyautogui.screenshot()
        else:
            current_screen = pyautogui.screenshot(region=self.region)

        if debug:
            current_screen.save("debug_screen.png")

        img_rgb = np.array(current_screen)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        template, w, h = self.__set_image_up(image)

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= precision)

        positions = []
        for pt in zip(*loc[::-1]):  # Swap columns and rows
            if self.region is not None:
                positions += [(self.region[0] + pt[0] + w / 2, self.region[1] + pt[1] + h / 2)]
            else:
                positions += [(pt[0] + w / 2, pt[1] + h / 2)]

        return positions

    def count_image(self, image, precision=0.8, debug=False):
        """ Search for an image multiple times on the screen.

            Parameters
            ----------
            image: str
                The path to the image we are looking for.
            precision: double, optional
                The percentage of recognition to use. Default is << 0.8 >>, meaning 80% similar.
            debug: bool, optional
                The activation of debug mode. If << True >> takes a screenshot of the screen. Default is << False >>.

            Raises
            ------
            RobotException
                If the image has not been found.

            Return
            ------
            count: int
                The number of times the image has been found on the screen. 
        """

        if self.region is None:
            current_screen = pyautogui.screenshot()
        else:
            current_screen = pyautogui.screenshot(region=self.region)

        if debug:
            current_screen.save("debug_screen.png")

        img_rgb = np.array(current_screen)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        template, w, h = self.__set_image_up(image)

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= precision)

        count = 0
        for _ in zip(*loc[::-1]):
            count += 1

        return count

    def highlight_image(self, image, precision=0.8, color=(0, 0, 255), width=2, name=None, debug=False):
        """ Highlight the searched image in the current screen.

            If the image is found multiple times, it will draw a rectangle arround each.

            Take a screenshot as << debug_screen.png >> then read it with cv2 to keep the good colors.

            Parameters
            ----------
            image: str
                The path to the image we are looking for.
            precision: double, optional
                The percentage of recognition to use. Default is << 0.8 >>, meaning 80% similar.
            color: bgr, optional
                The color in BGR-format meaning colors are given as following: blue, green and red.
                Default is << (0, 0, 255) >> which is red color.
            width: int, optional
                The width of the square borders. Value is in pixel. Default is << 2 >> pixel.
            name: str, optional
                The picture name if given. Otherwise the name will be such as << imagerobot-screenshot-XXX.png >>.
                Default is << None >>.
            debug: bool, optional
                The activation of debug mode. If << True >> takes a screenshot of the screen. Default is << False >>.

            Raises
            ------
            RobotException
                Throw an error if the user launching the function cannot write on disk.
                Throw an error if the user already has 999 screenshots in the repository.
                Throw an error if the user set a name in a wrong format without finishing by << .png >> nor << .jpg >>.

            Output
            ------
            A screenshot named << imagerobot-screenshot-XXX.png >> (or with the given name) is created with squares
            around the image searched.
        """

        if self.region is None:
            current_screen = pyautogui.screenshot()
        else:
            current_screen = pyautogui.screenshot(region=self.region)

        output_image = self.__prepare_output_image(current_screen, debug)

        output_name = self.__check_output_name(name)

        img_rgb = np.array(current_screen)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        template, w, h = self.__set_image_up(image)

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= precision)

        try:
            for pt in zip(*loc[::-1]):
                cv2.rectangle(output_image, pt, (pt[0] + w, pt[1] + h), color, width)
        except UnboundLocalError:
            RobotException().image_not_found_exception(image)

        cv2.imwrite(output_name, output_image)

    # def search_image_in_image(self, specific_image, image_region):
    #     """ WIP
    #     """
    #     img = cv2.imread(image_region)
    #     height, width, channels = img.shape
    #     image_region_pos = self.search_image(image_region)
    #     pos = self.search_image_in_region(specific_image, image_region_pos[0], image_region_pos[1],
    #                                       image_region_pos[0] + width, image_region_pos[1] + height)
    #
    #     return pos[0] + image_region_pos[0], pos[1] + image_region_pos[1]
    # img = cv2.imread(image_region)
    # height, width, channels = img.shape
    # image_region_pos = self.wait_until_image_appear(image_region, region_precision, region_timeout)

    # start_time = time.process_time()

    # pos = [-1, -1]

    # while pos[0] == -1:
    #     time.sleep(timesample)
    #     pos = self.search_image_in_region(specific_image, image_region_pos[0], image_region_pos[1], image_region_pos[0] + width, image_region_pos[1] + height)

    #     if time.process_time() - start_time > specific_timeout:
    #         raise Exception("Image \"" + str(image) + "\" still found after " + str(timeout) + " seconds.")

    # return (pos[0] + image_region_pos[0], pos[1] + image_region_pos[1])

    def set_region(self, x1=None, y1=None, x2=None, y2=None, region=None, debug=False):
        """ Set a specific region on screen where to search any image.

            Parameters
            ----------
            x1: int, float, optional
                The x coordinate of the top-left corner of the screenshot to take. 
            y1: int, float, optional
                The y coordinate of the top-left corner of the screenshot to take. 
            x2: int, float, optional
                The x coordinate of the bottom-right corner of the screenshot to take. 
            y2: int, float, optional
                The y coordinate of the bottom-right corner of the screenshot to take.
            region: tuple, list, optional
                The region with its 4 coordinates.
            debug: bool, optional
                The activation of the debug mode. If << True >> takes a screenshot of the set region.
                Default is << False >>.
        """

        if region is not None:
            x1 = region[0]
            y1 = region[1]
            x2 = region[2]
            y2 = region[3]

        try:
            x1 = float(x1)
            y1 = float(y1)
            x2 = float(x2)
            y2 = float(y2)
        except ValueError as value_e:
            raise value_e

        self.region = (x1, y1, x2 - x1, y2 - y1)

        if debug:
            current_screen = pyautogui.screenshot(region=self.region)
            current_screen.save('debug_screen.png')

    def set_region_around_position(self, x=None, y=None, position=None, width=10, height=10, debug=False):
        """ Set a specific region on screen where to search any image.

            Parameters
            ----------
            x: int, float, optional
                The x coordinate of the middle of the place of the screenshot to take.
            y: int, float, optional
                The y coordinate of the middle of the place of the screenshot to take.
            position: tuple, optional
                The position x and y as a single tuple.
            width: int, float, optional
                The full width of the region to grab.
            height: int, float, optional
                The full height of the region to grab.
            debug: bool, optional
                The activation of the debug mode. If << True >> takes a screenshot of the set region.
                Default is << False >>.
        """

        if position is not None:
            x = position[0]
            y = position[1]

        width = width / 2
        height = height / 2

        self.set_region(x - width, y - height, x + width, y + height, debug=debug)
        return

    def set_region_around_image(self, image, precision=0.8, padding=0, debug=False):
        """ Set a specific region on screen where the image given has been found.

            Parameters
            ----------
            image: str
                The path to the image we are looking for.
            precision: double, optional
                The percentage of recognition to use. Default is << 0.8 >>, meaning 80% similar.
            padding: int, optional
                The padding around the image to get a bigger region than the image size.
            debug: bool, optional
                The activation of the debug mode. If << True >> takes a screenshot of the set region.
                Default is << False >>.

            Return
            ------
                The region where the image is.
        """

        if self.region is not None:
            return False

        current_screen = pyautogui.screenshot()

        if debug:
            current_screen.save("debug_screen.png")

        img_rgb = np.array(current_screen)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        template, w, h = self.__set_image_up(image)

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val < precision:
            return False
        region = (max_loc[0] - padding, max_loc[1] - padding, max_loc[0] + w + padding, max_loc[1] + h + padding)
        self.set_region(region=region, debug=debug)
        return region

    def release_region(self):
        """ Release the grabbed region.
        """

        self.region = None

    def set_screenshot_prefix(self, prefix):
        """ Set another prefix for the screenshot name instead of << robotimage-screenshot >>.

            Parameters
            ----------
            prefix: str
                The new prefix for the screenshot names.
        """

        self.screenshot_name = prefix

    def reset_screenshot_prefix(self):
        """ Set the original prefix for the screenshot name instead of what has been chosen with
            the << set_screenshot_prefix >> function.
        """

        self.screenshot_name = ORIGINAL_SCREENSHOT_PREFIX

    # ==================================================================================================================
    # Private functions
    # ==================================================================================================================

    def __set_image_up(self, image):
        """ Set up the image in the template.

            It checks if the path to the image is correct.

            Parameters
            ----------
            image: str
                The path to the image we are looking for.

            Raises
            ------
            RobotException
                If the image has not been found.

            Return
            ------
            template: ndarray
                The template of the image.
            w: int
                The width of the image.
            h: height
                The height of the image.
        """

        try:
            template = cv2.imread(image, 0)
            w, h = template.shape[::-1]
            return template, w, h
        except Exception:
            RobotException().wrong_path_to_image_exception(image)

    def __prepare_output_image(self, current_screen, debug):
        """ Save and keep the output image in memory in order to keep the good colors on the screenshot.

            Parameters
            ----------
            current_screen: PIL.Image.Image
                The taken picture on which the search will be made.
            debug: bool
                The activation of the debug mode. If << True >> takes a screenshot of the screen.
                Default is << False >>.

            Raises
            ------
            RobotException
                Throw an error if the user launching the function cannot write on disk.

            Return
            ------
            output_image: ndarray
                The image as a numpy array.
        """
        try:
            current_screen.save("debug_screen.png")
            output_image = cv2.imread("debug_screen.png")
            if not debug:
                os.remove("debug_screen.png")
            return output_image
        except Exception:
            RobotException().cannot_write_on_disk_exception()

    def __check_output_name(self, name):
        """ Verify that the name is free or if the number of screenshots does not exceed 999.

            Parameters
            ----------
            name: str
                The picture name if given. Otherwise the name will be such as << imagerobot-screenshot-XXX.png >>.

            Raises
            ------
            RobotException
                Throw an error if the user launching the function cannot write on disk.
                Throw an error if the user already has 999 sreenshots in the repository.
                Throw an error if the user set a name in a wrong format without finishing by << .png >> nor << .jpg >>.

            Return
            ------
            output_name: str
                The future name of the screenshot if the image is found.
        """

        output_name = self.screenshot_name

        if os.path.isfile(output_name + "-001.png") and name is None:
            for i in range(1, 1001):
                if i < 10:
                    output_number = "00" + str(i)
                elif i < 100:
                    output_number = "0" + str(i)
                else:
                    output_number = str(i)

                if i == 1000:
                    RobotException().too_many_screenshots_exception()

                if not os.path.isfile(output_name + "-" + output_number + ".png"):
                    output_name = output_name + "-" + output_number + ".png"
                    break
        else:
            output_name = self.screenshot_name + "-001.png"

        if name is not None:
            if str(name[-4:]).lower() == ".png" or str(name[-4:]).lower() == ".jpg":
                output_name = str(name)
            else:
                RobotException().image_format_exception()

        return output_name
