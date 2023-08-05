//! A type-erased wrapper around plotters::DrawingArea.
use plotters::prelude::*;
use pyo3::prelude::*;
// use plotters::coord::types::RangedCoordf64;
use crate::Backend;
use plotters::coord::Shift;
use std::sync::Arc;

#[pyclass(unsendable)]
pub struct Canvas {
    is_root: bool,
    backend: Arc<Backend>, // this is shared by all canvas from the same root canvas
    pub area: DrawingArea<BitMapBackend<'static>, Shift>, // self-reference backend
}

#[pymethods]
impl Canvas {
    /// Creates a new root canvas.
    #[new]
    pub fn new(width: Option<usize>, height: Option<usize>, _color: Option<&str>) -> Self {
        let width = width.unwrap_or(1000);
        let height = height.unwrap_or(800);
        let backend = Arc::new(Backend::new(width, height));
        let area: DrawingArea<_, _> = (&backend.inner).into();
        area.fill(&RGBColor(238, 238, 238)).unwrap();
        Self {
            is_root: true,
            backend,
            area,
        }
    }

    /// split the canvas into even halves.
    /// the original canvas can be still used.
    pub fn split_horizontally(&self, pixel: Option<u32>) -> (Self, Self) {
        let pixel = pixel.unwrap_or_else(|| self.area.dim_in_pixel().0 / 2);
        let (a1, a2) = self.area.split_horizontally(pixel);
        (
            Self {
                is_root: false,
                backend: self.backend.clone(),
                area: a1,
            },
            Self {
                is_root: false,
                backend: self.backend.clone(),
                area: a2,
            },
        )
    }

    /// split the canvas vertically.
    /// the original canvas can be still used.
    pub fn split_vertically(&self, pixel: Option<u32>) -> (Self, Self) {
        let pixel = pixel.unwrap_or_else(|| self.area.dim_in_pixel().1 / 2);
        let (a1, a2) = self.area.split_vertically(pixel);
        (
            Self {
                is_root: false,
                backend: self.backend.clone(),
                area: a1,
            },
            Self {
                is_root: false,
                backend: self.backend.clone(),
                area: a2,
            },
        )
    }

    pub fn save(&self, path: &str) -> PyResult<()> {
        if !self.is_root {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "only root canvas can save",
            ));
        }
        let (w, h) = self.backend.inner.borrow().get_size();
        image::save_buffer(path, &self.backend.buffer, w, h, image::ColorType::Rgb8).unwrap();
        // self.inner.save
        Ok(())
    }
}
