#!/usr/bin/env node

/**
 * Structural Validator for SKILL.md files
 *
 * Performs deterministic (zero-LLM) checks on SKILL.md files.
 * Returns a structured result with errors and warnings.
 *
 * Usage:
 *   node evals/validators/structural.js <path-to-skill-dir>
 *   node evals/validators/structural.js --all
 */

const fs = require("fs");
const path = require("path");

// ── Frontmatter parsing ─────────────────────────────────────────────────────

function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;

  const meta = {};
  let currentKey = null;
  let currentValue = "";

  for (const line of match[1].split("\n")) {
    // Check for new key-value pair
    const kvMatch = line.match(/^(\w+):\s*(.*)/);
    if (kvMatch) {
      if (currentKey) {
        meta[currentKey] = currentValue.trim();
      }
      currentKey = kvMatch[1];
      currentValue = kvMatch[2];
      // Handle quoted strings that may span lines
      if (currentValue.startsWith('"') && !currentValue.endsWith('"')) {
        currentValue += "\n";
        continue;
      }
      // Strip surrounding quotes
      if (
        (currentValue.startsWith('"') && currentValue.endsWith('"')) ||
        (currentValue.startsWith("'") && currentValue.endsWith("'"))
      ) {
        currentValue = currentValue.slice(1, -1);
      }
    } else if (currentKey) {
      currentValue += line + "\n";
      if (line.trim().endsWith('"')) {
        currentValue = currentValue.trim();
        if (currentValue.startsWith('"')) {
          currentValue = currentValue.slice(1, -1);
        }
      }
    }
  }
  if (currentKey) {
    meta[currentKey] = currentValue.trim();
    if (
      (meta[currentKey].startsWith('"') && meta[currentKey].endsWith('"')) ||
      (meta[currentKey].startsWith("'") && meta[currentKey].endsWith("'"))
    ) {
      meta[currentKey] = meta[currentKey].slice(1, -1);
    }
  }

  const bodyStart = content.indexOf("---", 4);
  const body =
    bodyStart !== -1 ? content.slice(bodyStart + 3).trim() : "";

  return { meta, body, raw: match[1] };
}

// ── Individual checks ───────────────────────────────────────────────────────

function checkFrontmatterPresent(content) {
  const has = /^---\n[\s\S]*?\n---/.test(content);
  return {
    name: "frontmatter-present",
    rule: "YAML block with `name` and `description`",
    passed: has,
    severity: "error",
    message: has ? "Frontmatter found" : "Missing YAML frontmatter (--- block)",
  };
}

function checkNameField(meta) {
  const has = !!(meta && meta.name && meta.name.trim());
  return {
    name: "name-field",
    rule: "`name` field present in frontmatter",
    passed: has,
    severity: "error",
    message: has ? `name: "${meta.name}"` : "Missing `name` field in frontmatter",
  };
}

function checkDescriptionField(meta) {
  const has = !!(meta && meta.description && meta.description.trim());
  return {
    name: "description-field",
    rule: "`description` field present in frontmatter",
    passed: has,
    severity: "error",
    message: has
      ? `description present (${meta.description.length} chars)`
      : "Missing `description` field in frontmatter",
  };
}

function checkNameMatchesDirectory(meta, skillDir) {
  if (!meta || !meta.name) return null;
  const dirName = path.basename(skillDir);
  const matches = meta.name.trim().toLowerCase() === dirName.toLowerCase();
  return {
    name: "name-matches-directory",
    rule: "`name:` field matches the skill's directory name",
    passed: matches,
    severity: "error",
    message: matches
      ? `name "${meta.name}" matches directory "${dirName}"`
      : `name "${meta.name}" does not match directory "${dirName}"`,
  };
}

function checkDescriptionLength(meta) {
  if (!meta || !meta.description) return null;
  const len = meta.description.length;
  const ok = len >= 50 && len <= 500;
  return {
    name: "description-length",
    rule: "Description 50–500 characters",
    passed: ok,
    severity: "warning",
    message: ok
      ? `Description length: ${len} chars (within range)`
      : `Description length: ${len} chars (expected 50–500)`,
  };
}

