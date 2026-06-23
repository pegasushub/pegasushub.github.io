## 1. The Diamond Concept

Normally, when we write standard computer programs, tasks execute sequentially (Step 1, then Step 2, then Step 3). But in scientific computing, machine learning, and data processing, waiting for tasks one-by-one takes too long.

If two tasks do not rely on each other's data, **we should run them at the exact same time**.

<div>
<svg class="svg-graphic" viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
<rect x="330" y="40" width="140" height="45" rx="10" fill="var(--surface)" stroke="var(--primary)" stroke-width="2" filter="drop-shadow(0 0 8px var(--primary-glow))"/>
<text x="400" y="68" fill="var(--text-main)" font-family="sans-serif" font-size="14" text-anchor="middle" font-weight="700">preprocess</text>
<text x="400" y="30" fill="var(--text-muted)" font-family="sans-serif" font-size="12" text-anchor="middle">Input File (f.a)</text>
<path d="M 370 85 L 250 170" fill="none" stroke="var(--text-muted)" stroke-width="2" marker-end="url(#arrow-muted)"/>
<path d="M 430 85 L 550 170" fill="none" stroke="var(--text-muted)" stroke-width="2" marker-end="url(#arrow-muted)"/>
<rect x="250" y="115" width="40" height="20" rx="4" fill="var(--code-bg)" stroke="var(--border)"/>
<text x="270" y="129" fill="var(--primary)" font-family="monospace" font-size="10" text-anchor="middle">f.b1</text>
<rect x="510" y="115" width="40" height="20" rx="4" fill="var(--code-bg)" stroke="var(--border)"/>
<text x="530" y="129" fill="var(--primary)" font-family="monospace" font-size="10" text-anchor="middle">f.b2</text>
<rect x="180" y="180" width="140" height="45" rx="10" fill="var(--surface)" stroke="var(--border)" stroke-width="2"/>
<text x="250" y="208" fill="var(--text-main)" font-family="sans-serif" font-size="14" text-anchor="middle" font-weight="700">findrange_1</text>
<rect x="480" y="180" width="140" height="45" rx="10" fill="var(--surface)" stroke="var(--border)" stroke-width="2"/>
<text x="550" y="208" fill="var(--text-main)" font-family="sans-serif" font-size="14" text-anchor="middle" font-weight="700">findrange_2</text>
<text x="400" y="205" fill="var(--success)" font-family="sans-serif" font-size="12" text-anchor="middle" font-weight="bold">Parallel Execution</text>
<path d="M 250 225 L 370 310" fill="none" stroke="var(--text-muted)" stroke-width="2" marker-end="url(#arrow-muted)"/>
<path d="M 550 225 L 430 310" fill="none" stroke="var(--text-muted)" stroke-width="2" marker-end="url(#arrow-muted)"/>
<rect x="250" y="260" width="40" height="20" rx="4" fill="var(--code-bg)" stroke="var(--border)"/>
<text x="270" y="274" fill="var(--primary)" font-family="monospace" font-size="10" text-anchor="middle">f.c1</text>
<rect x="510" y="260" width="40" height="20" rx="4" fill="var(--code-bg)" stroke="var(--border)"/>
<text x="530" y="274" fill="var(--primary)" font-family="monospace" font-size="10" text-anchor="middle">f.c2</text>
<rect x="330" y="320" width="140" height="45" rx="10" fill="var(--surface)" stroke="var(--primary)" stroke-width="2" filter="drop-shadow(0 0 8px var(--primary-glow))"/>
<text x="400" y="348" fill="var(--text-main)" font-family="sans-serif" font-size="14" text-anchor="middle" font-weight="700">analyze</text>
<text x="400" y="385" fill="var(--text-muted)" font-family="sans-serif" font-size="12" text-anchor="middle">Final Output (f.d)</text>
<defs>
<marker id="arrow-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 0 L 10 5 L 0 10 z" fill="var(--text-muted)" />
</marker>
</defs>
</svg>
</div>

The **Diamond Workflow** perfectly demonstrates this concept. It gets its name from its shape:

- **The Top (`preprocess`):** A single job takes a starting file and splits the data into two independent pieces.
- **The Middle (`findrange`):** Two independent jobs run simultaneously on different compute nodes. Each processes one half of the data.
- **The Bottom (`analyze`):** A final job waits for the two middle jobs to finish, then merges their results into a final output.

## 2. Create Your Executable Programs

Before Pegasus can manage your workflow, it needs the actual software programs that will do the math or process the data. Let's write three simple Python scripts to act as our "software."

Open your terminal and create a folder for your project:

```bash
mkdir pegasus-beginner
cd pegasus-beginner
mkdir bin
```

Below are the three scripts. Save them inside the `bin/` folder and ensure you make them executable using `chmod +x bin/*`.

<div class="tab-system">
<div class="tab-nav">
<button class="tab-btn active" onclick="switchTab(event, 'script-1')">bin/preprocess</button>
<button class="tab-btn" onclick="switchTab(event, 'script-2')">bin/findrange</button>
<button class="tab-btn" onclick="switchTab(event, 'script-3')">bin/analyze</button>
</div>
<div id="script-1" class="tab-content">
<div class="code-container">
<pre><code class="language-python">#!/usr/bin/env python3
import sys
# sys.argv reads the arguments passed by Pegasus
input_file = sys.argv[1]
output_1   = sys.argv[2]
output_2   = sys.argv[3]
# Read the starting data
with open(input_file, 'r') as f:
    data = f.read()
