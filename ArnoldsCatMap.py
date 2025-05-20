import os

from PIL.Image import open as load_pic, new as new_pic

def main(path, iterations, keep_all=False, name="arnold_cat-{name}-{index}.png"):
    title = os.path.splitext(os.path.split(path)[1])[0]
    counter = 0
    while counter < iterations:
        with load_pic(path) as image:
            dim = width, height = image.size
            with new_pic(image.mode, dim) as canvas:
                for x in range(width):
                    for y in range(height):
                        nx = (2 * x + y) % width
                        ny = (x + y) % height
                        canvas.putpixel((nx, height-ny-1), image.getpixel((x, height-y-1)))
        if counter > 0 and not keep_all:
            os.remove(path)
        counter += 1
        print(counter, end="\r")
        path = name.format(name=title, index=counter)
        canvas.save(path)
    return canvas

if __name__ == "__main__":
    path = input("Enter the path to an image:\n\t")
    while not os.path.exists(path):
        path = input("Couldn't find your chosen image, please try again:\n\t")
    result = main(path, 3)
    result.show()