document.addEventListener('DOMContentLoaded', () => {
    const renderBtn = document.getElementById('renderBtn');
    const yamlInput = document.getElementById('yamlInput');
    const treeContainer = document.getElementById('tree-container');

    renderBtn.addEventListener('click', async () => {
        const yamlContent = yamlInput.value;

        // Slight button animation/loading state
        const originalText = renderBtn.innerHTML;
        renderBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Rendering...';
        renderBtn.disabled = true;

        try {
            const response = await fetch('/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ yaml: yamlContent }),
            });

            const data = await response.json();

            if (response.ok) {
                renderTree(data.tree);
            } else {
                showError(data.error);
            }
        } catch (error) {
            showError("Network Error: " + error.message);
        } finally {
            renderBtn.innerHTML = originalText;
            renderBtn.disabled = false;
        }
    });
});

function showError(message) {
    const container = document.getElementById('tree-container');
    container.innerHTML = `
        <div class="error-message" style="color: #ef4444; text-align: center; padding: 1rem;">
            <i class="fa-solid fa-triangle-exclamation" style="font-size: 2rem; margin-bottom: 0.5rem;"></i>
            <p>${message}</p>
        </div>
    `;
}

function renderTree(treeData) {
    const container = document.getElementById('tree-container');
    container.innerHTML = ''; // Clear previous

    if (!treeData) return;

    // Set dimensions
    const width = container.clientWidth;
    const height = container.clientHeight;

    // Create SVG
    const svg = d3.select("#tree-container").append("svg")
        .attr("width", width)
        .attr("height", height)
        .call(d3.zoom().on("zoom", (event) => {
            g.attr("transform", event.transform);
        }))
        .append("g");

    const g = svg.append("g")
        .attr("transform", `translate(${width / 2}, 50)`);

    // Convert data to D3 hierarchy
    // Our data format: { value: 10, left: {...}, right: {...} }
    // We need to transform it for D3 if we use d3.tree()
    // Or we write a custom accessor.

    // D3 hierarchy expects children array.
    // Let's create a helper to transform our binary structure to children array
    function transformData(node) {
        if (!node) return null;
        const children = [];
        if (node.left) children.push(transformData(node.left));
        if (node.right) children.push(transformData(node.right));
        // Also handle extra children if present (for bonus)
        if (node.children_extra) {
            node.children_extra.forEach(c => children.push(transformData(c)));
        }

        // Remove nulls if any (though usually we want to perhaps show empty slots? D3 tree layout handles existing nodes better)
        // If we want to strictly show Left/Right, we might need a more custom layout to preserve "emptiness"
        // For now, let's just show connected nodes.
        const cleanChildren = children.filter(c => c !== null);

        return {
            name: node.value,
            children: cleanChildren.length > 0 ? cleanChildren : null
        };
    }

    const rootData = transformData(treeData);
    if (!rootData) return; // Empty tree

    // Use d3.tree layout
    const treeLayout = d3.tree().size([width - 100, height - 100]);

    const root = d3.hierarchy(rootData);
    treeLayout(root);

    // Links
    g.selectAll(".link")
        .data(root.links())
        .enter().append("path")
        .attr("class", "link")
        .attr("d", d3.linkVertical()
            .x(d => d.x)
            .y(d => d.y)
        );

    // Nodes
    const node = g.selectAll(".node")
        .data(root.descendants())
        .enter().append("g")
        .attr("class", "node")
        .attr("transform", d => `translate(${d.x},${d.y})`);

    node.append("circle")
        .attr("r", 20);

    node.append("text")
        .attr("dy", ".35em")
        .text(d => d.data.name);
}