function checkTriggerPhrases(meta) {
  if (!meta || !meta.description) return null;
  // Look for trigger indicators: "when", "use this", "trigger", explicit examples
  const desc = meta.description.toLowerCase();
  const triggerPatterns = [
    /\bwhen\b/,
    /\btrigger/,
    /\buse this\b/,
    /\buse when\b/,
    /\bif the user\b/,
    /\bexamples?\s*include/,
    /\bsuch as\b/,
    /\bincluding\b/,
    /\basks?\s*(to|for|about)\b/,
    /\bmentions?\b/,
  ];
  const matchCount = triggerPatterns.filter((p) => p.test(desc)).length;
  const ok = matchCount >= 2;
  return {
    name: "trigger-phrases",
    rule: "Description includes at least 2 explicit trigger phrases",
    passed: ok,
    severity: "warning",
    message: ok
      ? `Found ${matchCount} trigger patterns`
      : `Only ${matchCount} trigger pattern(s) found (expected at least 2)`,
  };
}

function checkBodyNotEmpty(body) {
  const has = !!(body && body.trim().length > 0);
  return {
    name: "body-not-empty",
    rule: "SKILL.md has content beyond frontmatter",
    passed: has,
    severity: "error",
    message: has
      ? `Body content: ${body.trim().length} chars`
      : "SKILL.md body is empty",
  };
}

function checkNoMergeConflicts(content) {
  const has = /^<{7}\s/m.test(content);
  return {
    name: "no-merge-conflicts",
    rule: "No `<<<<<<<` markers in file",
    passed: !has,
    severity: "error",
    message: has
      ? "Merge conflict markers found"
      : "No merge conflict markers",
  };
}

function stripExampleContent(text) {
  // Strip fenced code blocks
  let result = text.replace(/^```[\s\S]*?^```/gm, "");
  // Strip lines that are illustrative examples (contain "Example", "e.g.", "would be", etc.)
  result = result.replace(/^.*(?:Examples?|e\.g\.|for instance|would be helpful|could be).*$/gim, "");
  return result;
}

function checkScriptsExist(body, skillDir) {
  if (!body) return null;
  // Strip fenced code blocks to avoid matching illustrative examples
  const strippedBody = stripExampleContent(body);
  // Find references to scripts/ paths
  const scriptRefs = [];
  const patterns = [
    /scripts\/[\w\-\/]+\.[\w]+/g,
    /`scripts\/[^`]+`/g,
  ];
  for (const pattern of patterns) {
    const matches = strippedBody.match(pattern) || [];
    for (const m of matches) {
      scriptRefs.push(m.replace(/`/g, ""));
    }
  }
  // Deduplicate
  const unique = [...new Set(scriptRefs)];
  if (unique.length === 0) return null;

  const missing = unique.filter(
    (ref) => !fs.existsSync(path.join(skillDir, ref))
  );
  const ok = missing.length === 0;
  return {
    name: "scripts-exist",
    rule: "Referenced scripts/ paths actually exist",
    passed: ok,
    severity: "error",
    message: ok
      ? `All ${unique.length} script reference(s) found`
      : `Missing scripts: ${missing.join(", ")}`,
  };
}

function checkReferencesExist(body, skillDir) {
  if (!body) return null;
  // Strip fenced code blocks to avoid matching illustrative examples
  const strippedBody = stripExampleContent(body);
  const refPatterns = [
    /references\/[\w\-\/]+\.[\w]+/g,
    /`references\/[^`]+`/g,
  ];
  const refs = [];
  for (const pattern of refPatterns) {
    const matches = strippedBody.match(pattern) || [];
    for (const m of matches) {
      refs.push(m.replace(/`/g, ""));
    }
  }
  const unique = [...new Set(refs)];
  if (unique.length === 0) return null;

  const missing = unique.filter(
    (ref) => !fs.existsSync(path.join(skillDir, ref))
  );
  const ok = missing.length === 0;
  return {
    name: "references-exist",
    rule: "Referenced references/ paths actually exist",
    passed: ok,
    severity: "warning",
    message: ok
      ? `All ${unique.length} reference(s) found`
      : `Missing references: ${missing.join(", ")}`,
  };
}

// ── Main validation function ────────────────────────────────────────────────

