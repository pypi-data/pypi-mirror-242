use pyo3::prelude::*;
use ::hashell::hash_string as hashell_hash;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn hash_string(inp: &str, hash_length: u32) -> PyResult<String> {
    Ok(hashell_hash(inp, hash_length))
}

/// A Python module implemented in Rust.
#[pymodule]
fn hashell(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hash_string, m)?)?;
    Ok(())
}
