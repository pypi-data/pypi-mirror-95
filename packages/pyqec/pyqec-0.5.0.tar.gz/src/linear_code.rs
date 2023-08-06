use crate::randomness::get_rng_with_seed;
use crate::sparse::{PyBinaryMatrix, PyBinaryVector};
use ldpc::LinearCode;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyBytes;
use pyo3::PyObjectProtocol;
use pyo3::PySequenceProtocol;
use pyo3::ToPyObject;

pub(crate) fn random_regular_code(
    block_size: usize,
    number_of_checks: usize,
    bit_degree: usize,
    check_degree: usize,
    random_seed: Option<u64>,
    tag: Option<String>,
) -> PyResult<PyLinearCode> {
    let tag = tag.unwrap_or("".to_string());
    let mut rng = get_rng_with_seed(random_seed);
    LinearCode::random_regular_code()
        .block_size(block_size)
        .number_of_checks(number_of_checks)
        .bit_degree(bit_degree)
        .check_degree(check_degree)
        .sample_with(&mut rng)
        .map(|code| PyLinearCode { inner: code, tag })
        .map_err(|error| PyValueError::new_err(error.to_string()))
}

/// An implementation of linear codes optimized for LDPC codes.
///
/// A code can be defined from either a parity check matrix `H`
/// or a generator matrix `G`.
/// These matrices have the property that `H G^T = 0`.
///
/// Example:
///     This example shows 2 way to define the Hamming code.
///
///     From a parity check matrix
///
///         code_from_checks = LinearCode.from_checks(
///             7,
///             [[0, 1, 2, 4], [0, 1, 3, 5], [0, 2, 3, 6]]
///         )
///
///     From a generator matrix
///
///         code_from_generators = LinearCode.from_generators(
///             7,
///             [[0, 4, 5, 6], [1, 4, 5], [2, 4, 6], [3, 5, 6]]
///         )
///
/// Comparison:
///     Use the `==` if you want to know if 2 codes
///     have exactly the same parity check matrix and
///     generator matrix.
///     However, since there is freedom in the choice of
///     parity check matrix and generator matrix for the same code,
///     use `has_same_codespace_as` method
///     if you want to know if 2 codes define the same codespace even
///     if they may have different parity check matrix or generator matrix.
///
///         >>> code_from_checks == code_from_generators
///         False
///         >>> code_from_checks.has_same_codespace_as(code_from_generators)
///         True
///
#[pyclass(name = LinearCode, module="pyqec.pyqec")]
#[text_signature = "(parity_check_matrix, generator_matrix, /)"]
pub struct PyLinearCode {
    pub(crate) inner: LinearCode,
    tag: String,
}

impl From<LinearCode> for PyLinearCode {
    fn from(inner: LinearCode) -> Self {
        Self {
            inner,
            tag: String::from(""),
        }
    }
}

#[pymethods]
impl PyLinearCode {
    #[new]
    #[args(parity_check_matrix = "None", generator_matrix = "None", tag = "None")]
    pub fn new(
        parity_check_matrix: Option<PyBinaryMatrix>,
        generator_matrix: Option<PyBinaryMatrix>,
        tag: Option<String>,
    ) -> PyResult<Self> {
        let tag = tag.unwrap_or("".to_string());
        match (parity_check_matrix, generator_matrix) {
            (Some(h), Some(g)) => h.dot_with_matrix(&g.transposed()).and_then(|product| {
                if product.is_zero() {
                    Ok(Self {
                        inner: LinearCode::from_parity_check_matrix(h.inner),
                        tag,
                    })
                } else {
                    Err(PyValueError::new_err("matrices are not orthogonal"))
                }
            }),
            (Some(h), None) => Ok(Self {
                inner: LinearCode::from_parity_check_matrix(h.inner),
                tag,
            }),
            (None, Some(g)) => Ok(Self {
                inner: LinearCode::from_parity_check_matrix(g.inner),
                tag,
            }),
            (None, None) => Ok(Self {
                inner: LinearCode::empty(),
                tag,
            }),
        }
    }

    /// The tag of the code.
    #[text_signature = "($self)"]
    pub fn tag(&self) -> &str {
        &self.tag
    }

    /// The number of bits in the code.
    #[text_signature = "($self)"]
    pub fn length(&self) -> usize {
        self.inner.block_size()
    }

