#!/usr/bin/env node

/**
 * Skill Scorer — Structural validation + score persistence
 *
 * This module handles:
 *   1. Deterministic structural validation (zero-LLM)
 *   2. Loading/saving per-skill quality scores
 *   3. Computing aggregate quality scores from judge results
 *
 * LLM judging is performed by Claude Code during PR review (not via API calls).
 * The reviewer runs `node evals/evaluate.js <skill-name>` and uses Claude Code
 * to score the skill, then saves results with --save.
 *
 * Per-skill scores are stored separately from skill source at:
 *   evals/scores/{category}/{skill}/scores.json
 *
 * This keeps skill directories clean for user downloads (no eval data included).
 * Scores are committed to the repo and fetchable via GitHub raw URLs:
 *   https://raw.githubusercontent.com/eigent-ai/agent-skills/main/evals/scores/{category}/{skill}/scores.json
 *
 * Usage:
 *   node evals/scorer.js <skill-dir>                    # Structural validation
 *   node evals/scorer.js <skill-dir> --json             # JSON output
 *   node evals/scorer.js --all                          # Validate all skills
 *   echo '<json>' | node evals/scorer.js <skill-dir> --save       # Save LLM judge results from stdin
 *   echo '<json>' | node evals/scorer.js <skill-dir> --save --force  # Save despite structural errors
 */

const fs = require("fs");
const path = require("path");
const { validateSkill, parseFrontmatter } = require("./validators/structural");

// ── Config ──────────────────────────────────────────────────────────────────

const DESCRIPTION_WEIGHT = 0.3;
const CONTENT_WEIGHT = 0.7;

// ── Score Persistence ───────────────────────────────────────────────────────

const EVALS_SCORES_ROOT = path.join(__dirname, "scores");

function getScoresPath(skillDir) {
  const skillName = path.basename(skillDir);
  const category = path.basename(path.dirname(skillDir));
  return path.join(EVALS_SCORES_ROOT, category, skillName, "scores.json");
}

function loadScores(skillDir) {
  const scoresPath = getScoresPath(skillDir);
  if (fs.existsSync(scoresPath)) {
    try {
      return JSON.parse(fs.readFileSync(scoresPath, "utf-8"));
    } catch {
      return null;
    }
  }
  return null;
}

function calculateQualityScore(descriptionJudge, contentJudge) {
  const descNorm = descriptionJudge?.normalizedScore || 0;
  const contentNorm = contentJudge?.normalizedScore || 0;
  return Math.round((descNorm * DESCRIPTION_WEIGHT + contentNorm * CONTENT_WEIGHT) * 100);
}

function saveScores(skillDir, judgeResults, options = {}) {
  const structural = validateSkill(skillDir);
  if (!structural.overallPassed && !options.force) {
    throw new Error(
      `Cannot save scores: structural validation failed for ${structural.category}/${structural.skill} ` +
        `(${structural.errorCount} error(s)). Fix SKILL.md or pass --force.`
    );
  }

  const { descriptionJudge, contentJudge, impactScore, compatibilityScore, communityScore } = judgeResults;

  const qualityScore = (descriptionJudge && contentJudge)
    ? calculateQualityScore(descriptionJudge, contentJudge)
    : null;

  // Compute aggregate if we have enough data
  let aggregateScore = null;
  if (qualityScore !== null) {
    const weights = { quality: 0.25, impact: 0.35, compatibility: 0.15, community: 0.25 };
    const available = [];
    if (qualityScore !== null) available.push({ score: qualityScore, weight: weights.quality });
    if (impactScore != null) available.push({ score: impactScore, weight: weights.impact });
    if (compatibilityScore != null) available.push({ score: compatibilityScore, weight: weights.compatibility });
    if (communityScore != null) available.push({ score: communityScore, weight: weights.community });

    const totalWeight = available.reduce((s, a) => s + a.weight, 0);
    aggregateScore = Math.round(available.reduce((s, a) => s + a.score * (a.weight / totalWeight), 0));
  }

  const scores = {
    skill: structural.skill,
    category: structural.category,
    version: "1.0.0",
    evaluatedAt: new Date().toISOString(),
    structural: {
      passed: structural.overallPassed,
      errorCount: structural.errorCount,
      warningCount: structural.warningCount,
      checks: structural.checks,
    },
    qualityScore,
    descriptionJudge: descriptionJudge || null,
    contentJudge: contentJudge || null,
    impactScore: impactScore ?? null,
    compatibilityScore: compatibilityScore ?? null,
    communityScore: communityScore ?? null,
    aggregateScore,
  };

  const scoresDir = path.dirname(getScoresPath(skillDir));
  if (!fs.existsSync(scoresDir)) fs.mkdirSync(scoresDir, { recursive: true });
  fs.writeFileSync(getScoresPath(skillDir), JSON.stringify(scores, null, 2) + "\n");

  return scores;
}

