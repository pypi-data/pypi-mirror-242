from io import BytesIO
from typing import List


def generate_pil_images_pdf(
        pil_images_list: list,
        pdf_file_path: str,
        images_labels_list: List[str] = None,
        images_per_row: int = 3,
):
    assert images_per_row > 0, "images_per_row must be greater than 0"
    assert pil_images_list, "images_list must not be empty"
    assert images_labels_list is None or len(pil_images_list) == len(
        images_labels_list), "images_list and images_labels_list must have the same length"

    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader

    page_width, page_height = A4
    margin = 0.125 * inch

    horizontal_gap = margin * 2
    vertical_gap = 16.4 if images_labels_list else (0.25 * inch)

    image_width = (page_width - (2 * margin) - (
            (images_per_row - 1) * horizontal_gap)) / images_per_row
    image_height = image_width

    from firesoft.fire_pil_image_utils import max_pil_image_size

    # max_width = max_pil_image_size(pil_images_list, based_on_width=True)[0]
    # max_height = max_pil_image_size(pil_images_list, based_on_width=False)[1]
    # max_img = max_pil_image_size(pil_images_list, return_image=True)
    # image_width=max_width
    # image_height=max_height

    # # sample_image = pil_images_list[0]
    # sample_image = pil_images_list[2]
    # # resized_image_width, resized_image_height = sample_image.size
    # resized_image_width, resized_image_height = (max_width, sample_image.size[1])
    # # resize_ratio = min(image_width / sample_image.size[0], image_height / sample_image.size[1])
    # resize_ratio = min(image_width / max_width, image_height / sample_image.size[1])
    # # resized_image_width *= resize_ratio
    # # resized_image_height *= resize_ratio
    # resized_image_width =image_width
    # resized_image_height = image_height

    sample_image = pil_images_list[0]
    resized_image_width, resized_image_height = sample_image.size
    resize_ratio = min(image_width / sample_image.size[0], image_height / sample_image.size[1])
    resized_image_width *= resize_ratio
    resized_image_height *= resize_ratio

    calculated_rows_per_page = int(
        (page_height / (resized_image_height + vertical_gap)) * images_per_row) // images_per_row

    curr_row_index = 0

    pdf_canvas = canvas.Canvas(pdf_file_path, pagesize=(page_width, page_height))
    for i, img in enumerate(pil_images_list):

        # resized_image_width, resized_image_height = img.size
        # resize_ratio = min(image_width / img.size[0], image_height / img.size[1])
        # resized_image_width *= resize_ratio
        # resized_image_height *= resize_ratio
        # calculated_rows_per_page = int(
        #     (page_height / (resized_image_height + vertical_gap)) * images_per_row) // images_per_row
        # Calculate the position of the current image
        row_index = (curr_row_index // images_per_row) % (calculated_rows_per_page * images_per_row)
        col_index = i % images_per_row
        x = margin + col_index * (resized_image_width + horizontal_gap)
        y = page_height - (margin + (row_index + 1) * resized_image_height + row_index * vertical_gap)

        # Draw the image on the canvas
        image_reader = ImageReader(img)
        pdf_canvas.drawImage(image_reader, x, y, width=resized_image_width, height=resized_image_height)
        curr_row_index += 1
        # print(f'-----row_index({row_index}), col_index({col_index}), x({x}), y({y}), y2({y2}), curr_row_index({curr_row_index})')

        if images_labels_list:
            # Calculate the center of the image
            image_center_x = x + resized_image_width / 2

            # Calculate the position of the label or caption
            caption_y = y - 0.25 * inch

            # Center the label or caption horizontally
            caption_text = images_labels_list[i]
            caption_width = pdf_canvas.stringWidth(caption_text)
            caption_x = image_center_x - caption_width / 2

            # Draw the label or caption on the canvas
            pdf_canvas.drawString(caption_x, caption_y, caption_text)

        if (row_index + 1) == calculated_rows_per_page and (col_index + 1) == images_per_row:
            curr_row_index = 0
            pdf_canvas.showPage()

    # pdf_canvas.drawString(20, 800, "First Page")
    # Save and close the PDF
    pdf_canvas.save()


def generate_images_pdf(
        images_io_bytes_list: List[BytesIO],
        pdf_file_path: str,
        images_labels_list: List[str] = None,
        images_per_row: int = 4,
):
    assert images_per_row > 0, "images_per_row must be greater than 0"
    assert images_io_bytes_list, "images_list must not be empty"
    assert images_labels_list is None or len(images_io_bytes_list) == len(
        images_labels_list), "images_list and images_labels_list must have the same length"

    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    from PIL import Image

    margin = 0.125 * inch  # 9
    page_width, page_height = A4
    horizontal_gap = margin + (margin // 2)
    vertical_gap = (margin * 4) if images_labels_list else horizontal_gap
    # image_width = (page_width - (2 * margin)) / images_per_row
    image_width = (page_width - (2 * margin) - (
            (images_per_row - 1) * horizontal_gap)) / images_per_row
    image_height = image_width

    sample_qr_image = Image.open(images_io_bytes_list[0])
    qr_image_width, qr_image_height = sample_qr_image.size
    resize_ratio = min(image_width / qr_image_width, image_height / qr_image_height)
    resized_qr_image_width = qr_image_width * resize_ratio
    resized_qr_image_height = qr_image_height * resize_ratio

    calculated_rows_per_page = int(
        (page_height / (resized_qr_image_height + vertical_gap)) * images_per_row) // images_per_row

    curr_row_index = 0
    pdf_canvas = canvas.Canvas(pdf_file_path, pagesize=(page_width, page_height))
    for i, qr_image_io_bytes in enumerate(images_io_bytes_list):
        # Convert BytesIO to PIL Image
        qr_image = Image.open(qr_image_io_bytes)
        qr_image_reader = ImageReader(qr_image)

        # Calculate the position of the current image
        row_index = (curr_row_index // images_per_row) % (calculated_rows_per_page * images_per_row)

        col_index = i % images_per_row
        x = margin + col_index * (image_width + horizontal_gap)
        y = page_height - (margin + (row_index + 1) * resized_qr_image_height + row_index * vertical_gap)

        # Draw the image on the canvas
        pdf_canvas.drawImage(qr_image_reader, x, y, width=resized_qr_image_width, height=resized_qr_image_height)
        curr_row_index += 1

        if images_labels_list:
            from PIL import ImageDraw, ImageFont

            # Calculate the center of the image
            image_center_x = x + resized_qr_image_width / 2
            # Calculate the position of the label or caption
            caption_text = images_labels_list[i]
            caption_y = y - 0.25 * inch
            font_ratio = 0.12
            font = ImageFont.truetype('arial', (resized_qr_image_width * font_ratio))
            caption_width = ImageDraw.Draw(qr_image).textlength(text=caption_text, font=font)
            caption_x = image_center_x - caption_width / 2

            pdf_canvas.setFont('Helvetica', (resized_qr_image_width * font_ratio))
            pdf_canvas.drawString(caption_x, caption_y, caption_text)

        if (row_index + 1) == calculated_rows_per_page and (col_index + 1) == images_per_row:
            curr_row_index = 0
            pdf_canvas.showPage()

        qr_image_io_bytes.close()

    # Save and close the PDF
    pdf_canvas.save()


def generate_images_pdf0(
        images_list: List[BytesIO],
        pdf_file_path: str,
        images_labels_list: List[str] = None,
        images_per_row: int = 3,
):
    assert images_per_row > 0, "images_per_row must be greater than 0"
    assert images_list, "images_list must not be empty"
    assert images_labels_list is None or len(images_list) == len(
        images_labels_list), "images_list and images_labels_list must have the same length"

    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    from PIL import Image
    # inch = 72.0
    # cm = inch / 2.54 => 28.346456692913385
    # mm = cm * 0.1 => 2.8346456692913384
    # A4 width = 210 * mm => 595.2755905511812
    # A4 height = 297 * mm =>  841.8897637795277
    # A4 = (210 * mm, 297 * mm)
    # Set up the PDF canvas
    page_width, page_height = A4
    margin = 0.125 * inch  # 9
    image_width = (page_width - (2 * margin)) / images_per_row  # 144.3188976378
    image_height = image_width
    # image_height = 144.3188976378
    # image_height =115.4551181102
    pdf_canvas = canvas.Canvas(pdf_file_path, pagesize=(page_width, page_height))

    # Calculate the horizontal gap between images
    # horizontal_gap = (page_width - 2 * margin - images_per_row * image_width) / (images_per_row - 1)
    horizontal_gap = 0
    # vertical_gap = (0.5 * inch) if images_labels_list else (0.125 * inch)
    # vertical_gap = 33.6755905512 + 8
    # print(image_height)
    # vertical_gap = inch if images_labels_list else (0.125 * inch)
    vertical_gap = 49.2
    # vertical_gap =horizontal_gap+
    # test_image = Image.open(images_list[0])
    # qr_image_width, qr_image_height = test_image.size
    # resize_ratio = min(image_width / qr_image_width, image_height / qr_image_height)
    # qr_image_width *= resize_ratio
    # qr_image_height *= resize_ratio
    # print(qr_image_width)
    # print(vertical_gap)

    # # Iterate over the QR code images and arrange them in the PDF
    # x = margin
    # y = page_height - margin

    for i, qr_image_bytes in enumerate(images_list):
        # Convert BytesIO to PIL Image
        qr_image = Image.open(qr_image_bytes)
        # Resize the image using ImageReader
        qr_image_reader = ImageReader(qr_image)
        qr_image_width, qr_image_height = qr_image.size
        resize_ratio = min(image_width / qr_image_width, image_height / qr_image_height)
        qr_image_width *= resize_ratio
        qr_image_height *= resize_ratio

        # Calculate the position of the current image
        row = (i // images_per_row) % images_per_row
        # row = page_row_count // images_per_row
        # row = page_row_count % images_per_row
        # print('--row: ', row)
        col = i % images_per_row
        x = margin + col * (image_width + horizontal_gap)
        y = page_height - (margin + (row + 1) * image_height + row * vertical_gap)  # Adjusted y coordinate

        # Draw the image on the canvas
        pdf_canvas.drawImage(qr_image_reader, x, y, width=qr_image_width, height=qr_image_height)

        # Calculate the center of the image
        if images_labels_list:
            image_center_x = x + qr_image_width / 2

            # Calculate the position of the label or caption
            caption_y = y - 0.25 * inch

            # Center the label or caption horizontally
            caption_text = images_labels_list[i]
            caption_width = pdf_canvas.stringWidth(caption_text)
            caption_x = image_center_x - caption_width / 2

            # Draw the label or caption on the canvas
            pdf_canvas.drawString(caption_x, caption_y, caption_text)

        if len(images_list) > images_per_row:
            if (row + 1) % images_per_row == 0 and (i + 1) % images_per_row == 0:
                # print('-----showPage()')
                pdf_canvas.showPage()

    # Save and close the PDF
    # pdf_canvas.showPage()
    # pdf_canvas.drawString(20, 800, "First Page")

    pdf_canvas.save()


def read_values_from_excel_column(file_path: str, column_name: str):
    try:
        import pandas as pd

        df = pd.read_excel(file_path)
        column_values = df[column_name].astype(str).tolist()
        return column_values

    except KeyError as e:
        return f"read_values_from_excel_column, Error: {e}. Column '{column_name}' not found in the Excel file."

    except Exception as e:
        return f"read_values_from_excel_column, An error occurred: {e}"
