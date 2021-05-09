"""Tests for `snntorch.spikegen` module."""


import pytest
import snntorch as snn
from snntorch import spikegen
import torch


def input_(a):
    return torch.Tensor([a])


def multi_input(a, b, c, d, e):
    return torch.Tensor([a, b, c, d, e])


def identity(n):
    return torch.eye(n)


@pytest.mark.parametrize("test_input, expected", [(input_(0), 0), (input_(1), 1)])
def test_rate(test_input, expected):
    assert spikegen.rate(test_input, time_var_input=True) == expected


@pytest.mark.parametrize("test_input, expected", [(input_(1), 2), (input_(0), 0)])
def test_rate2(test_input, expected):
    assert spikegen.rate(test_input, first_spike_time=3, num_steps=5).sum() == expected


@pytest.mark.parametrize("test_input, expected", [(input_(0), 1), (input_(1), 1)])
def test_latency(test_input, expected):
    assert spikegen.latency(test_input, bypass=True).sum() == expected


@pytest.mark.parametrize(
    "test_input, expected", [(input_(0), (16, True)), (input_(1), (5, False))]
)
def test_latency_code(test_input, expected):
    spike_time, idx = spikegen.latency_code(
        test_input, first_spike_time=5, num_steps=10
    )
    assert tuple((spike_time.long(), idx)) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [(multi_input(1, 2, 2.91, 3, 3.9), multi_input(1, 1, 1, 0, 1))],
)
def test_delta(test_input, expected):
    assert torch.all(torch.eq(spikegen.delta(test_input, threshold=0.1), expected))


@pytest.mark.parametrize(
    "test_input, expected", [(identity(5), (multi_input(0, 1, 2, 3, 4)))]
)
def test_from_one_hot(test_input, expected):
    assert torch.all(torch.eq(spikegen.from_one_hot(test_input), expected))


@pytest.mark.parametrize(
    "test_input, expected",
    [(input_(4), multi_input(0, 0, 0, 0, 1))],
)
def test_target_rate(test_input, expected):
    assert torch.all(
        torch.eq(
            spikegen.targets_convert(test_input, num_classes=5, code="rate"), expected
        )
    )


@pytest.mark.parametrize(
    "test_input, expected",
    [(input_(4), multi_input(0, 0, 1, 1, 1))],
)
def test_target_rate2(test_input, expected):
    assert torch.all(
        torch.eq(
            spikegen.targets_convert(
                test_input, num_classes=5, code="rate", num_steps=5, first_spike_time=2
            )[:, 0, 4],
            expected,
        )
    )
