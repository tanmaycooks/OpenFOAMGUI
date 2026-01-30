document.addEventListener('DOMContentLoaded', () => {
    const renderBtn = document.getElementById('renderBtn');
    const visualizeBtn = document.getElementById('visualizeBtn');
    const yamlInput = document.getElementById('yamlInput');
    const yamlOutput = document.getElementById('yamlOutput');
    const treeContainer = document.getElementById('tree-container');

    // Modal Elements
    const modal = document.getElementById('visualModal');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const dashInput = document.getElementById('dashInput');
    const dashOutput = document.getElementById('dashOutput');
    const dashTreeContainer = document.getElementById('dashTreeContainer');

    const dashUpdateBtn = document.getElementById('dashUpdateBtn');

    let currentTreeData = null; // Store for dashboard

    // --- Dashboard Update Logic ---
    dashUpdateBtn.addEventListener('click', async () => {
        const yamlContent = dashInput.value;
        const originalText = dashUpdateBtn.innerHTML;
        dashUpdateBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
        dashUpdateBtn.disabled = true;

        try {
            const response = await fetch('/process', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ yaml: yamlContent }),
            });
            const data = await response.json();

            if (response.ok) {
                renderTree(data.tree, "#dashTreeContainer");
                dashOutput.textContent = data.output_yaml || "No output generated.";
            } else {
                dashOutput.textContent = "Error: " + data.error;
            }
        } catch (error) {
            dashOutput.textContent = "Network Error: " + error.message;
        } finally {
            dashUpdateBtn.innerHTML = originalText;
            dashUpdateBtn.disabled = false;
        }
    });

    renderBtn.addEventListener('click', async () => {
        const yamlContent = yamlInput.value;
        // ... (rest of render logic is same, but I need to be careful not to delete it)


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
                currentTreeData = data.tree;
                renderTree(data.tree, "#tree-container");
                // Update Output YAML
                yamlOutput.value = data.output_yaml || "No output generated.";
            } else {
                showError(data.error);
                yamlOutput.value = "Error processing YAML.";
            }
        } catch (error) {
            showError("Network Error: " + error.message);
        } finally {
            renderBtn.innerHTML = originalText;
            renderBtn.disabled = false;
        }
    });

    // Visualize Button Logic
    visualizeBtn.addEventListener('click', () => {
        if (!currentTreeData) {
            alert("Please render a valid tree first!");
            return;
        }

        // Populate Dashboard
        dashInput.value = yamlInput.value;
        dashOutput.textContent = yamlOutput.value;

        // Show Modal
        modal.style.display = 'flex';

        // Render Tree in Dashboard (need timeout to wait for modal display for dimension calc)
        setTimeout(() => {
            renderTree(currentTreeData, "#dashTreeContainer");
        }, 100);
    });

    // Close Modal Logic
    closeModalBtn.addEventListener('click', () => {
        modal.style.display = 'none';
        // Clear dashboard tree to save memory/clean state
        d3.select("#dashTreeContainer").selectAll("*").remove();
    });

    // Close on click outside
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }

    // Auto-Run if query param loaded content
    if (yamlInput.value.trim().length > 0 && yamlInput.value.includes("root")) {
        // Auto-click render
        renderBtn.click();

        // Wait for render to complete (simple timeout)
        setTimeout(() => {
            visualizeBtn.click();
        }, 800);
    }
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

function renderTree(treeData, containerSelector) {
    const container = document.querySelector(containerSelector);
    container.innerHTML = ''; // Clear previous

    if (!treeData) return;

    // Set dimensions
    const width = container.clientWidth || 800;
    const height = container.clientHeight || 600;

    // Create SVG with Zoom
    const svg = d3.select(containerSelector).append("svg")
        .attr("width", "100%")
        .attr("height", "100%")
        .attr("viewBox", `0 0 ${width} ${height}`)
        .call(d3.zoom().on("zoom", (event) => {
            g.attr("transform", event.transform);
        }))
        .append("g");

    const g = svg.append("g");

    // Create Hierarchy
    const root = d3.hierarchy(treeData, d => {
        let kids = [];
        if (d.left) kids.push(d.left);
        if (d.right) kids.push(d.right);
        if (d.children_extra) kids = kids.concat(d.children_extra);
        return kids.length > 0 ? kids : null;
    });

    // Tree Layout - Increased Spacing for wider nodes
    // Width 160 to accommodate long names like "International"
    const nodeWidthSpace = 180;
    const nodeHeightSpace = 100;

    const treeMap = d3.tree().nodeSize([nodeWidthSpace, nodeHeightSpace]);
    treeMap(root);

    // Calculate Bounding Box to Center the Tree
    let x0 = Infinity;
    let x1 = -Infinity;

    root.each(d => {
        if (d.x < x0) x0 = d.x;
        if (d.x > x1) x1 = d.x;
    });

    // Center translation
    const centerOffset = width / 2 - (x0 + x1) / 2;
    const verticalOffset = 50;

    g.attr("transform", `translate(${centerOffset},${verticalOffset})`);

    // Links
    g.selectAll(".link")
        .data(root.links())
        .enter().append("path")
        .attr("class", "link")
        .attr("d", d3.linkVertical()
            .x(d => d.x)
            .y(d => d.y)
        );

    // Nodes Group
    const node = g.selectAll(".node")
        .data(root.descendants())
        .enter().append("g")
        .attr("class", "node")
        .attr("transform", d => `translate(${d.x},${d.y})`);

    // 1. Append Text FIRST to measure it
    // Replace underscores with spaces, no truncation
    node.append("text")
        .attr("dy", "0.35em")
        .style("text-anchor", "middle")
        .text(d => d.data.value.toString().replace(/_/g, " ")) // Formatting
        .style("font-size", "14px")
        .style("fill", "white")
        .style("pointer-events", "none")
        .style("font-weight", "500")
        .each(function (d) {
            // Calculate width for the background rect
            const bbox = this.getBBox();
            d.bbox = bbox;
        });

    // 2. Insert Rect (Pill Shape) BEHIND text
    node.insert("rect", "text")
        .attr("x", d => -(d.bbox.width + 20) / 2) // Center horizontally with padding
        .attr("y", -15) // Height is approx fixed (30px), so -15 centers it vertically relative to 0
        .attr("width", d => d.bbox.width + 20)
        .attr("height", 30)
        .attr("rx", 15) // Rounded corners (Pill)
        .attr("ry", 15)
        .style("fill", "var(--editor-bg)")
        .style("stroke", "var(--accent-primary)")
        .style("stroke-width", "2px")
        .style("transition", "all 0.3s ease");

    // Optional: Add hover effect to nodes via CSS (already present for .node:hover rect/circle)
}
