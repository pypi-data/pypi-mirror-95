"""Tests for `mlbench_core.utils.pytorch.utils` package."""
import torch

from mlbench_core.utils.pytorch.utils import orthogonalize, pack_tensors, unpack_tensors


def test_orthogonalize():
    m = torch.rand(2, 2)
    identity = torch.eye(2)

    orthogonalize(m)

    # check if m'*m = I
    assert torch.allclose(torch.matmul(m.t(), m), identity, atol=1e-04)


def test_pack_tensors():
    tensors = [torch.rand(2, 2), torch.rand(2, 2)]

    flattened = [y for x in tensors for y in x.view(-1)]

    vec, indices, sizes = pack_tensors(tensors)

    assert vec.tolist() == flattened
    assert indices == [0, 4, 8]
    assert sizes == [(2, 2), (2, 2)]


def test_unpack_tensors():
    tensors = [torch.rand(2, 2), torch.rand(2, 2)]
    vec, indices, sizes = pack_tensors(tensors)

    unpacked = unpack_tensors(vec, indices, sizes)

    assert all((x == y).all() for x, y in zip(tensors, unpacked))
