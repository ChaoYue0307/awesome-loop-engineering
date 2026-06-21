#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const validate = require('../validate');

function loadSchema() {
  // Prefer the packaged schema; fall back to the repository copy when run in-tree.
  const candidates = [
    path.join(__dirname, '..', 'loop-contract.schema.json'),
    path.join(__dirname, '..', '..', '..', 'schemas', 'loop-contract.schema.json'),
  ];
  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) return JSON.parse(fs.readFileSync(candidate, 'utf8'));
  }
  throw new Error('loop-contract.schema.json not found');
}

function main() {
  const file = process.argv[2];
  if (!file) {
    process.stderr.write('Usage: loop-contract-validate <contract.json>\n');
    process.exit(2);
  }

  let data;
  try {
    data = JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (error) {
    process.stderr.write(`Could not read ${file}: ${error.message}\n`);
    process.exit(2);
  }

  const errors = validate(data, loadSchema(), '$');
  if (errors.length === 0) {
    process.stdout.write(`${file}: valid loop contract\n`);
    process.exit(0);
  }

  process.stderr.write(`${file}: invalid loop contract\n`);
  for (const error of errors) process.stderr.write(`- ${error}\n`);
  process.exit(1);
}

main();
