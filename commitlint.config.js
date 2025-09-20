module.exports = {
  extends: ['@commitlint/config-conventional'],
  plugins: ['./tools/commitlint-plugin-english'],
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

