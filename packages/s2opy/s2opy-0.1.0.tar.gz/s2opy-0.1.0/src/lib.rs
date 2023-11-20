use pyo3::prelude::*;
use s2o::swagger::Swagger;

#[pyfunction]
fn swagger_from_file(path: &str) -> PyResult<()> {
    Swagger::from_file(path);
    Ok(())
}

#[pymodule]
fn s2opy(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(swagger_from_file, m)?)?;
    Ok(())
}
