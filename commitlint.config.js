module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // Keep conventional types; extend if needed
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'chore', 'refactor', 'test', 'build', 'ci', 'perf', 'revert'
    ]],
    // Reasonable defaults
    'subject-empty': [2, 'never'],
    // Allow slightly longer subjects for clarity
    'header-max-length': [2, 'always', 100],
  },
}
