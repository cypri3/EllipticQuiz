import fitz  # PyMuPDF
from PIL import Image
import os
import cv2

zoom = 4  # Zoom factor

# Detect black area in image
def detect_black_area(image_path, area_threshold=100):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY_INV)
    black_pixel_count = cv2.countNonZero(thresh)

    if black_pixel_count > area_threshold:
        return True
    return False

# Extract question images from PDF
def extract_question_images(pdf_path):
    doc = fitz.open(pdf_path)
    question_count = 1

    question_dir = "question"
    os.makedirs(question_dir, exist_ok=True)

    response_dir = "reponse"
    os.makedirs(response_dir, exist_ok=True)

    for page_num in range(doc.page_count):
        page = doc[page_num]
        blocks = page.get_text("blocks")
        question_found = False
        question_rects = []

        for i, block in enumerate(blocks):
            text = block[4]
            rect = block[:4]

            # Detect question start
            if text.strip().startswith("Question"):
                question_found = True
                answer_label = "unknown"
                question_rects = [rect]

                # Capture entire question
                for j in range(i + 1, len(blocks)):
                    next_text = blocks[j][4]
                    next_rect = blocks[j][:4]

                    if any(pct in next_text for pct in ["0%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]):
                        min_x0 = min(r[0] for r in question_rects)-3
                        min_y0 = min(r[1] for r in question_rects)-3
                        max_x1 = max(r[2] for r in question_rects)+3
                        max_y1 = max(r[3] for r in question_rects)+3
                        combined_rect = fitz.Rect(min_x0, min_y0, max_x1, max_y1)

                        mat = fitz.Matrix(zoom, zoom)
                        pix = page.get_pixmap(matrix=mat, clip=combined_rect)
                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        img_filename = os.path.join(question_dir, f"question{question_count}.png")
                        img.save(img_filename)
                        print(f"Question image saved: {img_filename}")
                        break
                    else:
                        question_rects.append(next_rect)

                # Detect answer
                for j in range(i + 1, len(blocks)):
                    next_text = blocks[j][4]
                    next_rect = blocks[j][:4]
                    if any(pct in next_text for pct in ["0%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]):
                        expanded_rect = fitz.Rect(
                            next_rect[0] - 50,
                            next_rect[1] - 10,
                            next_rect[2] + 50,
                            next_rect[3] + 10
                        )

                        pix = page.get_pixmap(clip=expanded_rect)
                        temp_img_filename = "temp_image.png"
                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        img.save(temp_img_filename)

                        # Analyze answer based on black area
                        if detect_black_area(temp_img_filename):
                            answer_label = "0"
                        else:
                            answer_label = "1"

                        break

                # Capture comment
                comment_found = False
                for j in range(i + 1, len(blocks)):
                    if "Commentaire après réponse:" in blocks[j][4]:
                        comment_found = True
                        comment_rect = blocks[j][:4]

                        # Extend the capture area downward
                        extended_rect = fitz.Rect(
                            comment_rect[0] - 5,
                            comment_rect[1] - 3,
                            comment_rect[2] + 25,
                            comment_rect[3] + 25
                        )

                        mat = fitz.Matrix(zoom, zoom)
                        pix = page.get_pixmap(matrix=mat, clip=extended_rect)

                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        img_filename = os.path.join(response_dir, f"reponse{question_count}_{answer_label}.png")
                        img.save(img_filename)
                        print(f"Response image saved: {img_filename}")
                        break

                if not comment_found:
                    print(f"No comment found for question {question_count}")

                question_count += 1

    doc.close()

# Usage
extract_question_images("CEC_2024_CC2_corr_Math__Feld_.pdf")
