# test_bridge_words.py
import networkx as nx
from bridge_words import find_bridge_words 




def test_TC01_word_not_in_graph(capsys):
    G = nx.DiGraph()  # 空图
    find_bridge_words(G, "apple", "banana")
    captured = capsys.readouterr()
    assert "词汇不存在于图中" in captured.out

def test_TC02_bridge_exists(capsys):
    G = nx.DiGraph()
    G.add_edges_from([("apple", "sweet"), ("sweet", "banana")])
    find_bridge_words(G, "apple", "banana")
    captured = capsys.readouterr()
    assert "'apple' 与 'banana' 的桥接词：sweet" in captured.out  # 正确断言

def test_TC03_no_bridge(capsys):
    G = nx.DiGraph()
    G.add_edges_from([
        ("apple", "juice"),
        ("juice", "orange"),
        ("apple", "fruit")
    ])
    G.add_node("banana")  # 确保 banana 存在于图中，但没有可达路径
    find_bridge_words(G, "apple", "banana")
    captured = capsys.readouterr()
    assert "无桥接词" in captured.out