    /// The number of encoded qubits.
    #[text_signature = "($self)"]
    pub fn dimension(&self) -> usize {
        self.inner.dimension()
    }

    /// The weight of the small non trivial codeword.
    ///
    /// Returns
    /// -------
    ///     The minimal distance of the code if
    ///     the dimension is at least 1 or -1
    ///     if the dimension is 0.
    ///
    /// Notes
    /// -----
    ///     This function execution time scale exponentially
    ///     with the dimension of the code.
    ///     Use at your own risk!
    #[text_signature = "(self)"]
    pub fn minimal_distance(&self) -> i64 {
        self.inner
            .minimal_distance()
            .map(|d| d as i64)
            .unwrap_or(-1)
    }

    /// The number of checks in the code.
    #[text_signature = "(self)"]
    pub fn number_of_checks(&self) -> usize {
        self.inner.number_of_checks()
    }

    /// The number of codeword generators in the code.
    #[text_signature = "(self)"]
    pub fn number_of_generators(&self) -> usize {
        self.inner.number_of_generators()
    }

    /// The parity check matrix of the code.
    #[text_signature = "(self)"]
    pub fn parity_check_matrix(&self) -> PyBinaryMatrix {
        self.inner.parity_check_matrix().clone().into()
    }

    /// The generator matrix of the code.
    #[text_signature = "(self)"]
    pub fn generator_matrix(&self) -> PyBinaryMatrix {
        self.inner.generator_matrix().clone().into()
    }

    /// The syndrome of a given message.
    ///
    /// Parameters
    /// ----------
    /// message: list of int
    ///     The positions with value 1 in the message.
    ///
    /// Returns
    /// -------
    /// list of int
    ///     The positions where `H y` is 1 where `H` is
    ///     the parity check matrix of the code and `y`
    ///     the input message.
    ///
    /// Raises
    /// ------
    /// ValueError
    ///     If a position in the message is greater or equal to the length of the code.
    #[text_signature = "(self, message)"]
    pub fn syndrome_of(&self, message: PyRef<PyBinaryVector>) -> PyResult<PyBinaryVector> {
        Ok(self.inner.syndrome_of(&message.inner).into())
    }

    /// Checks if the given message is a codeword of the code.
    ///
    /// Parameters
    /// ----------
    /// message: list of int
    ///     The positions with value 1 in the message.
    ///
    /// Returns
    /// -------
    /// bool
    ///     True if the message has the right length and a zero syndrome
    ///     or False otherwise.
    #[text_signature = "(self, message)"]
    pub fn has_codeword(&self, message: PyRef<PyBinaryVector>) -> bool {
        self.inner.has_codeword(&message.inner)
    }

    /// Checks if the other code defined the same codespace
    /// as this code.
    ///
    /// Parameters
    /// ----------
    /// other: LinearCode
    ///     The code to compare.
    ///
    /// Returns
    /// -------
    /// bool
    ///     True if other codewords are exactly the same
    ///     as this code codewords.
    #[text_signature = "(self, other)"]
    pub fn has_same_codespace_as(&self, other: PyRef<Self>) -> bool {
        self.inner.has_same_codespace_as(&other.inner)
    }

    pub fn __setstate__(&mut self, py: Python, state: PyObject) -> PyResult<()> {
        match state.extract::<&PyBytes>(py) {
            Ok(s) => serde_pickle::from_slice(s.as_bytes())
                .map(|(inner, tag)| {
                    self.inner = inner;
                    self.tag = tag;
                })
                .map_err(|error| PyValueError::new_err(error.to_string())),
            Err(e) => Err(e),
        }
    }

    pub fn __getstate__(&self, py: Python) -> PyResult<PyObject> {
        Ok(PyBytes::new(
            py,
            &serde_pickle::to_vec(&(&self.inner, &self.tag), true).unwrap(),
        )
        .to_object(py))
    }
}

#[pyproto]
impl PyObjectProtocol for PyLinearCode {
    fn __repr__(&self) -> String {
        let mut display = if self.tag != "" {
            format!("Tag = {}\n", self.tag)
        } else {
            String::new()
        };
        display.push_str(&format!(
            "Parity check matrix:\n{}\nGenerator matrix:\n{}",
            self.inner.parity_check_matrix(),
            self.inner.generator_matrix(),
        ));
        display
    }
}

#[pyproto]
impl PySequenceProtocol for PyLinearCode {
    fn __len__(&self) -> usize {
        self.inner.block_size()
    }
}
