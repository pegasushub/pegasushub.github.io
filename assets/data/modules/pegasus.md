## 1. The Big Picture

Welcome to the masterclass! To truly understand the **Pegasus Workflow Management System (WMS)**, you first need to understand the massive problem it solves for scientists, engineers, and data analysts.

Imagine you have 10,000 high-resolution images of galaxies, and you need to run a Python script to analyze each one. Doing this sequentially on your laptop would take years. You need to run this on a massive supercomputer or cloud cluster. But doing that manually is a nightmare. How do you reliably move 10,000 files? What if Server #443 crashes halfway through?

**Pegasus WMS is the automated manager that handles all of this for you.**

<div>
<svg class="svg-graphic" viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
<rect x="30" y="125" width="100" height="50" rx="8" fill="var(--surface)" stroke="var(--text-muted)" stroke-width="2"/>
<text x="80" y="155" fill="var(--text-main)" font-family="sans-serif" font-size="14" text-anchor="middle" font-weight="bold">User Code</text>
<rect x="230" y="40" width="220" height="220" rx="16" fill="var(--surface)" stroke="var(--primary)" stroke-width="3" filter="drop-shadow(0 0 10px var(--primary-glow))"/>
<text x="340" y="75" fill="var(--primary)" font-family="sans-serif" font-size="18" text-anchor="middle" font-weight="bold">Pegasus Planner</text>
<rect x="260" y="100" width="160" height="30" rx="6" fill="var(--code-bg)" stroke="#818cf8"/>
<text x="340" y="119" fill="var(--text-muted)" font-family="sans-serif" font-size="12" text-anchor="middle">1. Replica Catalog</text>
<rect x="260" y="145" width="160" height="30" rx="6" fill="var(--code-bg)" stroke="#818cf8"/>
<text x="340" y="164" fill="var(--text-muted)" font-family="sans-serif" font-size="12" text-anchor="middle">2. Transform Catalog</text>
<rect x="260" y="190" width="160" height="30" rx="6" fill="var(--code-bg)" stroke="#818cf8"/>
<text x="340" y="209" fill="var(--text-muted)" font-family="sans-serif" font-size="12" text-anchor="middle">3. Site Catalog</text>
<rect x="550" y="40" width="200" height="220" rx="12" fill="var(--code-bg)" stroke="var(--success)" stroke-width="2"/>
<text x="650" y="75" fill="var(--success)" font-family="sans-serif" font-size="18" text-anchor="middle" font-weight="bold">Compute Grid</text>
<rect x="580" y="100" width="60" height="60" rx="6" fill="var(--surface)" stroke="var(--success)"/>
<rect x="660" y="100" width="60" height="60" rx="6" fill="var(--surface)" stroke="var(--success)"/>
<rect x="580" y="170" width="60" height="60" rx="6" fill="var(--surface)" stroke="var(--success)"/>
<rect x="660" y="170" width="60" height="60" rx="6" fill="var(--surface)" stroke="var(--success)"/>
<path d="M 130 150 L 220 150" fill="none" stroke="var(--text-muted)" stroke-width="2" marker-end="url(#arrow-muted)"/>
<path d="M 450 150 L 540 150" fill="none" stroke="var(--primary)" stroke-width="3" stroke-dasharray="6,4" marker-end="url(#arrow-primary)"/>
<text x="495" y="140" fill="var(--primary)" font-family="sans-serif" font-size="12" text-anchor="middle" font-weight="bold">Exec DAG</text>
<defs>
<marker id="arrow-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 0 L 10 5 L 0 10 z" fill="var(--text-muted)" />
</marker>
<marker id="arrow-primary" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 0 L 10 5 L 0 10 z" fill="var(--primary)" />
</marker>
</defs>
</svg>
</div>

<div class="highlight-box">
<h3><i class="fas fa-lightbulb"></i> The Abstraction Principle</h3>
<p style="margin:0; font-size: 0.95rem;">Pegasus is built entirely on the philosophy of <b>Separation of Concerns</b>. When you write a workflow, you do not write physical instructions. You simply declare your intentions: <i>"I have a conceptual file `data.csv`. I want to run `analyze.py`. Please produce `result.txt`."</i> Because your workflow is abstract, you can run the exact same code on your laptop today, and on an AWS cluster tomorrow, without changing a single line!</p>
</div>

