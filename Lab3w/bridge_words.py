def find_bridge_words(G, word1, word2):
    if word1 not in G or word2 not in G:
        print("词汇不存在于图中")
        return
    bridges = [w3 for w3 in G.successors(word1) if G.has_edge(w3, word2)]
    if bridges:
        print(f"'{word1}' 与 '{word2}' 的桥接词：{', '.join(bridges)}")
    else:
        print("无桥接词")