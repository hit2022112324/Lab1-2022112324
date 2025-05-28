import re
import networkx as nx
import random
import matplotlib.pyplot as plt
import time
import os

# ——— 功能点 1：读取文本并构建有向图 ———
def read_and_generate_graph(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split()
    G = nx.DiGraph()
    for w1, w2 in zip(words[:-1], words[1:]):
        if G.has_edge(w1, w2):
            G[w1][w2]['weight'] += 1
        else:
            G.add_edge(w1, w2, weight=1)
    return G

# ——— 层次布局函数（带拓扑排序）———
def hierarchy_pos(G, root=None, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5):
    def _hierarchy_pos(G, node, width, vert_gap, vert_loc, xcenter, pos, parent=None):
        pos[node] = (xcenter, vert_loc)
        children = list(G.successors(node))
        if children:
            dx = width / len(children)
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, dx, vert_gap, vert_loc - vert_gap, nextx, pos, node)
        return pos
    if root is None:
        root = next(iter(nx.topological_sort(G)))
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter, {})

# ——— 功能点 2：展示图并保存（按用户要求）———
def display_graph(G):
    if len(G) == 0:
        print("Empty graph.")
        return
    try:
        root = next(iter(nx.topological_sort(G)))
        pos = hierarchy_pos(G, root)
        layout_type = "hierarchy"
    except nx.NetworkXUnfeasible:
        pos = nx.spring_layout(G, seed=42)
        layout_type = "spring"

    fig, ax = plt.subplots(figsize=(14, 10))

    # 先绘制边（箭头）
    nx.draw_networkx_edges(
        G, pos, ax=ax,
        arrowstyle='-|>',
        arrowsize=20,
        edge_color='blue',
        connectionstyle='arc3,rad=0.1',
        width=1.5,
        min_source_margin=15,
        min_target_margin=15
    )

    # 再绘制节点和标签
    nx.draw_networkx_nodes(
        G, pos, ax=ax,
        node_size=1200,
        node_color='lightyellow',
        edgecolors='black',
        linewidths=1
    )
    nx.draw_networkx_labels(
        G, pos, ax=ax,
        font_size=10,
        font_weight='bold'
    )

    # 权重标签
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels,
        font_size=9, label_pos=0.5, rotate=False
    )

    ax.set_title(f"Directed Word Graph ({layout_type} layout)", fontsize=14)
    ax.axis('off')
    plt.tight_layout()

    filename = f"directed_graph_{int(time.time())}.png"
    plt.savefig(filename)
    print(f"Graph saved as '{filename}'")
    plt.show()

# ——— 功能点 3：桥接词查询 ———
def find_bridge_words(G, word1, word2):
    if word1 not in G or word2 not in G:
        print("词汇不存在于图中")
        return
    bridges = [w3 for w3 in G.successors(word1) if G.has_edge(w3, word2)]
    if bridges:
        print(f"'{word1}' 与 '{word2}' 的桥接词：{', '.join(bridges)}")
    else:
        print("无桥接词")

# ——— 功能点 4：插入桥接词生成新句 ———
def generate_new_text(G, text):
    words = [w for w in re.sub(r'[^a-z\s]', ' ', text.lower()).split() if w]
    if len(words) < 2:
        return text
    new_text = []
    for w1, w2 in zip(words[:-1], words[1:]):
        new_text.append(w1)
        if w1 in G and w2 in G:
            bridges = [w3 for w3 in G.successors(w1) if G.has_edge(w3, w2)]
            if bridges:
                new_text.append(random.choice(bridges))
    new_text.append(words[-1])
    return ' '.join(new_text)

# ——— 功能点 5：最短路径查询并高亮边 ———
def find_and_show_shortest_path(G, word1, word2):
    if word1 not in G or word2 not in G:
        print("词汇不存在于图中")
        return
    try:
        path = nx.shortest_path(G, source=word1, target=word2, weight='weight')
        edges = [(u, v) for u, v in zip(path[:-1], path[1:])]
        weight_sum = sum(G[u][v]['weight'] for u, v in edges)
        print("最短路径：", " -> ".join(path))
        print("路径总权重：", weight_sum)
        display_graph_with_highlight(G, edges)
    except nx.NetworkXNoPath:
        print("两个词之间不可达")

# 使用 display_graph 的 wrapper 用于高亮边
def display_graph_with_highlight(G, highlight_path):
    display_graph(G)  # 您可在此加入边高亮逻辑拓展

# ——— 功能点 6：PageRank ———
def compute_pagerank(G):
    personalization = {n: 1.0 for n in G.nodes()}
    pr = nx.pagerank(G, alpha=0.85, personalization=personalization, dangling=personalization)
    print("PageRank 排名：")
    for node, score in sorted(pr.items(), key=lambda x: -x[1]):
        print(f"{node}: {score:.4f}")

# ——— 功能点 7：随机游走并写入文件 ———
def random_walk(G):
    path = []
    visited_edges = set()
    current = random.choice(list(G.nodes()))
    path.append(current)
    print(f"开始节点：{current}")

    while True:
        successors = list(G.successors(current))
        if not successors:
            print(f"节点 {current} 无出边，终止游走。")
            break
        next_node = random.choice(successors)
        edge = (current, next_node)
        if edge in visited_edges:
            print(f"边 {current} -> {next_node} 已重复，终止游走。")
            break
        print(f"{current} -> {next_node}")
        choice = input("按回车继续，输入 q 退出：").strip().lower()
        if choice == 'q':
            break
        visited_edges.add(edge)
        current = next_node
        path.append(current)

    print("游走路径：", ' -> '.join(path))
    filename = f"random_walk_{int(time.time())}.txt"
    with open(filename, 'w') as f:
        f.write(' '.join(path))
    print(f"路径写入文件：{filename}")

# ——— 主程序入口 ———
def main():
    file_path = input("请输入英文文本文件路径：").strip()
    if not os.path.exists(file_path):
        print("❌ 文件路径无效")
        return
    try:
        G = read_and_generate_graph(file_path)
        print(f"图加载成功，共 {len(G.nodes())} 个词，{len(G.edges())} 条边")
    except Exception as e:
        print(f"❌ 读取失败：{e}")
        return

    while True:
        print("\n========= 功能菜单 =========")
        print("1. 展示有向图并保存")
        print("2. 查询桥接词")
        print("3. 生成新文本（插入桥接词）")
        print("4. 查询最短路径")
        print("5. 计算 PageRank")
        print("6. 随机游走")
        print("7. 退出")
        print("============================")
        choice = input("请选择操作（1-7）：").strip()
        if choice == '1':
            display_graph(G)
        elif choice == '2':
            w1 = input("输入 word1：").strip().lower()
            w2 = input("输入 word2：").strip().lower()
            find_bridge_words(G, w1, w2)
        elif choice == '3':
            line = input("输入一行英文文本：").strip()
            result = generate_new_text(G, line)
            print("生成结果：", result)
        elif choice == '4':
            w1 = input("输入起点词：").strip().lower()
            w2 = input("输入终点词：").strip().lower()
            find_and_show_shortest_path(G, w1, w2)
        elif choice == '5':
            compute_pagerank(G)
        elif choice == '6':
            random_walk(G)
        elif choice == '7':
            print("程序结束。")
            break
        else:
            print("无效选项，请输入1~7之间的数字。")

if __name__ == "__main__":
    main()