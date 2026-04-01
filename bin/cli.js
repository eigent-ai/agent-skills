#!/usr/bin/env node

/**
 * Eigent Agent Skills CLI
 *
 * Install, update, and manage Eigent agent skills for
 * Claude Code, Cursor, Windsurf, Codex, and other AI coding agents.
 *
 * Usage:
 *   npx @eigent-ai/agent-skills install [skill1 [skill2 ...]] [--agent <name>] [--global]
 *   npx @eigent-ai/agent-skills update  [--agent <name>] [--global]
 *   npx @eigent-ai/agent-skills list
 *   npx @eigent-ai/agent-skills uninstall [skill1 [skill2 ...]] [--agent <name>] [--global]
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");
const crypto = require("crypto");

// ── Constants ────────────────────────────────────────────────────────────────

const REPO_URL = "https://github.com/eigent-ai/agent-skills.git";
const LOCK_FILE = ".eigent-skills.lock.json";
const SKILLS_DIR_NAME = "skills";

// ── Agent definitions ────────────────────────────────────────────────────────

const AGENTS = {
  "claude-code": {
    name: "Claude Code",
    projectDir: (root) => path.join(root, ".claude", "skills"),
    globalDir: () => path.join(homedir(), ".claude", "skills"),
    detect: () =>
      which("claude") || dirExists(path.join(homedir(), ".claude")),
  },
  cursor: {
    name: "Cursor",
    projectDir: (root) => path.join(root, ".cursor", "skills"),
    globalDir: () => path.join(homedir(), ".cursor", "skills"),
    detect: () =>
      which("cursor") || dirExists(path.join(homedir(), ".cursor")),
  },
  windsurf: {
    name: "Windsurf",
    projectDir: (root) => path.join(root, ".windsurf", "skills"),
    globalDir: () => path.join(homedir(), ".windsurf", "skills"),
    detect: () =>
      which("windsurf") || dirExists(path.join(homedir(), ".windsurf")),
  },
  codex: {
    name: "Codex",
    projectDir: (root) => path.join(root, ".codex", "skills"),
    globalDir: () => path.join(homedir(), ".codex", "skills"),
    detect: () =>
      which("codex") || dirExists(path.join(homedir(), ".codex")),
  },
  copilot: {
    name: "GitHub Copilot",
    projectDir: (root) => path.join(root, ".github", "skills"),
    globalDir: () => path.join(homedir(), ".github", "skills"),
    detect: () => dirExists(path.join(homedir(), ".github")),
  },
};

// ── Utility helpers ──────────────────────────────────────────────────────────

function homedir() {
  return require("os").homedir();
}

function which(cmd) {
  try {
    execSync(`which ${cmd}`, { stdio: "ignore" });
    return true;
  } catch {
    return false;
  }
}

function dirExists(p) {
  try {
    return fs.statSync(p).isDirectory();
  } catch {
    return false;
  }
}

function fileExists(p) {
  try {
    return fs.statSync(p).isFile();
  } catch {
    return false;
  }
}

function mkdirp(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function copyDir(src, dest) {
  mkdirp(dest);
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.name === ".DS_Store") continue;
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function hashDir(dir) {
  const hash = crypto.createHash("sha256");
  function walk(d) {
    if (!dirExists(d)) return;
    for (const entry of fs.readdirSync(d, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
      if (entry.name === ".DS_Store") continue;
      const full = path.join(d, entry.name);
      if (entry.isDirectory()) {
        walk(full);
      } else {
        hash.update(entry.name);
        hash.update(fs.readFileSync(full));
      }
    }
  }
  walk(dir);
  return hash.digest("hex").slice(0, 12);
}

function removeDir(dir) {
  if (dirExists(dir)) {
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

// ── Skill discovery ──────────────────────────────────────────────────────────

function getSkillsRoot() {
  // When running from repo checkout (development or npx from git)
  const repoSkills = path.join(__dirname, "..", SKILLS_DIR_NAME);
  if (dirExists(repoSkills)) return repoSkills;
  return null;
}

function discoverSkills(skillsRoot) {
  const skills = [];
  if (!skillsRoot || !dirExists(skillsRoot)) return skills;
  for (const category of fs.readdirSync(skillsRoot, { withFileTypes: true })) {
    if (!category.isDirectory()) continue;
    const catPath = path.join(skillsRoot, category.name);
    for (const skill of fs.readdirSync(catPath, { withFileTypes: true })) {
      if (!skill.isDirectory()) continue;
      const skillMd = path.join(catPath, skill.name, "SKILL.md");
      if (fileExists(skillMd)) {
        skills.push({
          name: skill.name,
          category: category.name,
          path: path.join(catPath, skill.name),
          skillMd,
        });
      }
    }
  }
  return skills;
}

/** Resolve skill names (e.g. "mintlify-docs-updater" or "category/mintlify-docs-updater") to skill objects. */
function resolveSkillNames(skillsRoot, skillNames) {
  if (!skillNames || skillNames.length === 0) return null;
  const all = discoverSkills(skillsRoot);
  const resolved = [];
  const notFound = [];
  for (const name of skillNames) {
    const norm = name.trim().toLowerCase();
    const skill = all.find(
      (s) =>
        s.name.toLowerCase() === norm ||
        `${s.category}/${s.name}`.toLowerCase() === norm
    );
    if (skill) {
      resolved.push(skill);
    } else {
      notFound.push(name);
    }
  }
  if (notFound.length > 0) {
    console.error(`Unknown skill(s): ${notFound.join(", ")}`);
    console.error(`Run 'npx @eigent-ai/agent-skills list' to see available skills.`);
    process.exit(1);
  }
  return resolved;
}

