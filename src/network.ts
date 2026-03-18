import Graph from "graphology";
import forceAtlas2 from "graphology-layout-forceatlas2";
import FA2Layout from "graphology-layout-forceatlas2/worker";

import Sigma from "sigma";
import data from './data/network.json'

const graph = new Graph();

const graph_container = document.getElementById('visContainer')
if (!(graph_container instanceof HTMLElement)) {
    throw new Error("Element #visContainer not found");
}

const colors = {
    "year": "#d97706",
    "bibl": "#1d4ed8",
    "author": "#10a633",
    "place": "#9333ea",
}

graph_container.style.height = "70vh";
graph_container.style.width = "90%";


for (const node of data.nodes) {
    if (graph.hasNode(node.id)) continue;

    const isYear = node.type === "year";
    graph.addNode(node.id, {
        label: node.label,
        x: Math.random(),
        y: Math.random(),
        color: colors[node.type],
    });
}

for (const [source, target] of data.edges) {
    if (!graph.hasNode(source) || !graph.hasNode(target)) continue;
    if (graph.hasEdge(source, target)) continue;

    graph.addEdge(source, target, { size: 1, color: "#9ca3af" });
}

const sensibleSettings = forceAtlas2.inferSettings(graph);
const fa2Layout = new FA2Layout(graph, {
    settings: sensibleSettings,
});
 fa2Layout.start();
new Sigma(graph, graph_container);