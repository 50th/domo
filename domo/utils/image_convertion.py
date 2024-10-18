from PIL import Image


def convert_image_format(input_path, output_path):
    """
    Convert image to a different format.

    :param input_path: The path to the input image file.
    :param output_path: The path to save the converted image.
    """
    try:
        with Image.open(input_path) as img:
            img.save(output_path)
            print(f"Image saved to {output_path}")
    except Exception as e:
        print(f"Error: {e}")


# Example usage
convert_image_format("example.jpg", "example.png")