function parseSkillMeta(skillMdPath) {
  const content = fs.readFileSync(skillMdPath, "utf-8");
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return {};
  const meta = {};
  for (const line of match[1].split("\n")) {
    const m = line.match(/^(\w+):\s*(.+)/);
    if (m) meta[m[1]] = m[2].trim();
  }
  return meta;
}

// ── Remote fetch (for auto-update) ──────────────────────────────────────────

function fetchLatestFromGit() {
  const tmpDir = path.join(require("os").tmpdir(), `eigent-skills-${Date.now()}`);
  try {
    console.log("  Fetching latest skills from GitHub...");
    execSync(`git clone --depth 1 ${REPO_URL} "${tmpDir}"`, { stdio: "ignore" });
    return path.join(tmpDir, SKILLS_DIR_NAME);
  } catch (err) {
    console.error("  Failed to fetch from GitHub:", err.message);
    return null;
  }
}

function cleanupTmp(tmpSkillsRoot) {
  // tmpSkillsRoot is like /tmp/eigent-skills-xxx/skills, go up one level
  const tmpDir = path.join(tmpSkillsRoot, "..");
  removeDir(tmpDir);
}

// ── Lock file management ────────────────────────────────────────────────────

function readLock(lockPath) {
  if (fileExists(lockPath)) {
    try {
      return JSON.parse(fs.readFileSync(lockPath, "utf-8"));
    } catch {
      return {};
    }
  }
  return {};
}

function writeLock(lockPath, data) {
  fs.writeFileSync(lockPath, JSON.stringify(data, null, 2) + "\n");
}

// ── Core commands ────────────────────────────────────────────────────────────

function detectAgents() {
  const detected = [];
  for (const [id, agent] of Object.entries(AGENTS)) {
    if (agent.detect()) detected.push(id);
  }
  return detected;
}

function resolveTargetAgents(agentFlag) {
  if (agentFlag && agentFlag !== "all") {
    const id = agentFlag.toLowerCase();
    if (!AGENTS[id]) {
      console.error(`Unknown agent: ${agentFlag}`);
      console.error(`Available agents: ${Object.keys(AGENTS).join(", ")}`);
      process.exit(1);
    }
    return [id];
  }
  const detected = detectAgents();
  if (detected.length === 0) {
    console.log("No supported agents detected. Installing for Claude Code by default.");
    return ["claude-code"];
  }
  return detected;
}

