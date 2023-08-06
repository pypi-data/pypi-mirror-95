use pyo3::prelude::*;

mod linear_code;
use linear_code::{random_regular_code, PyLinearCode};

mod noise;
use noise::PyBinarySymmetricChannel;

mod flip_decoder;
use flip_decoder::PyFlipDecoder;

mod randomness;

mod sparse;
use sparse::{PyBinaryMatrix, PyBinaryVector};

/// A toolbox for classical (and soon quantum) error correction.
#[pymodule]
fn pyqec(_py: Python, module: &PyModule) -> PyResult<()> {
    module.add_class::<PyLinearCode>()?;
    module.add_class::<PyBinarySymmetricChannel>()?;
    module.add_class::<PyFlipDecoder>()?;
    module.add_class::<PyBinaryMatrix>()?;
    module.add_class::<PyBinaryVector>()?;

    /// Samples a random regular codes.
    ///
    /// Parameters
    /// ----------
    /// block_size: int, default = 4
    ///     The number of bits in the code.
    /// number_of_checks: int, default = 3
    ///     The number of checks in the code.
    /// bit_degree: int, default = 3
    ///     The number of checks connected to each bit.
    /// check_degree: int, default = 4
    ///     The number of bits connected to each check.
    /// random_seed: int, optional
    ///     A seed to feed the random number generator.
    ///     By default, the rng is initialize from entropy.
    /// tag: string, option
    ///     An identifier for the code.
    ///
    /// Returns
    /// -------
    /// LinearCode
    ///     A random linear code with the given parameters.
    ///
    /// Raises
    /// ------
    /// ValueError
    ///     If `block_size * bit_degree != number_of_checks * check_degree`.
    #[pyfn(
        module,
        "random_regular_code",
        block_size = 4,
        number_of_checks = 3,
        bit_degree = 3,
        check_degree = 4
    )]
    fn py_random_regular_code(
        block_size: usize,
        number_of_checks: usize,
        bit_degree: usize,
        check_degree: usize,
        random_seed: Option<u64>,
        tag: Option<String>,
    ) -> PyResult<PyLinearCode> {
        random_regular_code(
            block_size,
            number_of_checks,
            bit_degree,
            check_degree,
            random_seed,
            tag,
        )
    }
    Ok(())
}
