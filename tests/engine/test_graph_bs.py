from freetoken.engine.graph import _determine_cuda_graph_bs


def test_the_cap_gets_its_own_graph():
    # --max-running-requests 5 clamps the cap to 5: a full batch must not fall back to eager
    assert _determine_cuda_graph_bs(None, 5, 0) == [1, 2, 4, 5]
    assert _determine_cuda_graph_bs(None, 12, 0) == [1, 2, 4, 8, 12]
    assert _determine_cuda_graph_bs(None, 16, 0) == [1, 2, 4, 8, 16]
    assert _determine_cuda_graph_bs(None, 1, 0) == [1]
    assert _determine_cuda_graph_bs(None, 0, 0) == []
    assert _determine_cuda_graph_bs([1, 3], 5, 0) == [1, 3]