function validateSkill(skillDir) {
  const skillMdPath = path.join(skillDir, "SKILL.md");
  if (!fs.existsSync(skillMdPath)) {
    return {
      skill: path.basename(skillDir),
      category: path.basename(path.dirname(skillDir)),
      path: skillDir,
      checks: [],
      errorCount: 1,
      warningCount: 0,
      overallPassed: false,
      error: "SKILL.md not found",
    };
  }

  const content = fs.readFileSync(skillMdPath, "utf-8");
  const parsed = parseFrontmatter(content);
  const meta = parsed ? parsed.meta : null;
  const body = parsed ? parsed.body : null;

  const checks = [
    checkFrontmatterPresent(content),
    checkNameField(meta),
    checkDescriptionField(meta),
    checkNameMatchesDirectory(meta, skillDir),
    checkDescriptionLength(meta),
    checkTriggerPhrases(meta),
    checkBodyNotEmpty(body),
    checkNoMergeConflicts(content),
    checkScriptsExist(body, skillDir),
    checkReferencesExist(body, skillDir),
  ].filter(Boolean);

  const errorCount = checks.filter((c) => !c.passed && c.severity === "error").length;
  const warningCount = checks.filter((c) => !c.passed && c.severity === "warning").length;

  return {
    skill: path.basename(skillDir),
    category: path.basename(path.dirname(skillDir)),
    path: skillDir,
    checks,
    errorCount,
    warningCount,
    overallPassed: errorCount === 0,
  };
}

// ── Exports & CLI ───────────────────────────────────────────────────────────

module.exports = { validateSkill, parseFrontmatter };

if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error("Usage: node structural.js <skill-dir> | --all");
    process.exit(1);
  }

  if (args[0] === "--all") {
    const jsonMode = args.includes("--json");
    const skillsRoot = path.join(__dirname, "..", "..", "skills");
    if (!fs.existsSync(skillsRoot)) {
      console.error("skills/ directory not found");
      process.exit(1);
    }
    const results = [];
    for (const cat of fs.readdirSync(skillsRoot, { withFileTypes: true })) {
      if (!cat.isDirectory()) continue;
      for (const skill of fs.readdirSync(path.join(skillsRoot, cat.name), { withFileTypes: true })) {
        if (!skill.isDirectory()) continue;
        const skillDir = path.join(skillsRoot, cat.name, skill.name);
        if (fs.existsSync(path.join(skillDir, "SKILL.md"))) {
          results.push(validateSkill(skillDir));
        }
      }
    }

    const totalErrors = results.reduce((n, r) => n + r.errorCount, 0);
    const totalWarnings = results.reduce((n, r) => n + r.warningCount, 0);

    if (jsonMode) {
      console.log(JSON.stringify(results, null, 2));
    } else {
      for (const r of results) {
        const icon = r.overallPassed ? "PASS" : "FAIL";
        const details = [];
        if (r.errorCount > 0) details.push(`${r.errorCount} error(s)`);
        if (r.warningCount > 0) details.push(`${r.warningCount} warning(s)`);
        console.log(`  [${icon}] ${r.category}/${r.skill}${details.length ? " — " + details.join(", ") : ""}`);
        for (const c of r.checks) {
          if (!c.passed) {
            const sev = c.severity === "error" ? "ERR" : "WRN";
            console.log(`         [${sev}] ${c.name}: ${c.message}`);
          }
        }
      }
      console.log(`\n  Total: ${results.length} skills, ${totalErrors} error(s), ${totalWarnings} warning(s)`);
      console.log(`  Passed: ${results.filter((r) => r.overallPassed).length}/${results.length}`);
    }

    process.exit(totalErrors > 0 ? 1 : 0);
  } else {
    const result = validateSkill(args[0]);
    if (args.includes("--json")) {
      console.log(JSON.stringify(result, null, 2));
    } else {
      const icon = result.overallPassed ? "PASS" : "FAIL";
      console.log(`\n  [${icon}] ${result.category}/${result.skill}`);
      for (const c of result.checks) {
        const status = c.passed ? "OK " : c.severity === "error" ? "ERR" : "WRN";
        console.log(`    [${status}] ${c.name}: ${c.message}`);
      }
      console.log(`\n  Errors: ${result.errorCount}, Warnings: ${result.warningCount}`);
    }
    process.exit(result.overallPassed ? 0 : 1);
  }
}
