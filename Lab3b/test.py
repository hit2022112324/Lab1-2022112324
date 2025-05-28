def test_tc1_bridge_exists(G1):
    input_text = "i you"
    print("TC1 input: G1, text =", input_text)
    result = generate_new_text(G1, input_text)
    print("TC1 output:", result)
    assert result == "i love you"

def test_tc2_no_bridge():
    G2 = nx.DiGraph()
    G2.add_edge("a", "b", weight=1)
    input_text = "x y"
    print("TC2 input: G2, text =", input_text)
    result = generate_new_text(G2, input_text)
    print("TC2 output:", result)
    assert result == "x y"
def test_tc3_short_text(G1, text):
    print(f"TC3 input: G1, text='{text}'")
    result = generate_new_text(G1, text)
    print("TC3 output:", result)
    assert result == text
def test_tc4_invalid_G_none():
    input_text = "i you"
    print("TC4 input: G=None, text =", input_text)
    with pytest.raises(TypeError) as exc_info:
        generate_new_text(None, input_text)
    print("TC4 raised:", type(exc_info.value).__name__)
def test_tc5_invalid_text_none(G1):
    print("TC5 input: G1, text=None")
    with pytest.raises(AttributeError) as exc_info:
        generate_new_text(G1, None)
    print(f"TC5 raised: {type(exc_info.value).__name__}: {exc_info.value}")
def test_tc6_invalid_text_type(G1, bad_text):
    print("TC6 input: G1, bad_text =", bad_text)
    with pytest.raises(AttributeError) as exc_info:
        generate_new_text(G1, bad_text)
    print(f"TC6 raised: {type(exc_info.value).__name__}: {exc_info.value}")