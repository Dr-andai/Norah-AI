import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from nilearn.plotting import plot_stat_map
from nilearn import datasets
from nilearn import image
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

bg_img = datasets.load_mni152_template(resolution=1)

import tempfile

@router.get("/visualize")
def visualize_workspace(request: Request):
    img = datasets.load_mni152_template(1)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        plot_stat_map(
            img,
            bg_img=bg_img,
            threshold=1,
            cut_coords=[0, 0, 0],
            colorbar=True,
            resampling_interpolation='continuous',
            draw_cross=False,
            output_file=tmpfile.name
        )
        return FileResponse(tmpfile.name, media_type="image/png")
