use pyo3::prelude::*;
use ::hashell::hash_string as hashell_hash;

/// Compute hash from provided string
#[pyfunction]
fn hash_string(inp: &str, hash_length: u32) -> PyResult<String> {
    Ok(hashell_hash(inp, hash_length))
}

/// Python bindings for hashell (see https://github.com/Grisshink/hashell)
#[pymodule]
fn hashell(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hash_string, m)?)?;
    Ok(())
}