## 2. The Replica Catalog

In Pegasus, data files have a split personality. To achieve true portability, files are divided into a **Logical File Name (LFN)** and a **Physical File Name (PFN)**.

- **LFN (Logical):** The name of the file as your workflow thinks of it (e.g., `input_data.csv`).
- **PFN (Physical):** The actual URL or file path where the file exists in the real world (e.g., `s3://aws-bucket/data.csv`).

<div>
<svg class="svg-graphic" viewBox="0 0 800 240" xmlns="http://www.w3.org/2000/svg">
<rect x="100" y="80" width="120" height="80" rx="8" fill="var(--surface)" stroke="var(--primary)" stroke-width="2"/>
<text x="160" y="115" fill="var(--text-main)" font-family="monospace" font-size="14" text-anchor="middle" font-weight="bold">data.csv</text>
<text x="160" y="135" fill="var(--text-muted)" font-family="sans-serif" font-size="12" text-anchor="middle">(Logical Name)</text>
<rect x="340" y="40" width="120" height="160" rx="12" fill="var(--code-bg)" stroke="#818cf8" stroke-width="2"/>
<text x="400" y="115" fill="#818cf8" font-family="sans-serif" font-size="14" text-anchor="middle" font-weight="bold">Replica</text>
<text x="400" y="135" fill="#818cf8" font-family="sans-serif" font-size="14" text-anchor="middle" font-weight="bold">Catalog</text>
<rect x="560" y="40" width="200" height="40" rx="6" fill="var(--surface)" stroke="var(--success)" stroke-width="2"/>
<text x="660" y="65" fill="var(--success)" font-family="monospace" font-size="12" text-anchor="middle">s3://aws-bucket/data.csv</text>
<rect x="560" y="100" width="200" height="40" rx="6" fill="var(--surface)" stroke="var(--success)" stroke-width="2"/>
<text x="660" y="125" fill="var(--success)" font-family="monospace" font-size="12" text-anchor="middle">http://server.edu/data.csv</text>
<rect x="560" y="160" width="200" height="40" rx="6" fill="var(--surface)" stroke="var(--success)" stroke-width="2"/>
<text x="660" y="185" fill="var(--success)" font-family="monospace" font-size="12" text-anchor="middle">file:///tmp/local/data.csv</text>
<path d="M 220 120 L 330 120" fill="none" stroke="#818cf8" stroke-width="2" marker-end="url(#arrow-accent)"/>
<path d="M 460 120 Q 500 120 550 60" fill="none" stroke="var(--success)" stroke-width="2" marker-end="url(#arrow-success)"/>
<path d="M 460 120 L 550 120" fill="none" stroke="var(--success)" stroke-width="2" marker-end="url(#arrow-success)"/>
<path d="M 460 120 Q 500 120 550 180" fill="none" stroke="var(--success)" stroke-width="2" marker-end="url(#arrow-success)"/>
<defs>
<marker id="arrow-accent" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#818cf8" /></marker>
<marker id="arrow-success" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="var(--success)" /></marker>
</defs>
</svg>
</div>

<div class="code-container">
<pre><code class="language-python"># How to write it in Python API
from Pegasus.api import *
rc = ReplicaCatalog()
input_file = File("data.csv")
rc.add_replica("local", input_file, "/home/ubuntu/project/data.csv")
wf.add_replica_catalog(rc)</code></pre>
</div>

## 3. The Transformation Catalog

Just like data files, the actual software programs (Python scripts, C++ executables) you want to run are abstracted. The Transformation Catalog (TC) maps a logical software name to its physical executable location or container.

If your workflow needs to run a Python script to clean data, you do not tell the workflow to run `/home/user/scripts/clean.py`. You tell it to run a logical transformation called `clean_data`.

<div class="code-container">
<pre><code class="language-python"># Define the physical location of the software
preprocess_script = Transformation(
    name="clean_data",
    site="local",
    pfn="/home/ubuntu/project/bin/clean.py",
    is_stageable=True
)
# Add it to the catalog
tc = TransformationCatalog()
tc.add_transformations(preprocess_script)
wf.add_transformation_catalog(tc)</code></pre>
</div>

## 4. The Site Catalog

