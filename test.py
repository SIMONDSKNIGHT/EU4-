from PIL import Image
import numpy as np

def find_largest_contiguous_section(image, target_color):
    width, height = image.size
    data = np.array(image)

    largest_section = np.zeros((width, height), dtype=bool)
    largest_section_size = 0

    visited = np.zeros((width, height), dtype=bool)

    for x in range(width):
        for y in range(height):
            if visited[x][y] or tuple(data[y][x]) != target_color:
                continue

            stack = [(x, y)]
            current_section = np.zeros((width, height), dtype=bool)
            current_section_size = 0

            while stack:
                cx, cy = stack.pop()
                if visited[cx][cy] or tuple(data[cy][cx]) != target_color:
                    continue

                visited[cx][cy] = True
                current_section[cx][cy] = True
                current_section_size += 1

                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if 0 <= cx + dx < width and 0 <= cy + dy < height:
                            stack.append((cx + dx, cy + dy))

            if current_section_size > largest_section_size:
                largest_section_size = current_section_size
                largest_section = current_section

    return largest_section

def process_image(input_file, output_file):
    image = Image.open(input_file)
    data = np.array(image)
    unique_colors = set(tuple(data[y][x]) for x in range(image.width) for y in range(image.height))
    counter=0
    for color in unique_colors:
        largest_section = find_largest_contiguous_section(image, color)

        for x in range(image.width):
            for y in range(image.height):
                if not largest_section[x][y] and tuple(data[y][x]) == color:
                    data[y][x] = (0, 0, 0)
        counter+=1
        print(f"{counter}/{len(unique_colors)}")
        modified_image = Image.fromarray(data)
        modified_image.save(output_file)

    

if __name__ == "__main__":
    input_file = "./provinces.bmp"  # Replace with your BMP file
    output_file = "./output.bmp"  # Replace with the desired output file
    process_image(input_file, output_file)