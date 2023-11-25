use crate::streamable_struct;
use chik_streamable_macro::Streamable;

use crate::bytes::Bytes96;
use crate::chik_error;
use crate::coin_spend::CoinSpend;
use crate::streamable::Streamable;

#[cfg(feature = "py-bindings")]
use crate::from_json_dict::FromJsonDict;
#[cfg(feature = "py-bindings")]
use crate::to_json_dict::ToJsonDict;
#[cfg(feature = "py-bindings")]
use chik_py_streamable_macro::PyStreamable;
#[cfg(feature = "py-bindings")]
use pyo3::prelude::*;

streamable_struct! (SpendBundle {
    coin_spends: Vec<CoinSpend>,
    aggregated_signature: Bytes96,
});
