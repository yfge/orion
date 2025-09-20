const englishPlugin = require('./tools/commitlint-plugin-english')

module.exports = {
  extends: ['@commitlint/config-conventional'],
  plugins: [englishPlugin],
  rules: {
    // Enforce English (ASCII) header only
    'header-english': [2, 'always'],
    // Keep conventional types; extend if needed
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'chore', 'refactor', 'test', 'build', 'ci', 'perf', 'revert'
    ]],
    // Reasonable defaults
    'subject-empty': [2, 'never'],
    'header-max-length': [2, 'always', 72],
  },
}
