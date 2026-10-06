from model_sandbox.backdoor_detector import (
    BackdoorDetector
)


def test_detector_finds_large_trigger_increase():

    normal = [

        {
            "neuron_activation_energy": {

                "layer0": [
                    0.010,
                    0.020
                ]
            }
        },

        {
            "neuron_activation_energy": {

                "layer0": [
                    0.010,
                    0.020
                ]
            }
        }
    ]


    trigger = [

        {
            "neuron_activation_energy": {

                "layer0": [
                    0.030,
                    0.020
                ]
            }
        },

        {
            "neuron_activation_energy": {

                "layer0": [
                    0.030,
                    0.020
                ]
            }
        }
    ]


    detector = BackdoorDetector(

        relative_threshold=0.50,

        absolute_threshold=0.005
    )


    result = detector.compare(

        normal,

        trigger
    )


    assert (
        result["status"]
        ==
        "SUSPICIOUS_ACTIVATION"
    )


    assert (
        result["suspicious_neuron_count"]
        >=
        1
    )


def test_detector_accepts_similar_activations():

    normal = [

        {
            "neuron_activation_energy": {

                "layer0": [
                    0.010,
                    0.020
                ]
            }
        }
    ]


    trigger = [

        {
            "neuron_activation_energy": {

                "layer0": [
                    0.011,
                    0.020
                ]
            }
        }
    ]


    detector = BackdoorDetector()


    result = detector.compare(

        normal,

        trigger
    )


    assert (
        result["status"]
        ==
        "NO_SIGNIFICANT_TRIGGER_ANOMALY"
    )


    assert (
        result["risk_level"]
        ==
        "LOW"
    )
def test_detector_rejects_invalid_relative_threshold():

    try:
        BackdoorDetector(
            relative_threshold=0,
            absolute_threshold=0.005
        )
        assert False
    except ValueError:
        assert True


def test_detector_rejects_invalid_absolute_threshold():

    try:
        BackdoorDetector(
            relative_threshold=0.50,
            absolute_threshold=0
        )
        assert False
    except ValueError:
        assert True