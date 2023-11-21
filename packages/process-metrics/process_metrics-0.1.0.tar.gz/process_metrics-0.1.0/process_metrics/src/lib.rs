use opentelemetry::{
    global,
    metrics::{self},
};
use opentelemetry_system_metrics::init_process_observer;

use opentelemetry_otlp::{ExportConfig, WithExportConfig};
use opentelemetry_sdk::{metrics::MeterProvider, runtime};
use pyo3::prelude::*;
use tokio::runtime::{Builder, Runtime};

fn init_metrics(endpoint: Option<String>) -> metrics::Result<MeterProvider> {
    let endpoint = match (
        endpoint,
        std::env::var("OTEL_EXPORTER_OTLP_METRICS_ENDPOINT"),
    ) {
        (Some(endpoint), _) => endpoint,
        (None, Ok(endpoint)) => endpoint,
        (None, Err(_)) => "http://localhost:4317".to_string(),
    };

    let export_config = ExportConfig {
        endpoint,
        ..ExportConfig::default()
    };

    opentelemetry_otlp::new_pipeline()
        .metrics(runtime::Tokio)
        .with_exporter(
            opentelemetry_otlp::new_exporter()
                .tonic()
                .with_export_config(export_config),
        )
        .build()
}

#[pyclass]
struct PyRuntime(Runtime);

/// Init the process metrics with optionally a given endpoint
#[pyfunction]
fn init(endpoint: Option<String>) -> PyResult<PyRuntime> {
    let rt = Builder::new_current_thread().build()?;
    rt.spawn(async {
        let _started = init_metrics(endpoint);
        let meter = global::meter("process-metrics");
        init_process_observer(meter).unwrap();
    });
    Ok(PyRuntime(rt))
}

/// Process metrics module
#[pymodule]
fn process_metrics(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(init, m)?)?;
    Ok(())
}