// ── Skill Context Builder ───────────────────────────────────────────────────
// Builds the context needed for Claude Code to act as LLM judge

function getAllSkillMetas(skillsRoot) {
  const metas = [];
  if (!skillsRoot || !fs.existsSync(skillsRoot)) return metas;
  for (const cat of fs.readdirSync(skillsRoot, { withFileTypes: true })) {
    if (!cat.isDirectory()) continue;
    for (const skill of fs.readdirSync(path.join(skillsRoot, cat.name), { withFileTypes: true })) {
      if (!skill.isDirectory()) continue;
      const mdPath = path.join(skillsRoot, cat.name, skill.name, "SKILL.md");
      if (fs.existsSync(mdPath)) {
        const content = fs.readFileSync(mdPath, "utf-8");
        const parsed = parseFrontmatter(content);
        if (parsed && parsed.meta) {
          metas.push({
            name: parsed.meta.name || skill.name,
            description: parsed.meta.description || "",
          });
        }
      }
    }
  }
  return metas;
}

function listSkillFiles(skillDir) {
  const files = [];
  function walk(dir, prefix) {
    if (!fs.existsSync(dir)) return;
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (entry.name === ".DS_Store") continue;
      const rel = prefix ? `${prefix}/${entry.name}` : entry.name;
      if (entry.isDirectory()) {
        walk(path.join(dir, entry.name), rel);
      } else {
        files.push(rel);
      }
    }
  }
  walk(skillDir, "");
  return files;
}

function buildEvalContext(skillDir, skillsRoot) {
  const content = fs.readFileSync(path.join(skillDir, "SKILL.md"), "utf-8");
  const parsed = parseFrontmatter(content);
  if (!parsed) return null;

  const meta = parsed.meta;
  const body = parsed.body;
  const skillFiles = listSkillFiles(skillDir);
  const allMetas = getAllSkillMetas(skillsRoot || path.join(skillDir, "..", ".."));
  const otherSkills = allMetas.filter((m) => m.name !== meta.name);

  return {
    skill: {
      name: meta.name,
      description: meta.description,
      body,
      files: skillFiles,
      dir: skillDir,
    },
    otherSkills,
  };
}

// ── Main scoring function (structural only) ─────────────────────────────────

function scoreSkill(skillDir) {
  const structural = validateSkill(skillDir);
  const existing = loadScores(skillDir);

  return {
    skill: structural.skill,
    category: structural.category,
    path: skillDir,
    structural,
    existingScores: existing,
  };
}

// ── CLI ─────────────────────────────────────────────────────────────────────