function installSkills(skillsRoot, agents, isGlobal, projectRoot, skillFilter) {
  const allSkills = discoverSkills(skillsRoot);
  const skills = skillFilter
    ? resolveSkillNames(skillsRoot, skillFilter)
    : allSkills;

  if (skills.length === 0) {
    console.error("No skills found to install.");
    process.exit(1);
  }

  let totalInstalled = 0;

  for (const agentId of agents) {
    const agent = AGENTS[agentId];
    const targetBase = isGlobal ? agent.globalDir() : agent.projectDir(projectRoot);
    const lockPath = path.join(targetBase, LOCK_FILE);
    const existingLock = readLock(lockPath);

    console.log(`\n  Installing to ${agent.name}${isGlobal ? " (global)" : ""}...`);
    console.log(`  Target: ${targetBase}`);

    for (const skill of skills) {
      const dest = path.join(targetBase, skill.category, skill.name);
      copyDir(skill.path, dest);
      console.log(`    + ${skill.category}/${skill.name}`);
      totalInstalled++;
    }

    // Merge with existing lock when installing specific skills; otherwise replace
    const existingSkills = (existingLock.skills || []).filter(
      (s) => !skills.some((n) => n.category === s.category && n.name === s.name)
    );
    const mergedSkills = [...existingSkills, ...skills.map((s) => ({ name: s.name, category: s.category }))];

    const lockData = {
      version: getPackageVersion(),
      installedAt: new Date().toISOString(),
      hash: skillFilter ? existingLock.hash || hashDir(skillsRoot) : hashDir(skillsRoot),
      source: REPO_URL,
      skills: mergedSkills,
    };
    writeLock(lockPath, lockData);
  }

  return totalInstalled;
}

function updateSkills(agents, isGlobal, projectRoot) {
  const remoteSkillsRoot = fetchLatestFromGit();
  if (!remoteSkillsRoot) {
    console.error("Update failed: could not fetch latest skills.");
    process.exit(1);
  }

  const remoteHash = hashDir(remoteSkillsRoot);
  let updatedCount = 0;

  for (const agentId of agents) {
    const agent = AGENTS[agentId];
    const targetBase = isGlobal ? agent.globalDir() : agent.projectDir(projectRoot);
    const lockPath = path.join(targetBase, LOCK_FILE);
    const lock = readLock(lockPath);

    if (lock.hash === remoteHash) {
      console.log(`  ${agent.name}: Already up to date.`);
      continue;
    }

    console.log(`  ${agent.name}: Updating skills...`);

    // Remove old skills that were tracked
    if (lock.skills) {
      for (const s of lock.skills) {
        const oldDir = path.join(targetBase, s.category, s.name);
        removeDir(oldDir);
      }
    }

    // Install fresh
    const skills = discoverSkills(remoteSkillsRoot);
    for (const skill of skills) {
      const dest = path.join(targetBase, skill.category, skill.name);
      copyDir(skill.path, dest);
      console.log(`    ~ ${skill.category}/${skill.name}`);
      updatedCount++;
    }

    const lockData = {
      version: getPackageVersion(),
      installedAt: new Date().toISOString(),
      hash: remoteHash,
      source: REPO_URL,
      skills: skills.map((s) => ({
        name: s.name,
        category: s.category,
      })),
    };
    writeLock(lockPath, lockData);
  }

  cleanupTmp(remoteSkillsRoot);
  return updatedCount;
}

function uninstallSkills(agents, isGlobal, projectRoot, skillFilter) {
  let removed = 0;

  for (const agentId of agents) {
    const agent = AGENTS[agentId];
    const targetBase = isGlobal ? agent.globalDir() : agent.projectDir(projectRoot);
    const lockPath = path.join(targetBase, LOCK_FILE);
    const lock = readLock(lockPath);

    if (!lock.skills || lock.skills.length === 0) {
      console.log(`  ${agent.name}: No Eigent skills found.`);
      continue;
    }

    const toRemove = skillFilter
      ? lock.skills.filter((s) => {
          const norm = (n) => n.trim().toLowerCase();
          return skillFilter.some(
            (f) =>
              norm(f) === s.name.toLowerCase() ||
              norm(f) === `${s.category}/${s.name}`.toLowerCase()
          );
        })
      : lock.skills;

    if (toRemove.length === 0) {
      if (skillFilter) {
        console.log(`  ${agent.name}: No matching skills to remove.`);
      }
      continue;
    }

    console.log(`  ${agent.name}: Removing skills...`);
    for (const s of toRemove) {
      const dir = path.join(targetBase, s.category, s.name);
      removeDir(dir);
      console.log(`    - ${s.category}/${s.name}`);
      removed++;
    }

    // Clean up empty category dirs
    for (const s of toRemove) {
      const catDir = path.join(targetBase, s.category);
      if (dirExists(catDir)) {
        const entries = fs.readdirSync(catDir);
        if (entries.length === 0) fs.rmdirSync(catDir);
      }
    }

    const remaining = lock.skills.filter(
      (s) => !toRemove.some((r) => r.category === s.category && r.name === s.name)
    );
    if (remaining.length > 0) {
      writeLock(lockPath, { ...lock, skills: remaining });
    } else {
      if (fileExists(lockPath)) fs.unlinkSync(lockPath);
    }
  }

  return removed;
}

