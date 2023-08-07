import commands.modules.postprocess as postprocess


def test_postprocess_fetch_field():
    assert postprocess.postprocess_fetch_field("hi") == "hi"
    assert postprocess.postprocess_fetch_field("") == ""
    assert (
        postprocess.postprocess_fetch_field(["a", "b", "c"]) == "* a\n* b\n* c"
    )


def test_postprocess_fetch_item_returns_str():
    """Since discord msgs only accept strings, this function should return only strings."""
    input_dict = {"title": "a", "blurb": "b", "desc": "c", "links": "d"}
    assert type(postprocess.postprocess_fetch_item(input_dict)) is str
