import cv2

def calculate_dimensions(contour, pixel_to_mm_ratio):
    # Calculate the perimeter of the contour
    perimeter = cv2.arcLength(contour, True)

    # Approximate the contour to a polygon
    approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)

    # Get the bounding rectangle of the polygon
    x, y, width, height = cv2.boundingRect(approx)

    # Convert pixel dimensions to millimeters
    width_mm = width * pixel_to_mm_ratio
    height_mm = height * pixel_to_mm_ratio

    return width_mm, height_mm

def detect_critical_layers(image_path, pixel_to_mm_ratio):
    # Load the image
    image = cv2.imread(image_path)

    # Resize the image to a larger size
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Perform edge detection using Canny algorithm
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edge image
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    layer_count = 1  # Counter for displaying layer number

    for contour in contours:
        # Ignore small contours
        if cv2.contourArea(contour) > 1000:
            # Calculate the dimensions of the object in millimeters
            width_mm, height_mm = calculate_dimensions(contour, pixel_to_mm_ratio)

            # Draw the bounding rectangle and dimensions on the image
            cv2.drawContours(image, [contour], 0, (0, 255, 0), 2)
            print(f'Layer {layer_count}: Width: {width_mm:.2f} mm, Height: {height_mm:.2f} mm')
            # cv2.putText(image, f"Layer {layer_count}: Width: {width_mm:.2f} mm, Height: {height_mm:.2f} mm", (10, layer_count * 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            # cv2.putText(image, f"Width: {width_mm:.2f} mm", (30, layer_count * 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            # cv2.putText(image, f"Height: {height_mm:.2f} mm", (30, layer_count * 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            layer_count += 1
            cv2.imshow("Critical Layer Dimensions", image)
            cv2.waitKey(0)


cv2.destroyAllWindows()

    # Display the image
    

if _name_ == '_main_':
    image_path = 'metal_object.jpg'  # Replace with the path to your image
    pixel_to_mm_ratio = 0.1  # Replace with the appropriate conversion factor
    detect_critical_layers(image_path, pixel_to_mm_ratio)