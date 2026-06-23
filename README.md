# PegasusHub

The centralized ecosystem for discovering, learning, and deploying high-throughput scientific workflows using [Pegasus WMS](https://pegasus.isi.edu).

**Live site:** [pegasushub.github.io](https://pegasushub.github.io)

## Pages

| Page | Description |
|------|-------------|
| `/` | Homepage — overview and mission |
| `/pages/academy.html` | Learning portal with video tutorials and Jupyter notebooks |
| `/pages/workflows.html` | Workflow registry browser |
| `/pages/build.html` | Build & Run guide + workflow submission |
| `/pages/ai-tools.html` | AI tools for Pegasus |
| `/modules/module.html?module=X` | Interactive module viewer (diamond, pegasus, split, hwf) |

## Structure

```
pegasushub/
├── index.html                  # Homepage
├── pages/                      # Site pages
├── modules/                    # Module viewer (renders .md files)
├── assets/
│   ├── css/main.css            # Shared styles
│   ├── js/main.js              # Shared scripts
│   └── data/
│       ├── courses.json        # Academy tutorials config
│       └── modules/            # Module markdown content + config
└── CNAME                       # Custom domain (pegasushub.io)
```

## Data Sources

| Data | Source |
|------|--------|
| Workflow registry | [pegasushub/workflow-registry](https://github.com/pegasushub/workflow-registry) |
| Academy tutorials | `assets/data/courses.json` |
| Module content | `assets/data/modules/*.md` |

## Deployment

Push to `master` branch of [pegasushub/pegasushub.github.io](https://github.com/pegasushub/pegasushub.github.io) — GitHub Pages serves it automatically.

## Related Repositories

- [pegasushub/workflow-registry](https://github.com/pegasushub/workflow-registry) — workflow submission registry
- [pegasus-isi](https://github.com/pegasus-isi) — official Pegasus WMS organization
