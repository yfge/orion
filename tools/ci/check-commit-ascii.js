#!/usr/bin/env node
const { execSync } = require('node:child_process')

function readRange(fromRef, toRef) {
  const range = fromRef && toRef ? `${fromRef}..${toRef}` : 'HEAD~20..HEAD'
  const out = execSync(`git log --format=%s ${range}`, { encoding: 'utf8' })
  return out.split('\n').filter(Boolean)
}

function isAscii(str) {
  return /^[\x00-\x7F]+$/.test(str)
}

const fromRef = process.env.COMMIT_RANGE_FROM || process.argv[2]
const toRef = process.env.COMMIT_RANGE_TO || process.argv[3]
const subjects = readRange(fromRef, toRef)

let ok = true
for (const s of subjects) {
  if (!isAscii(s)) {
    console.error(`Non-ASCII commit header detected: ${s}`)
    ok = false
  }
}

if (!ok) {
  console.error('Commit headers must be English (ASCII only).')
  process.exit(1)
}
console.log(`Checked ${subjects.length} commit headers: ASCII OK`)
