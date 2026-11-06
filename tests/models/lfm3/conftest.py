import pytest


@pytest.fixture(autouse=True)
def runtime():
    import freetoken.core as core
    from freetoken.distributed import set_tp_info, try_get_tp_info

    if try_get_tp_info() is None:
        set_tp_info(0, 1)
    import torch
    # Fused and separate GEMMs must accumulate in fp32; cuBLAS may otherwise
    # truncate intermediate reductions differently for their different shapes.
    previous = torch.backends.cuda.matmul.allow_bf16_reduced_precision_reduction
    torch.backends.cuda.matmul.allow_bf16_reduced_precision_reduction = False
    core._GLOBAL_CTX = None
    yield
    torch.backends.cuda.matmul.allow_bf16_reduced_precision_reduction = previous
    core._GLOBAL_CTX = None


@pytest.fixture(params=["bfloat16", "float32"])
def reference_dtype(request):
    import torch
    return getattr(torch, request.param)