function listSkills(skillsRoot) {
  const skills = discoverSkills(skillsRoot);
  if (skills.length === 0) {
    console.log("No skills found.");
    return;
  }

  const byCategory = {};
  for (const skill of skills) {
    if (!byCategory[skill.category]) byCategory[skill.category] = [];
    const meta = parseSkillMeta(skill.skillMd);
    byCategory[skill.category].push({
      name: skill.name,
      description: meta.description || "(no description)",
    });
  }

  for (const [cat, catSkills] of Object.entries(byCategory).sort()) {
    console.log(`\n  ${cat}/`);
    for (const s of catSkills) {
      const desc =
        s.description.length > 80
          ? s.description.slice(0, 77) + "..."
          : s.description;
      console.log(`    ${s.name}`);
      console.log(`      ${desc}`);
    }
  }
}

function showStatus(agents, isGlobal, projectRoot) {
  for (const agentId of agents) {
    const agent = AGENTS[agentId];
    const targetBase = isGlobal ? agent.globalDir() : agent.projectDir(projectRoot);
    const lockPath = path.join(targetBase, LOCK_FILE);
    const lock = readLock(lockPath);

    if (!lock.installedAt) {
      console.log(`  ${agent.name}: Not installed`);
      continue;
    }

    console.log(`  ${agent.name}:`);
    console.log(`    Version:   ${lock.version || "unknown"}`);
    console.log(`    Installed: ${lock.installedAt}`);
    console.log(`    Skills:    ${lock.skills ? lock.skills.length : 0}`);
    console.log(`    Path:      ${targetBase}`);
  }
}

function getPackageVersion() {
  try {
    const pkg = JSON.parse(
      fs.readFileSync(path.join(__dirname, "..", "package.json"), "utf-8")
    );
    return pkg.version || "0.0.0";
  } catch {
    return "0.0.0";
  }
}

// ── Cron / auto-update setup ─────────────────────────────────────────────────

function setupAutoUpdate(interval) {
  const schedule = interval || "weekly";
  const cronExpr =
    schedule === "daily"
      ? "0 9 * * *"
      : schedule === "monthly"
        ? "0 9 1 * *"
        : "0 9 * * 1"; // weekly default (Monday 9am)

  const cronCmd = `npx @eigent-ai/agent-skills update --global -y`;
  const cronLine = `${cronExpr} ${cronCmd} >> /tmp/eigent-skills-update.log 2>&1`;

  console.log(`\n  Auto-update schedule: ${schedule}`);
  console.log(`  Cron expression: ${cronExpr}`);
  console.log(`\n  Add this line to your crontab (crontab -e):\n`);
  console.log(`    ${cronLine}`);
  console.log(`\n  Or run updates manually anytime with:`);
  console.log(`    npx @eigent-ai/agent-skills update`);
}

// ── CLI parsing ──────────────────────────────────────────────────────────────

function parseArgs(argv) {
  const args = { command: null, agent: null, global: false, yes: false, interval: null, skills: [], json: false };
  const positional = [];

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === "--agent" || arg === "-a") {
      args.agent = argv[++i];
    } else if (arg === "--global" || arg === "-g") {
      args.global = true;
    } else if (arg === "--yes" || arg === "-y") {
      args.yes = true;
    } else if (arg === "--interval") {
      args.interval = argv[++i];
    } else if (arg === "--json") {
      args.json = true;
    } else if (arg === "--all") {
      // handled per-command
      args.all = true;
    } else if (arg === "--help" || arg === "-h") {
      args.command = "help";
    } else if (arg === "--version" || arg === "-v") {
      args.command = "version";
    } else if (!arg.startsWith("-")) {
      positional.push(arg);
    }
  }

  if (!args.command && positional.length > 0) {
    args.command = positional[0];
    args.skills = positional.slice(1);
  }

  return args;
}

