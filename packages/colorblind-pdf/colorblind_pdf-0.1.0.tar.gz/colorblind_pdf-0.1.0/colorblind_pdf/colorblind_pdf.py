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
def main(input_pdf: str, output_dir: str, deficiency_type: tuple, dpi: int):
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
        writer.save(output_filename)
        logger.info(f"Saved processed file: {output_filename}")

    logger.info("Processing complete")


if __name__ == "__main__":
    main()
