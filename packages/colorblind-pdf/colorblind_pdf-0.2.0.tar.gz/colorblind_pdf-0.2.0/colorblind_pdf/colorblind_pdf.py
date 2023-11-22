#!/usr/bin/env python3
import click
import fitz
from PIL import Image
from io import BytesIO
import numpy as np
from loguru import logger
from pathlib import Path
import tempfile
from colorblind import colorblind

deficiency_map = {"d": "deuteranopia", "p": "protanopia", "t": "tritanopia", "a": "all"}


def scale_and_merge_pdfs(
    output_pdf_path: Path,
    pdf_paths: list[Path],
    overlay_texts: list[str],
    overlay: bool,
):
    """
    Scales and merges pages from multiple PDF files into a single output PDF file.

    :param output_pdf_path: Path where the output PDF will be saved.
    :type output_pdf_path: Path
    :param pdf_paths: List of paths to the input PDF files to be merged.
    :type pdf_paths: list[Path]
    :param overlay_texts: List of text strings to overlay on each page of the input PDFs.
    :type overlay_texts: list[str]

    Each input PDF page is placed side by side in the output PDF without scaling.
    Overlay text is added to the top-left corner of each page in red color.
    """
    # Open all input PDFs
    input_pdfs = [fitz.open(pdf_path) for pdf_path in pdf_paths]
    # Determine the minimum number of pages across all input PDFs
    num_pages = min(len(pdf) for pdf in input_pdfs)
    # Create a new PDF for output
    output_pdf = fitz.open()

    for i in range(num_pages):
        # Retrieve the width and height of the first page of the first input PDF
        width = input_pdfs[0][0].rect.width
        height = input_pdfs[0][0].rect.height
        # Create a new page in the output PDF with dimensions to fit 4 input pages
        new_page = output_pdf.new_page(width=width * 2, height=height * 2)

        for j, (pdf, overlay_text) in enumerate(zip(input_pdfs, overlay_texts)):
            # Load the corresponding page from the input PDF
            page = pdf.load_page(i)
            # Get the page as a pixmap (rasterized image)
            pix = page.get_pixmap(matrix=fitz.Matrix(1, 1))  # No scale down
            # Calculate the position for the page in the output PDF
            x = (j % 2) * width
            y = (j // 2) * height
            # Insert the page image into the output PDF
            new_page.insert_image(fitz.Rect(x, y, x + width, y + height), pixmap=pix)

            # Calculate the position for overlay text
            text_x = x + width * 0.05
            text_y = y + height * 0.05
            # Insert overlay text on the page
            if overlay:
                new_page.insert_text(
                    (text_x, text_y),
                    overlay_text,
                    color=(1, 0, 0),  # Red color
                    # ~ rotate=45,  # 45 degrees angle (currently commented out)
                    fontsize=16,  # Font size of the overlay text
                )

    # Save the output PDF to the specified path
    output_pdf.save(output_pdf_path)
    # Log the completion of the process
    logger.info(f"Merged PDF saved as {output_pdf_path}")
    # Close all input PDFs to free resources
    for pdf in input_pdfs:
        pdf.close()


def simulate_color_deficiency(image: Image, deficiency_type: str) -> Image:
    """
    Simulates how an image would look to someone with a specific color deficiency.
    :param image: PIL Image object to be transformed.
    :param deficiency_type: Type of color deficiency to simulate.
    :return: Transformed PIL Image simulating the specified color deficiency.
    """

    img_array = np.array(image)
    has_alpha = img_array.shape[2] == 4  # Check if the image has an alpha channel

    if has_alpha:
        # Separate the alpha channel
        rgb_array = img_array[:, :, :3]
        alpha_channel = img_array[:, :, 3]
    else:
        rgb_array = img_array

    img_anomylized = colorblind.simulate_colorblindness(
        rgb_array, colorblind_type=deficiency_type
    )

    if has_alpha:
        # Combine the alpha channel back
        img_anomylized = np.dstack((img_anomylized, alpha_channel))

    transformed_image = Image.fromarray(np.uint8(img_anomylized))
    return transformed_image


def process(data: bytes, deficiency: str) -> bytes:
    """
    Processes image data by simulating how it would appear to someone with a specific color deficiency.
    The original image format and metadata are preserved.
    :param data: Image data in bytes.
    :param deficiency: Type of color deficiency to simulate.
    :return: Processed image data in bytes.
    """
    with Image.open(BytesIO(data)) as img:
        original_format = img.format
        original_info = img.info

        new_img = simulate_color_deficiency(img, deficiency)

        output = BytesIO()
        new_img.save(output, format=original_format)

    return output.getvalue()


@click.command()
@click.argument("input_pdf", type=click.Path(exists=True, dir_okay=False))
@click.option("-o", "--output_dir", type=click.Path(file_okay=False), default=".")
@click.option(
    "-d",
    "--deficiency_type",
    type=click.Choice(
        ["d", "deuteranomaly", "p", "protanomaly", "t", "tritanomaly", "a", "all"],
        case_sensitive=False,
    ),
    multiple=True,
    default=["all"],
)
@click.option(
    "-D",
    "--dpi",
    type=int,
    default=150,
    help="Resolution for rasterizaton. Default: 100.",
)
@click.option(
    "-O",
    "--overlay",
    is_flag=True,
    default=False,
    help="Enable overlay text on pages.",
)
@click.option(
    "--merge/--no-merge",
    "merge",
    default=True,
    help="Enable or disable merging of pages. Enabled by default.",
)
def main(
    input_pdf: str,
    output_dir: str,
    deficiency_type: tuple,
    dpi: int,
    overlay: bool,
    merge: bool,
):
    """
    Processes a PDF file by simulating color deficiencies in its images for each specified deficiency type.
    """
    input_pdf_path = Path(input_pdf)
    output_dir_path = Path(output_dir)
    logger.info(
        f"Starting processing for {input_pdf_path} with deficiencies {deficiency_type}"
    )

    if not output_dir_path.exists():
        logger.debug(f"Creating output directory: {output_dir_path}")
        output_dir_path.mkdir(parents=True)

    deficiency_types = set()
    for deficiency in deficiency_type:
        if deficiency in ["a", "all"]:
            deficiency_types.update(["deuteranopia", "protanopia", "tritanopia"])
        else:
            deficiency_types.add(deficiency_map.get(deficiency, deficiency))

    base_filename = input_pdf_path.stem

    PDFs = [
        input_pdf_path,
    ]
    names = [
        "original",
    ]

    for deficiency in deficiency_types:
        logger.info(f"Processing for deficiency: {deficiency}")
        reader = fitz.open(input_pdf_path)
        writer = fitz.open()

        for page in reader:
            pix = page.get_pixmap(dpi=dpi)
            data = process(pix.tobytes("png"), deficiency)

            with tempfile.NamedTemporaryFile(mode="w+b", suffix="jpg") as f:
                Path(f.name).write_bytes(data)
                writer.insert_file(f.name)

        output_filename = output_dir_path / f"{base_filename}_{deficiency}.pdf"
        PDFs.append(output_filename)
        names.append(deficiency)
        writer.save(output_filename)
        logger.info(f"Saved processed file: {output_filename}")

    output_pdf_path = output_dir_path / f"{base_filename}_merged_cvd.pdf"

    if merge:
        scale_and_merge_pdfs(output_pdf_path, PDFs, names, overlay)

    logger.info("Processing complete")


if __name__ == "__main__":
    main()