function printHelp() {
  const version = getPackageVersion();
  console.log(`
  eigent-skills v${version} — Install Eigent agent skills for AI coding agents

  USAGE
    npx @eigent-ai/agent-skills <command> [options]

  COMMANDS
    install       Install all skills (or specific skills) to detected agents
    update        Fetch latest skills from GitHub and update
    uninstall     Remove installed Eigent skills (all or specific)
    list          List available skills in this package
    status        Show installation status per agent
    eval          Run structural checks and show quality scores
    auto-update   Show instructions for scheduled auto-updates
    doctor        Check agent detection and installation health

  OPTIONS
    --agent, -a <name>   Target a specific agent (claude-code, cursor, windsurf, codex, copilot)
    --global, -g         Install to user-level (global) directory instead of project
    --yes, -y            Skip confirmation prompts
    --interval <freq>    For auto-update: daily, weekly (default), or monthly
    --help, -h           Show this help
    --version, -v        Show version

  EXAMPLES
    npx @eigent-ai/agent-skills install                     # Install all skills to detected agents
    npx @eigent-ai/agent-skills install mintlify-docs-updater # Install only mintlify-docs-updater
    npx @eigent-ai/agent-skills install mintlify-docs-updater webapp-testing  # Install multiple
    npx @eigent-ai/agent-skills install -g                  # Install globally
    npx @eigent-ai/agent-skills install -a cursor mintlify-docs-updater  # Install one skill for Cursor only
    npx @eigent-ai/agent-skills uninstall mintlify-docs-updater # Remove one skill
    npx @eigent-ai/agent-skills update                      # Update to latest
    npx @eigent-ai/agent-skills eval                         # Structural checks on all skills
    npx @eigent-ai/agent-skills eval docx                    # Check a specific skill
    npx @eigent-ai/agent-skills eval --json                  # Output as JSON
    npx @eigent-ai/agent-skills auto-update --interval daily # Show daily auto-update cron

  SUPPORTED AGENTS
    claude-code    Claude Code (.claude/skills/)
    cursor         Cursor (.cursor/skills/)
    windsurf       Windsurf (.windsurf/skills/)
    codex          Codex (.codex/skills/)
    copilot        GitHub Copilot (.github/skills/)
`);
}

function doctor() {
  console.log("\n  Agent Detection:\n");
  for (const [id, agent] of Object.entries(AGENTS)) {
    const detected = agent.detect();
    const icon = detected ? "+" : "-";
    console.log(`    ${icon} ${agent.name} (${id}): ${detected ? "detected" : "not found"}`);
  }
}

// ── Eval command ────────────────────────────────────────────────────────────

