## 1. Why Hierarchical Workflows?

In traditional scientific computing, a single Directed Acyclic Graph (DAG) defines all tasks from start to finish. However, as workflows grow to encompass hundreds of thousands of jobs, a flat DAG becomes a massive bottleneck. The planning process takes too long, the submission files become too large, and failure recovery is incredibly difficult.

**Hierarchical Workflows** (the "Workflow of Workflows" paradigm) solve this by allowing you to nest DAGs inside of DAGs.

<div class="highlight-box">
<h3><i class="fas fa-bolt"></i> Key Benefits:</h3>
<ul>
<li><b>Scalability:</b> Bypasses the job limit of a single Condor submission node by distributing the graph generation across multiple compute nodes.</li>
<li><b>Dynamic Graph Generation (JIT Planning):</b> By using <code>is_planned=False</code>, the parent workflow waits until the exact moment a child job is scheduled to generate and plan its specific DAG. This allows the child workflow to adapt to newly created data or changing cluster conditions!</li>
<li><b>Fault Isolation:</b> If a sub-workflow fails (e.g., Round 5 of a machine learning loop), you can rescue and restart <em>only</em> that specific sub-DAG, rather than re-evaluating the entire global pipeline.</li>
</ul>
</div>

## 2. Workflow Design & Architecture

Designing a hierarchical workflow requires a strict separation of concerns. You must divide your logic into two distinct components: the **Parent (Orchestrator)** and the **Child (SubWorkflow)**.

<div>
<svg class="svg-graphic" viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
<rect x="50" y="40" width="220" height="220" fill="var(--surface)" rx="16" stroke="var(--border)" stroke-width="2"/>
<text x="160" y="70" fill="var(--text-muted)" font-family="sans-serif" font-size="12" text-anchor="middle" font-weight="bold" letter-spacing="1">PARENT DAG</text>
<circle cx="160" cy="110" r="18" fill="var(--code-bg)" stroke="var(--text-muted)" stroke-width="2"/>
<circle cx="160" cy="170" r="22" fill="var(--code-bg)" stroke="var(--primary)" stroke-width="3" filter="drop-shadow(0 0 10px var(--primary-glow))"/>
<circle cx="160" cy="230" r="18" fill="var(--code-bg)" stroke="var(--text-muted)" stroke-width="2"/>
<line x1="160" y1="128" x2="160" y2="148" stroke="var(--text-muted)" stroke-width="2" marker-end="url(#arrow-muted)"/>
<line x1="160" y1="192" x2="160" y2="212" stroke="var(--text-muted)" stroke-width="2" marker-end="url(#arrow-muted)"/>
<path d="M 182 170 C 260 170, 300 150, 380 150" fill="none" stroke="var(--primary)" stroke-width="3" stroke-dasharray="6,4" marker-end="url(#arrow-primary)"/>
<text x="280" y="140" fill="var(--primary)" font-family="sans-serif" font-size="11" font-weight="bold">Triggers SubWorkflow</text>
<rect x="380" y="40" width="370" height="220" fill="var(--surface)" rx="16" stroke="var(--primary)" stroke-width="2"/>
<text x="565" y="70" fill="var(--primary)" font-family="sans-serif" font-size="12" text-anchor="middle" font-weight="bold" letter-spacing="1">CHILD DAG (Execution Unit)</text>
<rect x="420" y="100" width="100" height="40" rx="8" fill="var(--code-bg)" stroke="var(--text-muted)" stroke-width="2"/>
<text x="470" y="125" fill="var(--text-main)" font-family="sans-serif" font-size="12" text-anchor="middle" font-weight="600">Initiation</text>
<rect x="570" y="100" width="150" height="40" rx="8" fill="var(--code-bg)" stroke="var(--text-muted)" stroke-width="2"/>
<text x="645" y="125" fill="var(--text-main)" font-family="sans-serif" font-size="12" text-anchor="middle" font-weight="600">Parallel Training (N)</text>
<rect x="495" y="180" width="140" height="40" rx="8" fill="var(--code-bg)" stroke="var(--text-muted)" stroke-width="2"/>
<text x="565" y="205" fill="var(--text-main)" font-family="sans-serif" font-size="12" text-anchor="middle" font-weight="600">Weight Aggregation</text>
<line x1="520" y1="120" x2="570" y2="120" stroke="var(--text-muted)" stroke-width="2" marker-end="url(#arrow-muted)"/>
<line x1="645" y1="140" x2="565" y2="180" stroke="var(--text-muted)" stroke-width="2" marker-end="url(#arrow-muted)"/>
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

