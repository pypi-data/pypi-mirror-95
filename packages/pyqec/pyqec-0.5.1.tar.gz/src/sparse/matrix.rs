use crate::sparse::PyBinaryVector;
use bincode::{deserialize, serialize};
use pyo3::class::basic::CompareOp;
use pyo3::exceptions::{PyIndexError, PyNotImplementedError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::PyBytes;
use pyo3::ToPyObject;
use pyo3::{PyMappingProtocol, PyNumberProtocol, PyObjectProtocol};
use sparse_bin_mat::SparseBinMat;
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};

#[pyclass(name = BinaryMatrix, module="pyqec.pyqec")]
#[derive(Debug, Clone)]
pub struct PyBinaryMatrix {
    pub(crate) inner: SparseBinMat,
}

impl From<SparseBinMat> for PyBinaryMatrix {
    fn from(inner: SparseBinMat) -> Self {
        Self { inner }
    }
}

#[pymethods]
impl PyBinaryMatrix {
    #[new]
    pub fn new(number_of_columns: usize, rows: Vec<Vec<usize>>) -> PyResult<Self> {
        let matrix = SparseBinMat::try_new(number_of_columns, rows)
            .map_err(|error| PyValueError::new_err(error.to_string()))?;
        Ok(Self::from(matrix))
    }

    #[staticmethod]
    pub fn identity(length: usize) -> Self {
        Self::from(SparseBinMat::identity(length))
    }

    #[staticmethod]
    pub fn zeros(number_of_rows: usize, number_of_columns: usize) -> Self {
        Self::from(SparseBinMat::zeros(number_of_rows, number_of_columns))
    }

    #[staticmethod]
    pub fn empty() -> Self {
        Self::from(SparseBinMat::empty())
    }

    pub fn number_of_columns(&self) -> usize {
        self.inner.number_of_columns()
    }

    pub fn number_of_rows(&self) -> usize {
        self.inner.number_of_rows()
    }

    pub fn dimensions(&self) -> (usize, usize) {
        self.inner.dimension()
    }

    pub fn number_of_zeros(&self) -> usize {
        self.inner.number_of_zeros()
    }

    pub fn number_of_ones(&self) -> usize {
        self.inner.number_of_ones()
    }

    pub fn is_empty(&self) -> bool {
        self.inner.is_empty()
    }

    pub fn is_zero(&self) -> bool {
        self.inner.is_zero()
    }

    pub fn rank(&self) -> usize {
        self.inner.rank()
    }

    pub fn transposed(&self) -> Self {
        self.inner.transposed().into()
    }

    pub fn echelon_form(&self) -> Self {
        self.inner.echelon_form().into()
    }

    pub fn nullspace(&self) -> Self {
        self.inner.nullspace().into()
    }

    pub fn is_zero_at(&self, row: usize, column: usize) -> PyResult<bool> {
        self.inner.is_zero_at(row, column).ok_or_else(|| {
            PyIndexError::new_err(format!(
                "row {} or column {} is out of bound for {} x {} matrix",
                row,
                column,
                self.number_of_rows(),
                self.number_of_columns()
            ))
        })
    }

    pub fn is_one_at(&self, row: usize, column: usize) -> PyResult<bool> {
        self.inner.is_one_at(row, column).ok_or_else(|| {
            PyIndexError::new_err(format!(
                "row {} or column {} is out of bound for {} x {} matrix",
                row,
                column,
                self.number_of_rows(),
                self.number_of_columns()
            ))
        })
    }

    pub fn horizontal_concat_with(&self, other: &Self) -> Self {
        self.inner.horizontal_concat_with(&other.inner).into()
    }

    pub fn vertical_concat_with(&self, other: &Self) -> Self {
        self.inner.vertical_concat_with(&other.inner).into()
    }

    pub fn dot_with_vector(&self, vector: &PyBinaryVector) -> PyResult<PyBinaryVector> {
        self.inner
            .dot_with_vector(&vector.inner)
            .map(|result| result.into())
            .map_err(|error| PyValueError::new_err(error.to_string()))
    }

    pub fn dot_with_matrix(&self, matrix: &PyBinaryMatrix) -> PyResult<PyBinaryMatrix> {
        self.inner
            .dot_with_matrix(&matrix.inner)
            .map(|result| result.into())
            .map_err(|error| PyValueError::new_err(error.to_string()))
    }

    pub fn __setstate__(&mut self, py: Python, state: PyObject) -> PyResult<()> {
        match state.extract::<&PyBytes>(py) {
            Ok(s) => {
                self.inner = deserialize(s.as_bytes()).unwrap();
                Ok(())
            }
            Err(e) => Err(e),
        }
    }

    pub fn __getstate__(&self, py: Python) -> PyResult<PyObject> {
        Ok(PyBytes::new(py, &serialize(&self.inner).unwrap()).to_object(py))
    }
}

#[pyproto]
impl PyObjectProtocol for PyBinaryMatrix {
    fn __repr__(&self) -> String {
        self.inner.to_string()
    }

    fn __richcmp__(&self, other: PyRef<Self>, op: CompareOp) -> PyResult<bool> {
        match op {
            CompareOp::Eq => Ok(&self.inner == &other.inner),
            CompareOp::Ne => Ok(&self.inner != &other.inner),
            _ => Err(PyNotImplementedError::new_err("not implemented")),
        }
    }

    fn __hash__(&self) -> u64 {
        let mut hasher = DefaultHasher::new();
        self.inner.hash(&mut hasher);
        hasher.finish()
    }
}

#[pyproto]
impl PyNumberProtocol for PyBinaryMatrix {
    fn __add__(lhs: PyRef<Self>, rhs: PyRef<Self>) -> PyResult<Self> {
        lhs.inner
            .bitwise_xor_with(&rhs.inner)
            .map(|matrix| matrix.into())
            .map_err(|error| PyValueError::new_err(error.to_string()))
    }
}

#[pyproto]
impl PyMappingProtocol for PyBinaryMatrix {
    fn __getitem__(&'p self, indices: (isize, isize)) -> PyResult<u8> {
        if indices.0 < -1 * self.number_of_rows() as isize
            || indices.1 < -1 * self.number_of_columns() as isize
        {
            return Err(PyIndexError::new_err(format!(
                "invalid indices {:?} for {} x {} matrix",
                indices,
                self.number_of_rows(),
                self.number_of_columns()
            )));
        }
        let row = if indices.0 < 0 {
            -1 * indices.0
        } else {
            indices.0
        } as usize;
        let column = if indices.1 < 0 {
            -1 * indices.1
        } else {
            indices.1
        } as usize;
        self.inner.get(row, column).ok_or_else(|| {
            PyIndexError::new_err(format!(
                "invalid indices {:?} for {} x {} matrix",
                indices,
                self.number_of_rows(),
                self.number_of_columns()
            ))
        })
    }
}
