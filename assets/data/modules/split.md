## 1. Why Split Workflows?

In data-intensive sciences like bioinformatics, astrophysics, or log analysis, researchers often deal with monolithic files (e.g., a 500GB log file or an unpartitioned genome sequence). Running a single processing script on a 500GB file on one machine is incredibly slow and prone to memory exhaustion.

**Data Splitting** allows us to overcome hardware limits and time constraints by dividing the large problem into hundreds or thousands of smaller, independent problems that can be solved simultaneously on a grid.

<div class="highlight-box">
<h3><i class="fas fa-tachometer-alt"></i> Key Benefits:</h3>
<ul>
<li><b>Massive Parallelism:</b> A job taking 100 hours on a single CPU can take just 1 hour if split into 100 chunks and run across a high-throughput cluster.</li>
<li><b>Fault Tolerance:</b> If a node crashes while processing chunk 42, Pegasus only retries chunk 42, rather than restarting the entire 500GB process from scratch.</li>
<li><b>Memory Efficiency:</b> Processing smaller chunks prevents Out-Of-Memory (OOM) errors on compute nodes.</li>
</ul>
</div>

## 2. Design & Architecture

The split workflow architecture relies on a "Scatter" pattern. It typically begins with a single job that divides the data, followed by a wide fan-out of parallel processing jobs.

<div>
<svg class="svg-graphic" viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
<rect x="330" y="30" width="140" height="45" rx="10" fill="var(--surface)" stroke="var(--primary)" stroke-width="2" filter="drop-shadow(0 0 8px var(--primary-glow))"/>
<text x="400" y="58" fill="var(--text-main)" font-family="sans-serif" font-size="14" text-anchor="middle" font-weight="700">split_job</text>
<path d="M 400 75 L 150 160" fill="none" stroke="var(--text-muted)" stroke-width="2" marker-end="url(#arrow-muted)"/>
<path d="M 400 75 L 320 160" fill="none" stroke="var(--text-muted)" stroke-width="2" marker-end="url(#arrow-muted)"/>
<path d="M 400 75 L 480 160" fill="none" stroke="var(--text-muted)" stroke-width="2" marker-end="url(#arrow-muted)"/>
<path d="M 400 75 L 650 160" fill="none" stroke="var(--text-muted)" stroke-width="2" marker-end="url(#arrow-muted)"/>
<rect x="220" y="90" width="60" height="20" rx="4" fill="var(--code-bg)" stroke="var(--border)"/>
<text x="250" y="104" fill="var(--primary)" font-family="monospace" font-size="10" text-anchor="middle">part.01</text>
<rect x="520" y="90" width="60" height="20" rx="4" fill="var(--code-bg)" stroke="var(--border)"/>
<text x="550" y="104" fill="var(--primary)" font-family="monospace" font-size="10" text-anchor="middle">part.0N</text>
<rect x="100" y="170" width="100" height="40" rx="8" fill="var(--surface)" stroke="var(--border)" stroke-width="2"/>
<text x="150" y="195" fill="var(--text-main)" font-family="sans-serif" font-size="12" text-anchor="middle">process_1</text>
<rect x="270" y="170" width="100" height="40" rx="8" fill="var(--surface)" stroke="var(--border)" stroke-width="2"/>
<text x="320" y="195" fill="var(--text-main)" font-family="sans-serif" font-size="12" text-anchor="middle">process_2</text>
<rect x="430" y="170" width="100" height="40" rx="8" fill="var(--surface)" stroke="var(--border)" stroke-width="2"/>
<text x="480" y="195" fill="var(--text-main)" font-family="sans-serif" font-size="12" text-anchor="middle">process_3</text>
<circle cx="560" cy="190" r="3" fill="var(--text-muted)"/>
<circle cx="575" cy="190" r="3" fill="var(--text-muted)"/>
<circle cx="590" cy="190" r="3" fill="var(--text-muted)"/>
<rect x="600" y="170" width="100" height="40" rx="8" fill="var(--surface)" stroke="var(--border)" stroke-width="2"/>
<text x="650" y="195" fill="var(--text-main)" font-family="sans-serif" font-size="12" text-anchor="middle">process_N</text>
<defs>
<marker id="arrow-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 0 L 10 5 L 0 10 z" fill="var(--text-muted)" />
</marker>
</defs>
</svg>
</div>

## 3. What is the Scatter Pattern?

The Scatter pattern is the act of taking a single input and dispatching it to an array of independent workers. In Pegasus, we accomplish this by writing a Python generator loop.