- **The Parent DAG:** Acts purely as a high-level manager. It does not perform scientific computation. Instead, its "jobs" are `SubWorkflow` API calls. The parent is responsible for passing arguments (like round numbers or data partitions) down to the child generators.
- **The Child DAG:** Represents a focused, localized module of work. When triggered by the parent, it runs its own Python generator script, creates an abstract YAML file, plans itself against the available execution sites, and executes the actual tasks (like data processing or model training).
- **Data Flow:** Data is passed between the Parent and Child using the **Replica Catalog** and a **Shared Scratch Directory**. When a child DAG finishes, its output files remain in the shared scratch, allowing the parent DAG to easily pass them as input to the next child DAG in the sequence.

## 3. What is Federated Learning?

**Federated Learning (FL)** is a highly iterative, privacy-preserving machine learning approach. Instead of sending all raw user data to a centralized server to train an AI model, the server sends the *model* to the users.

<div>
<svg class="svg-graphic" viewBox="0 0 800 350" xmlns="http://www.w3.org/2000/svg">
<circle cx="400" cy="100" r="55" fill="var(--surface)" stroke="var(--primary)" stroke-width="3" filter="drop-shadow(0 0 15px var(--primary-glow))"/>
<text x="400" y="95" fill="var(--text-main)" font-family="sans-serif" font-size="14" text-anchor="middle" font-weight="bold">Global</text>
<text x="400" y="115" fill="var(--text-main)" font-family="sans-serif" font-size="14" text-anchor="middle" font-weight="bold">Server</text>
<g transform="translate(150, 250)">
<rect x="-50" y="-30" width="100" height="60" rx="10" fill="var(--surface)" stroke="var(--border)" stroke-width="2"/>
<text x="0" y="-5" fill="var(--text-main)" font-family="sans-serif" font-size="14" text-anchor="middle" font-weight="600">Client 1</text>
<text x="0" y="15" fill="var(--text-muted)" font-family="sans-serif" font-size="11" text-anchor="middle">Local Data</text>
</g>
<g transform="translate(400, 250)">
<rect x="-50" y="-30" width="100" height="60" rx="10" fill="var(--surface)" stroke="var(--border)" stroke-width="2"/>
<text x="0" y="-5" fill="var(--text-main)" font-family="sans-serif" font-size="14" text-anchor="middle" font-weight="600">Client 2</text>
<text x="0" y="15" fill="var(--text-muted)" font-family="sans-serif" font-size="11" text-anchor="middle">Local Data</text>
</g>
<g transform="translate(650, 250)">
<rect x="-50" y="-30" width="100" height="60" rx="10" fill="var(--surface)" stroke="var(--border)" stroke-width="2"/>
<text x="0" y="-5" fill="var(--text-main)" font-family="sans-serif" font-size="14" text-anchor="middle" font-weight="600">Client 3</text>
<text x="0" y="15" fill="var(--text-muted)" font-family="sans-serif" font-size="11" text-anchor="middle">Local Data</text>
</g>
<path d="M 360 135 L 180 220" fill="none" stroke="var(--primary)" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#arrow-primary)"/>
<path d="M 400 155 L 400 220" fill="none" stroke="var(--primary)" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#arrow-primary)"/>
<path d="M 440 135 L 620 220" fill="none" stroke="var(--primary)" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#arrow-primary)"/>
<text x="240" y="165" fill="var(--primary)" font-family="sans-serif" font-size="13" font-weight="bold">Broadcast Model</text>
<path d="M 150 220 Q 150 150 340 110" fill="none" stroke="var(--success)" stroke-width="2" marker-end="url(#arrow-success)"/>
<path d="M 430 220 Q 480 180 445 125" fill="none" stroke="var(--success)" stroke-width="2" marker-end="url(#arrow-success)"/>
<path d="M 650 220 Q 650 150 460 110" fill="none" stroke="var(--success)" stroke-width="2" marker-end="url(#arrow-success)"/>
<text x="530" y="165" fill="var(--success)" font-family="sans-serif" font-size="13" font-weight="bold">Upload Weight Updates</text>
<defs>
<marker id="arrow-success" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 0 L 10 5 L 0 10 z" fill="var(--success)" />
</marker>
</defs>
</svg>
</div>

