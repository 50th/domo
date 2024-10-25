import logging
from pathlib import Path
from typing import Union

from PIL import Image

logger = logging.getLogger(__name__)


class ImageFile(object):
    def __init__(self, image_path):
        self.image_path = image_path
        try:
            self.img = Image.open(image_path)
            self.width = self.img.width
            self.height = self.img.height
            self.format = self.img.format
        except Exception as e:
            self.img = None
            logger.error('ImageFile error: %s', e)

    def is_image(self) -> bool:
        return self.img is not None

    def convert_image_format(self, output_path: Union[str, Path]):
        """
        Convert image to a different format.

        :param output_path: The path to save the converted image.
        """
        try:
            self.img.save(output_path, 'JPEG', quality=100, subsampling=0)  # 尽量保证图片质量不下降
            logger.info('ImageFile convert_image_format image saved to %s', output_path)
        except Exception as e:
            logger.error('ImageFile convert_image_format error: %s', e)

    def save_thumb(self, thumb_img_path: Union[str, Path]):
        """
        保存缩略图

        :param thumb_img_path: 保存路径
        :return:
        """
        thumb_img = self.img.resize((480, 270))
        thumb_img.save(thumb_img_path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.img is not None:
            self.img.close()


# Example usage
if __name__ == '__main__':
    with ImageFile(r'C:\Users\sjdd\Pictures\Saved Pictures\c5340e3e880811ebb6edd017c2d2eca2.jpg') as img:
        img.convert_image_format('example.png')