# Write data to two parallel branches
with open(output_1, 'w') as f1:
    f1.write(f"{data} -> Processed for Branch 1")
with open(output_2, 'w') as f2:
    f2.write(f"{data} -> Processed for Branch 2")</code></pre>
</div>
</div>
<div id="script-2" class="tab-content" style="display:none;">
<div class="code-container">
<pre><code class="language-python">#!/usr/bin/env python3
import sys
input_file  = sys.argv[1]
output_file = sys.argv[2]
with open(input_file, 'r') as f:
    data = f.read()
with open(output_file, 'w') as f:
    f.write(f"{data} -> Analyzed by Findrange")</code></pre>
</div>
<div style="padding: 20px; background: var(--surface); border-top: 1px solid var(--border);">
<p style="margin: 0; font-size: 0.95rem;"><b>Note:</b> This exact same script will be executed <b>twice simultaneously</b> by Pegasus.</p>
</div>
</div>
<div id="script-3" class="tab-content" style="display:none;">
<div class="code-container">
<pre><code class="language-python">#!/usr/bin/env python3
import sys
# Read the data from both middle jobs
with open(sys.argv[1], 'r') as f1: data1 = f1.read()
with open(sys.argv[2], 'r') as f2: data2 = f2.read()
# Merge it into the final output file
with open(sys.argv[3], 'w') as out:
    out.write("--- FINAL MERGED RESULT ---\n")
    out.write(f"Result A: {data1}\n")
    out.write(f"Result B: {data2}\n")</code></pre>
</div>
</div>
</div>

## 3. Write the Workflow Blueprint

Now we need to tell Pegasus how these scripts connect to each other. We do this by writing a "Blueprint" using the Pegasus Python API. Create a file named `workflow_generator.py` in your main folder.

<div class="tab-system">
<div class="tab-nav">
<button class="tab-btn active" style="cursor:default;">workflow_generator.py</button>
</div>
<div class="tab-content">
<div class="code-container">
<pre><code class="language-python">#!/usr/bin/env python3
import logging
from pathlib import Path
from Pegasus.api import *
logging.basicConfig(level=logging.DEBUG)
# 1. Initialize the Workflow
wf = Workflow("diamond-beginner")
# 2. Create the Starting File (f.a)
with open("f.a", "w") as f:
    f.write("Starting Point")
in_file = File("f.a")
rc = ReplicaCatalog().add_replica("local", in_file, Path(".").resolve() / "f.a")
wf.add_replica_catalog(rc)
# 3. Define the Executables
preprocess = Transformation("preprocess", site="local", pfn=Path(".").resolve() / "bin/preprocess", is_stageable=True)
findrange  = Transformation("findrange",  site="local", pfn=Path(".").resolve() / "bin/findrange",  is_stageable=True)
analyze    = Transformation("analyze",    site="local", pfn=Path(".").resolve() / "bin/analyze",    is_stageable=True)
tc = TransformationCatalog().add_transformations(preprocess, findrange, analyze)
wf.add_transformation_catalog(tc)
# 4. Connect the Jobs (Build the Diamond shape)
f_b1 = File("f.b1")
f_b2 = File("f.b2")
job_preprocess  = Job(preprocess).add_args(in_file, f_b1, f_b2).add_inputs(in_file).add_outputs(f_b1, f_b2)
f_c1 = File("f.c1")
f_c2 = File("f.c2")
# findrange is reused twice — once per branch
job_findrange_1 = Job(findrange).add_args(f_b1, f_c1).add_inputs(f_b1).add_outputs(f_c1)
job_findrange_2 = Job(findrange).add_args(f_b2, f_c2).add_inputs(f_b2).add_outputs(f_c2)
f_d = File("f.d")
job_analyze = Job(analyze).add_args(f_c1, f_c2, f_d).add_inputs(f_c1, f_c2).add_outputs(f_d)
wf.add_jobs(job_preprocess, job_findrange_1, job_findrange_2, job_analyze)
# 5. Plan and Submit
try:
    wf.plan(submit=True)
except PegasusClientError as e:
    print(e)</code></pre>
</div>
</div>
</div>

## 4. Execution & Monitoring

You are ready! Execute your blueprint script to submit the DAG to HTCondor:

```bash
chmod +x workflow_generator.py
./workflow_generator.py
```

Pegasus will plan the execution, handle the data transfers, and run the jobs. It will output a "submit directory path" in your terminal. You can check the progress of your parallel jobs by running:

```bash
pegasus-status [paste_your_submit_directory_path_here]
```

<div class="highlight-box" style="border-color: var(--success); background: rgba(16, 185, 129, 0.1);">
<h3 style="color: var(--success);"><i class="fas fa-check-circle"></i> Success</h3>
<p style="margin:0;">When the status says "DONE", look inside your folder for a new file named <code>f.d</code>. Open it up, and you will see your merged data! You have officially run your first parallel workflow.</p>
</div>