The lifecycle of Federated Learning perfectly matches the Hierarchical Workflow design:

1. **Global Server (Parent Workflow):** Orchestrates the experiment. It initializes the base neural network model and defines how many "rounds" of training will occur.
2. **Edge Clients (Child Workflows):** In every round, a subset of remote clients (hospitals, mobile phones, etc.) download the current model, train it locally on their private data, and compute weight updates.
3. **Aggregation (End of Child Workflow):** The remote clients send only their mathematical weight updates back to the server. An aggregation job averages these weights to update the global model. The Parent workflow then triggers the next round.

## 4. Example of Implementation

Let's look at how to implement this FL pattern in Pegasus. You will create two files: `workflow_generator_main_sub.py` (The Parent) and `workflow_generator_sub.py` (The Child Round).

<div class="tab-system">
<div class="tab-nav">
<button class="tab-btn active" onclick="switchTab(event, 'parent-code')">workflow_generator_main_sub.py (Parent)</button>
<button class="tab-btn" onclick="switchTab(event, 'sub-code')">workflow_generator_sub.py (Child)</button>
</div>
<div id="parent-code" class="tab-content">
<div class="code-container">
<pre><code class="language-python">#!/usr/bin/env python3
from Pegasus.api import *
class FederatedLearningWorkflow:
    def run_workflow(self, clients, selected_clients, num_rounds, score):
        # The parent workflow simply manages the FL rounds
        for round_num in range(num_rounds):
            # 1. Define the SubWorkflow job
            # We point it to the 'workflow.yml' the child script WILL generate
            sub_wf_job = SubWorkflow("workflow.yml", is_planned=False)
            # 2. Pass dynamic arguments from parent to child generator
            sub_wf_job.add_args(
                "-c", str(clients),
                "-n", str(selected_clients),
                "-r", str(round_num),
                "-score", str(score)
            )
            # 3. Add to the parent DAG
            self.wf.add_jobs(sub_wf_job)
        self.wf.write()</code></pre>
</div>
<div style="padding: 20px; background: var(--surface); border-top: 1px solid var(--border);">
<p style="margin: 0; font-size: 0.95rem;"><b>What's happening?</b> The parent creates a <code>SubWorkflow</code> node for every FL round. It passes arguments like <code>-r</code> (round number). Because <code>is_planned=False</code> is used, HTCondor will trigger the Pegasus planner dynamically on the child graph when it's time for that round to execute.</p>
</div>
</div>
<div id="sub-code" class="tab-content" style="display:none;">
<div class="code-container">
<pre><code class="language-python">#!/usr/bin/env python3
from Pegasus.api import *
class FederatedLearningWorkflow:
    def __init__(self, dagfile="workflow.yml"):
        self.dagfile = dagfile
        # CRITICAL: Child maps its scratch relative to the Parent's scratch!
        self.shared_scratch_dir = os.path.join(wf_dir, "Main_workflow/scratch")
        self.local_storage_dir  = os.path.join(wf_dir, "Main_workflow/output")
    def run_workflow(self, args):
        # 1. Initiation Job
        init_job = Job("initiation")
        # 2. Parallel Training Jobs (Run locally on N clients)
        for client in range(args.number_of_selected_clients):
            train_job = Job("training")
            train_job.add_args("-c", str(client), "-r", str(args.number_of_rounds))
            self.wf.add_jobs(train_job)
        # 3. Aggregation Job (Average the model weights)
        agg_job = Job("aggregation")
        # 4. Write the YAML file that the parent is expecting!
        self.wf.write(args.output)</code></pre>
</div>
<div style="padding: 20px; background: var(--surface); border-top: 1px solid var(--border);">
<p style="margin: 0; font-size: 0.95rem;"><b>What's happening?</b> The child script parses the arguments sent by the parent. It maps its scratch directory to <code>Main_workflow/scratch</code> so models can be shared between rounds. It then defines the actual scientific workload (initiation, parallel client training, and weight aggregation), and writes the final <code>workflow.yml</code> file.</p>
</div>
</div>
</div>
