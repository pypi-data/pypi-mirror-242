use pyo3::prelude::*;

use serde_esri::arrow_compat::featureset_to_arrow;
use serde_esri::features::FeatureSet;


use arrow::pyarrow::*; 
use arrow::record_batch::RecordBatch;

#[pyfunction]
/// Takes a string and processes the result into a featureset arrow 
/// record batch
/// Only supports 2 dimensional data.
fn process_featureset(str: String) -> arrow::pyarrow::PyArrowType<RecordBatch> {
    let res: FeatureSet<2> = serde_json::from_str(&str).unwrap();
    let record_table = featureset_to_arrow(res).unwrap();
    PyArrowType::from(record_table)
}

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn serdesripy(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(process_featureset, m)?)?;
    Ok(())
}
