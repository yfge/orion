module.exports = {
  rules: {
    'header-english': (parsed /*, when, value */) => {
      const header = parsed.header || ''
      const asciiOnly = /^[\x00-\x7F]+$/.test(header)
      return [
        asciiOnly,
        'Commit header must be English (ASCII only). Use English Conventional Commits.',
      ]
    },
  },
}