<div>
<svg class="svg-graphic" viewBox="0 0 800 240" xmlns="http://www.w3.org/2000/svg">
<rect x="80" y="50" width="90" height="120" fill="var(--surface)" stroke="var(--text-muted)" stroke-width="2" rx="4"/>
<line x1="100" y1="80" x2="150" y2="80" stroke="var(--text-muted)" stroke-width="2"/>
<line x1="100" y1="100" x2="150" y2="100" stroke="var(--text-muted)" stroke-width="2"/>
<line x1="100" y1="120" x2="150" y2="120" stroke="var(--text-muted)" stroke-width="2"/>
<line x1="100" y1="140" x2="150" y2="140" stroke="var(--text-muted)" stroke-width="2"/>
<text x="125" y="195" fill="var(--text-main)" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold">Monolithic Data</text>
<circle cx="300" cy="110" r="35" fill="var(--primary-glow)" stroke="var(--primary)" stroke-width="2"/>
<text x="300" y="115" fill="var(--primary)" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle">SPLIT</text>
<path d="M 190 110 L 250 110" fill="none" stroke="var(--primary)" stroke-width="3" marker-end="url(#arrow-primary)"/>
<path d="M 345 110 L 450 40" fill="none" stroke="var(--success)" stroke-width="2" marker-end="url(#arrow-success)"/>
<path d="M 345 110 L 450 85" fill="none" stroke="var(--success)" stroke-width="2" marker-end="url(#arrow-success)"/>
<path d="M 345 110 L 450 135" fill="none" stroke="var(--success)" stroke-width="2" marker-end="url(#arrow-success)"/>
<path d="M 345 110 L 450 180" fill="none" stroke="var(--success)" stroke-width="2" marker-end="url(#arrow-success)"/>
<rect x="470" y="20" width="40" height="40" fill="var(--surface)" stroke="var(--success)" stroke-width="2" rx="4"/>
<rect x="470" y="65" width="40" height="40" fill="var(--surface)" stroke="var(--success)" stroke-width="2" rx="4"/>
<rect x="470" y="110" width="40" height="40" fill="var(--surface)" stroke="var(--success)" stroke-width="2" rx="4"/>
<rect x="470" y="155" width="40" height="40" fill="var(--surface)" stroke="var(--success)" stroke-width="2" rx="4"/>
<text x="540" y="125" fill="var(--text-main)" font-family="sans-serif" font-size="14" font-weight="600">Simultaneous Execution</text>
<defs>
<marker id="arrow-primary" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 0 L 10 5 L 0 10 z" fill="var(--primary)" />
</marker>
<marker id="arrow-success" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 0 L 10 5 L 0 10 z" fill="var(--success)" />
</marker>
</defs>
</svg>
</div>

Instead of manually defining 100 different jobs, we use a loop to dynamically add jobs to our Pegasus Workflow object based on the number of split outputs. Pegasus automatically deduces the dependencies because the `process` jobs require the output files generated by the `split` job.

## 4. Implementation Example

Here is the Python API code required to generate a Split Workflow. Notice how we dynamically generate the output files for the `split_job` and then immediately use them as inputs for the `process_job` loop.

<div class="tab-system">
<div class="tab-nav">
<button class="tab-btn active" onclick="switchTab(event, 'code-gen')">workflow_generator.py</button>
</div>
<div id="code-gen" class="tab-content">
<div class="code-container">
<pre><code class="language-python">from Pegasus.api import *
def generate_workflow(num_splits):
    wf = Workflow("split-pattern")
    # 1. Define the input file
    input_file = File("massive_dataset.txt")
    # 2. Define the Split Job
    split_job = Job("split_tool")
    split_job.add_inputs(input_file)
    # 3. Dynamically define the output chunks and link them
    split_outputs = []
    for i in range(num_splits):
        chunk = File(f"part_{i}.txt")
        split_outputs.append(chunk)
        split_job.add_outputs(chunk)
    wf.add_jobs(split_job)
    # 4. Create a Parallel Process Job for every chunk
    for chunk_file in split_outputs:
        process_job = Job("compute_tool")
        process_job.add_inputs(chunk_file)
        result_file = File(f"result_{chunk_file.lfn}")
        process_job.add_outputs(result_file)
        wf.add_jobs(process_job)
    # Pegasus auto-draws DAG edges because process jobs
    # require files outputted by the split job!
    wf.write()
if __name__ == "__main__":
    generate_workflow(num_splits=10)</code></pre>
</div>
<div style="padding: 20px; background: var(--surface); border-top: 1px solid var(--border);">
<p style="margin: 0; font-size: 0.95rem;"><b>Dependency Magic:</b> In Pegasus, you rarely need to use <code>wf.add_dependency()</code> manually. Because <code>split_job</code> declares <code>part_0.txt</code> as an output, and <code>process_job</code> declares it as an input, Pegasus automatically infers that <code>split_job</code> must run first!</p>
</div>
</div>
</div>