A **Site** in Pegasus is a location where jobs can be executed, or where data can be stored securely. In beginner workflows, you mostly use `"local"`. In advanced grids, you might use `"condorpool"` for execution and `"aws_s3"` for storage.

When defining a site, you must provide two specific directories to orchestrate data movement safely:

- **Scratch Directory:** A temporary, high-speed workspace. Pegasus moves data here, runs code, and creates temporary files. It is wiped clean when done.
- **Storage Directory:** The safe zone. Pegasus moves "final" output files here to be preserved securely.

<div>
<svg class="svg-graphic" viewBox="0 0 800 240" xmlns="http://www.w3.org/2000/svg">
<rect x="50" y="60" width="120" height="120" rx="8" fill="var(--code-bg)" stroke="var(--primary)" stroke-width="2"/>
<text x="110" y="90" fill="var(--text-main)" font-family="sans-serif" font-size="14" text-anchor="middle" font-weight="bold">Submit Site</text>
<text x="110" y="110" fill="var(--text-muted)" font-family="sans-serif" font-size="12" text-anchor="middle">(Your Laptop)</text>
<rect x="70" y="130" width="80" height="30" rx="4" fill="var(--surface)" stroke="var(--border)"/>
<text x="110" y="150" fill="var(--primary)" font-family="monospace" font-size="12" text-anchor="middle">Input Data</text>
<rect x="340" y="40" width="160" height="160" rx="12" fill="var(--surface)" stroke="var(--text-muted)" stroke-width="2"/>
<text x="420" y="75" fill="var(--text-main)" font-family="sans-serif" font-size="14" text-anchor="middle" font-weight="bold">Execution Site</text>
<text x="420" y="95" fill="var(--text-muted)" font-family="sans-serif" font-size="12" text-anchor="middle">"condorpool"</text>
<rect x="360" y="120" width="120" height="40" rx="6" fill="var(--code-bg)" stroke="#ef4444" stroke-width="2"/>
<text x="420" y="145" fill="#ef4444" font-family="monospace" font-size="14" text-anchor="middle" font-weight="bold">/scratch</text>
<rect x="630" y="60" width="120" height="120" rx="8" fill="var(--code-bg)" stroke="var(--success)" stroke-width="2"/>
<text x="690" y="90" fill="var(--text-main)" font-family="sans-serif" font-size="14" text-anchor="middle" font-weight="bold">Storage Site</text>
<rect x="650" y="130" width="80" height="30" rx="4" fill="var(--surface)" stroke="var(--success)"/>
<text x="690" y="150" fill="var(--success)" font-family="monospace" font-size="12" text-anchor="middle">/outputs</text>
<path d="M 170 145 L 350 145" fill="none" stroke="var(--primary)" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#arrow-primary)"/>
<text x="260" y="135" fill="var(--primary)" font-family="sans-serif" font-size="12" text-anchor="middle" font-weight="bold">Stage-In</text>
<path d="M 480 145 L 640 145" fill="none" stroke="var(--success)" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#arrow-success)"/>
<text x="560" y="135" fill="var(--success)" font-family="sans-serif" font-size="12" text-anchor="middle" font-weight="bold">Stage-Out</text>
</svg>
</div>

## 5. Building the DAG

Finally, we construct the **Directed Acyclic Graph (DAG)**. This is the blueprint that links the data files to the software transformations. Because Pegasus tracks which job inputs rely on which job outputs, it automatically connects the edges of the DAG for you!

<div class="code-container">
<pre><code class="language-python"># Create the Workflow object
wf = Workflow("my-first-pipeline")
# Define a File object for the output
output_file = File("result.txt")
# Create a Job using the logical transformation name
job = Job("clean_data")
job.add_inputs(input_file)
job.add_outputs(output_file)
# Add the job to the workflow
wf.add_jobs(job)
# Plan and Execute!
wf.plan(submit=True)</code></pre>
</div>

<div class="highlight-box" style="border-color: var(--success); background: rgba(16, 185, 129, 0.1);">
<h3 style="color: var(--success);"><i class="fas fa-trophy"></i> Masterclass Complete!</h3>
<p style="margin:0; font-size: 0.95rem;">You now understand the core abstraction architecture of the Pegasus Workflow Management System. Check out the <b>Data Splitting</b> or <b>Hierarchical Workflows</b> sections to see these concepts applied to real-world parallel computing!</p>
</div>
