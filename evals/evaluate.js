#!/usr/bin/env node

/**
 * Evaluation Context Builder
 *
 * Prepares the full context needed for Claude Code to act as LLM judge.
 * Outputs structured evaluation prompts that Claude Code reads and scores.
 *
 * Usage:
 *   node evals/evaluate.js <skill-name>              # Output eval context for one skill
 *   node evals/evaluate.js <skill-name> --save       # Read scores from stdin and save
 *   node evals/evaluate.js <skill-name> --save --force  # Save even if structural checks fail
 *
 * Workflow (run by Claude Code):
 *   1. `node evals/evaluate.js docx`  → outputs eval context
 *   2. Claude Code scores the skill using the judge prompts
 *   3. `node evals/evaluate.js docx --save` + pipe JSON → saves scores.json
 */

const fs = require("fs");
const path = require("path");
const { validateSkill } = require("./validators/structural");
const { saveScores, loadScores, buildEvalContext, getScoresPath } = require("./scorer");

// ── Skill discovery ─────────────────────────────────────────────────────────

function findSkillDir(skillName) {
  const skillsRoot = path.join(__dirname, "..", "skills");
  for (const cat of fs.readdirSync(skillsRoot, { withFileTypes: true })) {
    if (!cat.isDirectory()) continue;
    const skillDir = path.join(skillsRoot, cat.name, skillName);
    if (fs.existsSync(path.join(skillDir, "SKILL.md"))) {
      return skillDir;
    }
  }
  // Try as category/skill path
  const direct = path.join(skillsRoot, skillName);
  if (fs.existsSync(path.join(direct, "SKILL.md"))) return direct;
  // Try as absolute path
  if (path.isAbsolute(skillName) && fs.existsSync(path.join(skillName, "SKILL.md"))) return skillName;
  return null;
}

// ── Context output ──────────────────────────────────────────────────────────

function outputEvalContext(skillDir) {
  const skillsRoot = path.join(__dirname, "..", "skills");
  const structural = validateSkill(skillDir);

  // Always show structural results
  console.log("=== STRUCTURAL VALIDATION ===\n");
  const icon = structural.overallPassed ? "PASS" : "FAIL";
  console.log(`[${icon}] ${structural.category}/${structural.skill}\n`);
  for (const c of structural.checks) {
    const status = c.passed ? "OK " : c.severity === "error" ? "ERR" : "WRN";
    console.log(`  [${status}] ${c.name}: ${c.message}`);
  }

  if (!structural.overallPassed) {
    console.log(`\nStructural errors must be fixed before LLM evaluation.`);
    process.exit(1);
  }

  // Build eval context
  const ctx = buildEvalContext(skillDir, skillsRoot);
  if (!ctx) {
    console.error("Failed to build eval context");
    process.exit(1);
  }

  // Output description judge context
  console.log("\n=== DESCRIPTION JUDGE CONTEXT ===\n");
  console.log(`Skill Name: ${ctx.skill.name}`);
  console.log(`Description: ${ctx.skill.description}`);
  console.log(`\nOther Skills in Collection:`);
  for (const s of ctx.otherSkills) {
    console.log(`  - ${s.name}: ${s.description.slice(0, 120)}${s.description.length > 120 ? "..." : ""}`);
  }

  // Output content judge context
  console.log("\n=== CONTENT JUDGE CONTEXT ===\n");
  console.log(`Files in skill directory:`);
  for (const f of ctx.skill.files) {
    console.log(`  - ${f}`);
  }
  console.log(`\nSKILL.md body (${ctx.skill.body.length} chars):`);
  console.log(ctx.skill.body.slice(0, 3000));
  if (ctx.skill.body.length > 3000) {
    console.log(`\n... [truncated, ${ctx.skill.body.length - 3000} more chars]`);
  }

  // Output the judge prompts for reference
  console.log("\n=== JUDGE PROMPTS ===\n");
  console.log("Description judge: evals/judges/description-judge.md");
  console.log("Content judge: evals/judges/content-judge.md");

  // Show existing scores if any
  const existing = loadScores(skillDir);
  if (existing) {
    console.log(`\n=== EXISTING SCORES (from ${existing.evaluatedAt}) ===\n`);
    console.log(`Quality: ${existing.qualityScore}/100`);
  }

  console.log("\n=== SAVE PATH ===\n");
  console.log(getScoresPath(skillDir));
}

// ── Save mode: read judge results from stdin ────────────────────────────────

function saveFromStdin(skillDir, options = {}) {
  let input = "";
  process.stdin.setEncoding("utf-8");
  process.stdin.on("data", (chunk) => (input += chunk));
  process.stdin.on("end", () => {
    try {
      const judgeResults = JSON.parse(input);
      const scores = saveScores(skillDir, judgeResults, options);
      console.log(`Saved scores for ${scores.category}/${scores.skill}`);
      console.log(`Quality: ${scores.qualityScore}/100`);
      console.log(`Path: ${getScoresPath(skillDir)}`);
    } catch (e) {
      console.error(`Failed to save or parse judge results: ${e.message}`);
      process.exit(1);
    }
  });
}

// ── Main ────────────────────────────────────────────────────────────────────

function main() {
  const args = process.argv.slice(2);
  const saveMode = args.includes("--save");
  const forceSave = args.includes("--force");
  const skillName = args.find((a) => !a.startsWith("--"));

  if (!skillName) {
    console.error("Usage: node evaluate.js <skill-name> [--save] [--force]");
    process.exit(1);
  }

  const skillDir = findSkillDir(skillName);
  if (!skillDir) {
    console.error(`Skill not found: ${skillName}`);
    process.exit(1);
  }

  if (saveMode) {
    saveFromStdin(skillDir, { force: forceSave });
  } else {
    outputEvalContext(skillDir);
  }
}

if (require.main === module) {
  main();
}

module.exports = { findSkillDir, outputEvalContext };
