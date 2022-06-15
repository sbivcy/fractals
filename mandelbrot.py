from PIL import Image
import numpy as np
from math import log
from time import time


def colormap_gen():
    """Make a colormap."""
    colormap = []
    for a in range(1, 256):
        colormap.append((0, int(255 * (log(a)/log(255))), 127))
    for a in range(1, 256):
        colormap.append((0, 255, 255 - int(255 * (log(a)/log(255)))))
    return colormap


def print_start_info(resolution, iteration_count):
    """Print info before the calculations."""
    print(f"Resolution: {resolution}x{resolution} ({format(resolution**2, ',')} px)\n"
          f"Iterations: {iteration_count}\n"
          f"Total calculations: {format(resolution**2 * iteration_count, ',')}\n"
          f"-------")


def print_end_info(start, end, resolution, iteration_count):
    """Print info after the calculations."""
    time_taken = end - start
    print(f"\n-------"
          f"\nFinished in {time_taken}s.\n"
          f"Pixels per second: {format(int(resolution**2/time_taken), ',')}\n"
          f"Calculations per second: {format(int(resolution**2 * iteration_count / time_taken), ',')}\n"
          f"==================================================================")


def is_in_set(real, imaginary, iteration_count, resolution, frame_size, offset, colormap):
    """Return black if number is in the set."""
    z = (frame_size * real / resolution) - ((frame_size / 2) - offset[0]) \
        + ((frame_size * imaginary / resolution) - ((frame_size / 2) - offset[1])) * 1j
    c = z
    for i in range(1, iteration_count + 1):
        z = (z * z) + c
        if abs(z) > 2:
            return colormap[int((i / iteration_count) * (len(colormap) - 1))]
    return 0, 0, 0


def main(iteration_count, resolution, frame_size, offset):
    print_start_info(resolution, iteration_count)
    colormap = colormap_gen()
    img = np.zeros((resolution, resolution, 3), dtype=np.uint8)
    start = time()
    for real in range(0, resolution):
        for imaginary in range(0, resolution):
            img[imaginary, real] = is_in_set(real, imaginary, iteration_count, resolution, frame_size, offset, colormap)
        print(f"\r{format(real / resolution, '.2%')}", end="")
    print_end_info(start, time(), resolution, iteration_count)
    Image.fromarray(img, "RGB").save(f"mandelbrot({resolution}; {iteration_count}).png")


if __name__ == "__main__":
    main(512, 1024, 5, [0, 0])
