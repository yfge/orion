#!/usr/bin/env node
const { execSync } = require('node:child_process')

function sh(cmd) { return execSync(cmd, { encoding: 'utf8' }).trim() }

function getRange(fromRef, toRef) {
  if (fromRef && toRef) return `${fromRef}..${toRef}`
  return 'HEAD~20..HEAD'
}

function listCommits(range) {
  const out = sh(`git rev-list --no-merges ${range}`)
  return out.split('\n').filter(Boolean)
}

function getCommitMessage(hash) {
  return sh(`git log -1 --pretty=%B ${hash}`)
}

function listChangedFiles(hash) {
  const out = sh(`git show --name-only --pretty=format: ${hash}`)
  return out.split('\n').map(s => s.trim()).filter(Boolean)
}

function needsAgentsChat(files) {
  // Consider “code changes” only when touching these paths
  const codeTouched = files.some(f => (
    f.startsWith('backend/') ||
    f.startsWith('frontend/') ||
    f.startsWith('Docker/') ||
    f === 'docker-compose.yml'
  ))
  if (!codeTouched) return false
  const agentsTouched = files.some(f => f.startsWith('agents_chat/'))
  return !agentsTouched
}

const fromRef = process.env.COMMIT_RANGE_FROM || process.argv[2]
const toRef = process.env.COMMIT_RANGE_TO || process.argv[3]
const range = getRange(fromRef, toRef)
const commits = listCommits(range)

let ok = true
for (const c of commits) {
  const msg = getCommitMessage(c)
  if (/skip agents-chat/i.test(msg)) continue
  const files = listChangedFiles(c)
  if (needsAgentsChat(files)) {
    console.error(`Commit ${c.slice(0,7)} modifies code without agents_chat entry.`)
    console.error(`Add an agents_chat log in the same commit or include 'skip agents-chat' in the body to bypass.`)
    console.error(`Changed files: \n  - ${files.join('\n  - ')}`)
    ok = false
  }
}

if (!ok) process.exit(1)
console.log(`Checked ${commits.length} commits for agents_chat coupling: OK`)
