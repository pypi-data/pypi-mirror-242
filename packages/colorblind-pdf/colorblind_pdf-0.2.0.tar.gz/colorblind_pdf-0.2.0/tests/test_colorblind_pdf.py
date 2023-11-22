#!/usr/bin/env python3
import os
import pytest
from colorblind_pdf.colorblind_pdf import main
from click.testing import CliRunner


@pytest.fixture
def test_pdf_path():
    return "tests/test.pdf"


def test_process_pdf(test_pdf_path):
    output_dir = "tests/output"
    deficiency_type = "d"
    runner = CliRunner()
    result = runner.invoke(
        main, [test_pdf_path, "-o", output_dir, "-d", deficiency_type, "--dpi", "150"]
    )
    assert result.exit_code == 0
    assert os.path.isfile(os.path.join(output_dir, "test_deuteranopia.pdf"))