function main() {
  const args = process.argv.slice(2);
  const jsonOutput = args.includes("--json");
  const saveArg = args.includes("--save");
  const filtered = args.filter((a) => !a.startsWith("--"));

  if (filtered.length === 0 && !args.includes("--all")) {
    console.error(
      "Usage: node scorer.js <skill-dir> | --all [--json]\n" +
      "       echo '<json>' | node scorer.js <skill-dir> --save [--force]"
    );
    process.exit(1);
  }

  const forceSave = args.includes("--force");

  // ── Save mode: read judge results from stdin ──
  if (saveArg) {
    const skillDir = path.resolve(filtered[0]);
    let input = "";
    process.stdin.setEncoding("utf-8");
    process.stdin.on("data", (chunk) => (input += chunk));
    process.stdin.on("end", () => {
      let judgeResults;
      try {
        judgeResults = JSON.parse(input);
      } catch (e) {
        console.error(`Invalid JSON from stdin: ${e.message}`);
        process.exit(1);
      }
      let scores;
      try {
        scores = saveScores(skillDir, judgeResults, { force: forceSave });
      } catch (e) {
        console.error(e.message);
        process.exit(1);
      }
      if (jsonOutput) {
        console.log(JSON.stringify(scores, null, 2));
      } else {
        console.log(`  Saved scores for ${scores.category}/${scores.skill}`);
        console.log(`  Quality: ${scores.qualityScore}/100`);
        console.log(`  Path: ${getScoresPath(skillDir)}`);
      }
    });
    return;
  }

  const skillsRoot = path.join(__dirname, "..", "skills");

  // ── All skills mode ──
  if (args.includes("--all")) {
    const results = [];
    for (const cat of fs.readdirSync(skillsRoot, { withFileTypes: true })) {
      if (!cat.isDirectory()) continue;
      for (const skill of fs.readdirSync(path.join(skillsRoot, cat.name), { withFileTypes: true })) {
        if (!skill.isDirectory()) continue;
        const skillDir = path.join(skillsRoot, cat.name, skill.name);
        if (fs.existsSync(path.join(skillDir, "SKILL.md"))) {
          results.push(scoreSkill(skillDir));
        }
      }
    }

    if (jsonOutput) {
      console.log(JSON.stringify(results, null, 2));
    } else {
      for (const r of results) {
        const icon = r.structural.overallPassed ? "PASS" : "FAIL";
        const scoreInfo = r.existingScores?.qualityScore != null
          ? ` — Quality: ${r.existingScores.qualityScore}/100`
          : "";
        const issues = [];
        if (r.structural.errorCount > 0) issues.push(`${r.structural.errorCount} error(s)`);
        if (r.structural.warningCount > 0) issues.push(`${r.structural.warningCount} warning(s)`);
        console.log(`  [${icon}] ${r.category}/${r.skill}${scoreInfo}${issues.length ? " — " + issues.join(", ") : ""}`);
        for (const c of r.structural.checks) {
          if (!c.passed) {
            const sev = c.severity === "error" ? "ERR" : "WRN";
            console.log(`         [${sev}] ${c.name}: ${c.message}`);
          }
        }
      }
      const passed = results.filter((r) => r.structural.overallPassed).length;
      const scored = results.filter((r) => r.existingScores?.qualityScore != null);
      console.log(`\n  Structural: ${passed}/${results.length} passed`);
      if (scored.length > 0) {
        const avg = Math.round(scored.reduce((s, r) => s + r.existingScores.qualityScore, 0) / scored.length);
        console.log(`  Avg quality: ${avg}/100 (${scored.length} with scores)`);
      }
    }

    process.exit(results.some((r) => !r.structural.overallPassed) ? 1 : 0);
    return;
  }

  // ── Single skill mode ──
  const skillDir = path.resolve(filtered[0]);
  const result = scoreSkill(skillDir);

  if (jsonOutput) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    const icon = result.structural.overallPassed ? "PASS" : "FAIL";
    console.log(`\n  [${icon}] ${result.category}/${result.skill}`);
    for (const c of result.structural.checks) {
      const status = c.passed ? "OK " : c.severity === "error" ? "ERR" : "WRN";
      console.log(`    [${status}] ${c.name}: ${c.message}`);
    }
    if (result.existingScores) {
      const s = result.existingScores;
      console.log(`\n  Existing Quality Score: ${s.qualityScore}/100 (from ${s.evaluatedAt})`);
    } else {
      console.log(`\n  No quality scores yet. Use Claude Code to run full evaluation.`);
    }
  }

  process.exit(result.structural.overallPassed ? 0 : 1);
}

// ── Exports ─────────────────────────────────────────────────────────────────

module.exports = {
  scoreSkill,
  saveScores,
  loadScores,
  calculateQualityScore,
  buildEvalContext,
  getScoresPath,
  DESCRIPTION_WEIGHT,
  CONTENT_WEIGHT,
};

if (require.main === module) {
  main();
}
