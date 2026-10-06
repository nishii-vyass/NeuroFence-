from model_sandbox.report_generator import (
    ForensicReportGenerator
)


class FakeParameter:

    def __init__(self, count):

        self._count = count

    def numel(self):

        return self._count


class FakeConfig:

    model_type = "test-model"

    hidden_size = 4

    num_hidden_layers = 2

    vocab_size = 100

    torch_dtype = None


class FakeModel:

    config = FakeConfig()

    def parameters(self):

        return [

            FakeParameter(10),

            FakeParameter(20)

        ]


def test_report_contains_required_sections(
    tmp_path
):

    detection = {

        "status":
            "NO_SIGNIFICANT_TRIGGER_ANOMALY",

        "risk_level":
            "LOW",

        "method":
            "trigger_vs_normal_activation_comparison",

        "total_neurons_compared":
            4,

        "suspicious_neuron_count":
            0,

        "relative_threshold":
            0.50,

        "absolute_threshold":
            0.005
    }


    generator = ForensicReportGenerator(

        model=FakeModel(),

        model_path=tmp_path / "model",

        model_hash="abc123",

        detection_result=detection
    )


    report = generator.build_report()


    assert (
        report["tool"]
        ==
        "NeuroFence"
    )


    assert (
        report["model"]["sha256"]
        ==
        "abc123"
    )


    assert (
        report[
            "week3_detection"
        ][
            "risk_level"
        ]
        ==
        "LOW"
    )


    assert (
        "final_assessment"
        in
        report
    )