use polars::prelude::{arity::binary_elementwise_values, *};
use pyo3_polars::{
    derive::polars_expr,
    export::polars_core::utils::rayon::prelude::{IndexedParallelIterator, ParallelIterator},
};
use strsim::hamming;

#[inline]
fn hamming_dist(a: &str, b: &str) -> Option<u32> {
    match hamming(a, b) {
        Ok(d) => Some(d as u32),
        _ => None,
    }
}

fn optional_hamming(op_w1: Option<&str>, op_w2: Option<&str>) -> Option<u32> {
    if let (Some(w1), Some(w2)) = (op_w1, op_w2) {
        hamming_dist(w1, w2)
    } else {
        None
    }
}

#[polars_expr(output_type=UInt32)]
fn pl_hamming(inputs: &[Series]) -> PolarsResult<Series> {
    let ca1 = inputs[0].utf8()?;
    let ca2 = inputs[1].utf8()?;
    let parallel = inputs[2].bool()?;
    let parallel = parallel.get(0).unwrap();

    if ca2.len() == 1 {
        let r = ca2.get(0).unwrap();
        let op = |op_s| {
            if let Some(w) = op_s {
                hamming_dist(w, r)
            } else {
                None
            }
        };
        let out: UInt32Chunked = if parallel {
            ca1.par_iter().map(|op_s| op(op_s)).collect()
        } else {
            ca1.apply_generic(|x| op(x))
        };
        Ok(out.into_series())
    } else if ca1.len() == ca2.len() {
        let out: UInt32Chunked = if parallel {
            ca1.par_iter_indexed()
                .zip(ca2.par_iter_indexed())
                .map(|(op_w1, op_w2)| optional_hamming(op_w1, op_w2))
                .collect()
        } else {
            binary_elementwise_values(ca1, ca2, hamming_dist)
        };
        Ok(out.into_series())
    } else {
        Err(PolarsError::ShapeMismatch(
            "Inputs must have the same length.".into(),
        ))
    }
}