function runEval(skillsRoot, args) {
  const { scoreSkill, loadScores } = require(path.join(__dirname, "..", "evals", "scorer"));

  const allSkills = discoverSkills(skillsRoot);

  // Determine which skills to evaluate
  let targets;
  if (args.skills.length > 0) {
    targets = resolveSkillNames(skillsRoot, args.skills);
  } else {
    targets = allSkills;
  }

  if (targets.length === 0) {
    console.error("  No skills found to evaluate.");
    process.exit(1);
  }

  const results = [];
  console.log(`  Evaluating ${targets.length} skill(s)...\n`);

  for (const skill of targets) {
    const result = scoreSkill(skill.path);
    results.push(result);

    if (!args.json) {
      const icon = result.structural.overallPassed ? "PASS" : "FAIL";
      const scoreInfo = result.existingScores?.qualityScore != null
        ? ` — Quality: ${result.existingScores.qualityScore}/100`
        : "";
      let line = `  [${icon}] ${result.category}/${result.skill}${scoreInfo}`;

      if (result.structural.errorCount > 0) {
        line += ` (${result.structural.errorCount} error(s))`;
      }
      console.log(line);

      // Show structural issues
      for (const c of result.structural.checks) {
        if (!c.passed) {
          const sev = c.severity === "error" ? "ERR" : "WRN";
          console.log(`         [${sev}] ${c.name}: ${c.message}`);
        }
      }
    }
  }

  if (args.json) {
    console.log(JSON.stringify(results, null, 2));
  } else {
    // Summary
    const passed = results.filter((r) => r.structural.overallPassed).length;
    const scored = results.filter((r) => r.existingScores?.qualityScore != null);
    console.log(`\n  Structural: ${passed}/${results.length} passed`);
    if (scored.length > 0) {
      const avg = Math.round(scored.reduce((s, r) => s + r.existingScores.qualityScore, 0) / scored.length);
      console.log(`  Avg quality: ${avg}/100 (${scored.length} with scores)`);
    }
    const unscored = results.filter((r) => r.structural.overallPassed && !r.existingScores);
    if (unscored.length > 0) {
      console.log(`  Unscored: ${unscored.length} skill(s) need LLM evaluation`);
    }
  }

  console.log();
  const hasErrors = results.some((r) => !r.structural.overallPassed);
  process.exit(hasErrors ? 1 : 0);
}

// ── Main ─────────────────────────────────────────────────────────────────────

function main() {
  const args = parseArgs(process.argv.slice(2));
  const projectRoot = process.cwd();
  const version = getPackageVersion();

  if (args.command === "version") {
    console.log(version);
    return;
  }

  if (args.command === "help" || !args.command) {
    printHelp();
    return;
  }

  console.log(`\n  eigent-skills v${version}\n`);

  const skillsRoot = getSkillsRoot();

  switch (args.command) {
    case "install": {
      if (!skillsRoot) {
        console.error("Skills directory not found. Run from the repo or install via npm.");
        process.exit(1);
      }
      const agents = resolveTargetAgents(args.agent);
      const skillFilter = args.skills.length > 0 ? args.skills : null;
      if (skillFilter) {
        console.log(`  Installing skill(s): ${skillFilter.join(", ")}`);
      }
      console.log(`  Detected agents: ${agents.map((a) => AGENTS[a].name).join(", ")}`);
      const count = installSkills(skillsRoot, agents, args.global, projectRoot, skillFilter);
      console.log(`\n  Done! Installed ${count} skill(s).`);
      console.log(`  Run 'npx @eigent-ai/agent-skills update' anytime to get the latest.\n`);
      break;
    }

    case "update": {
      const agents = resolveTargetAgents(args.agent);
      console.log(`  Checking for updates...`);
      const count = updateSkills(agents, args.global, projectRoot);
      if (count > 0) {
        console.log(`\n  Updated ${count} skill(s).`);
      } else {
        console.log(`\n  All skills are up to date.`);
      }
      console.log();
      break;
    }

    case "uninstall": {
      const agents = resolveTargetAgents(args.agent);
      const skillFilter = args.skills.length > 0 ? args.skills : null;
      if (skillFilter) {
        console.log(`  Uninstalling skill(s): ${skillFilter.join(", ")}`);
      }
      const count = uninstallSkills(agents, args.global, projectRoot, skillFilter);
      console.log(`\n  Removed ${count} skill(s).\n`);
      break;
    }

    case "list": {
      if (!skillsRoot) {
        console.error("Skills directory not found.");
        process.exit(1);
      }
      console.log("  Available Eigent Skills:");
      listSkills(skillsRoot);
      console.log();
      break;
    }

    case "status": {
      const agents = resolveTargetAgents(args.agent);
      showStatus(agents, args.global, projectRoot);
      console.log();
      break;
    }

    case "auto-update": {
      setupAutoUpdate(args.interval);
      break;
    }

    case "doctor": {
      doctor();
      console.log();
      break;
    }

    case "eval": {
      if (!skillsRoot) {
        console.error("Skills directory not found. Run from the repo.");
        process.exit(1);
      }
      runEval(skillsRoot, args);
      return;
    }

    default:
      console.error(`  Unknown command: ${args.command}`);
      printHelp();
      process.exit(1);
  }
}

main();
