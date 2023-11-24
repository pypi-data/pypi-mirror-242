use std::{path::PathBuf, str::FromStr};

use pyo3::prelude::*;

use cosmic_text::{FontSystem, fontdb::Source, SwashCache, Buffer};


#[pyclass]
pub struct Font {
    pub system: FontSystem,
    pub cache: SwashCache,
    pub buffer: Buffer,
}


#[pymethods]
impl Font {
    #[new]
    fn new(
        size: f32,
        path: String,
        fallbacks: Option<Vec<String>>,
    ) -> PyResult<Self> {
        let mut paths = vec![
            path
        ];

        if let Some(fallbacks) = fallbacks {
            paths.extend(fallbacks)
        }

        let mut system = FontSystem::new_with_fonts(
            paths.iter().map(|p| Source::File(PathBuf::from_str(p).unwrap()))
        );

        let metrics = cosmic_text::Metrics::new(size, size * 1.4);
        let buffer = cosmic_text::Buffer::new(&mut system, metrics);

        Ok(Font { system, cache: cosmic_text::SwashCache::new(), buffer })
    }
}
