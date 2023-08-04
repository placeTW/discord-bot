import commands.modules.postprocess as postprocess


def test_postprocess_fetch_field():
    assert postprocess.postprocess_fetch_field("hi") == "hi"
    assert (
        postprocess.postprocess_fetch_field(["a", "b", "c"]) == "* a\n* b\n* c"
    )
