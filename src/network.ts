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

const colors: Record<string, string> = {
    "year": "#d97706",
    "bibl": "#1d4ed8",
    "author": "#10a633",
    "place": "#9333ea",
    "org": "#db2777"
}
const forceAtlas2TimeOut = 5000
const allNodesByType = new Map<string, typeof data.nodes>();
for (const node of data.nodes) {
    const existing = allNodesByType.get(node.type) ?? [];
    existing.push(node);
    allNodesByType.set(node.type, existing);
}

graph_container.style.height = "70vh";
graph_container.style.width = "100%";
for (const node of data.nodes) {
    if (graph.hasNode(node.id)) continue;
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

const MIN_NODE_SIZE = 3;
const MAX_NODE_SIZE = 14;

const updateNodeSizes = () => {
    if (graph.order === 0) return;

    let minDegree = Infinity;
    let maxDegree = -Infinity;

    graph.forEachNode((node) => {
        const degree = graph.degree(node);
        if (degree < minDegree) minDegree = degree;
        if (degree > maxDegree) maxDegree = degree;
    });

    const degreeRange = maxDegree - minDegree;

    graph.forEachNode((node) => {
        const degree = graph.degree(node);
        const normalized = degreeRange === 0 ? 0.5 : (degree - minDegree) / degreeRange;
        const size = MIN_NODE_SIZE + normalized * (MAX_NODE_SIZE - MIN_NODE_SIZE);
        graph.setNodeAttribute(node, "size", size);
    });
};

updateNodeSizes();

const sensibleSettings = forceAtlas2.inferSettings(graph);
const fa2Layout = new FA2Layout(graph, {
    settings: sensibleSettings,
});
let forceAtlasStopTimer: ReturnType<typeof setTimeout> | null = null;

const rerunForceAtlasLayout = (durationMs = 5000) => {
    if (forceAtlasStopTimer) {
        clearTimeout(forceAtlasStopTimer);
        forceAtlasStopTimer = null;
    }

    if (graph.order === 0) {
        fa2Layout.stop();
        return;
    }

    fa2Layout.start();
    forceAtlasStopTimer = setTimeout(() => {
        fa2Layout.stop();
        forceAtlasStopTimer = null;
    }, durationMs);
};

rerunForceAtlasLayout();
new Sigma(graph, graph_container);

let legendDiv = document.getElementById("legendDiv");
if (!(legendDiv instanceof HTMLElement)) {
    throw new Error("Element #legendDiv not found");
}

const setTypeVisibility = (type: string, visible: boolean) => {
    const nodesOfType = allNodesByType.get(type) ?? [];

    if (!visible) {
        for (const node of nodesOfType) {
            if (graph.hasNode(node.id)) {
                graph.dropNode(node.id);
            }
        }
        updateNodeSizes();
        rerunForceAtlasLayout(forceAtlas2TimeOut);
        return;
    }

    for (const node of nodesOfType) {
        if (graph.hasNode(node.id)) continue;
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

    updateNodeSizes();
    rerunForceAtlasLayout(forceAtlas2TimeOut);
};


for (const [nodeType, nodeColor] of Object.entries(colors)) {
    if (nodeType != 'bibl'){
        let radioDiv = document.createElement("div");
    legendDiv.append(radioDiv)
    radioDiv.classList.add("form-check", "form-switch")
    let legendInput = document.createElement("input")
    radioDiv.append(legendInput)
    legendInput.classList.add("form-check-input")
    legendInput.type = "checkbox";
    legendInput.id = `input-${nodeType}`
    legendInput.checked = true;
    legendInput.addEventListener("change", () => {
        setTypeVisibility(nodeType, legendInput.checked);
    });

    let legendInputLabel = document.createElement("label")
    radioDiv.append(legendInputLabel)
    legendInputLabel.textContent = `${nodeType}`
    legendInputLabel.id = `label-input-${nodeType}`
    legendInputLabel.htmlFor = `input-${nodeType}`
    legendInputLabel.style.color = nodeColor

    }
    
    
}
