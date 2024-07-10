import packageJsonPlugin from 'prettier-plugin-packagejson';

/** @type {import("prettier").Config} */
const config = {
  plugins: [packageJsonPlugin],
  /**
   * With trailing commas, we have less changed lines, when adding a new entry to an existing array.
   * This is nice for version control tools like git.
   *
   * Example:
   * const myArray = [
   *   { myEntry: 1 },
   *   { myEntry: 2 },
   *   { myEntry: 3 },
   * ];
   *
   * When we remove the last entry, there is only one changed line.
   * Without trailing commas, the line of the second entry would change too,
   * since it would loose the comma at the end.
   */
  trailingComma: 'all',
  // we have wide enough screens
  printWidth: 120,
  tabWidth: 2,
  useTabs: false,
  semi: true,
  singleQuote: true,
  quoteProps: 'as-needed',
  endOfLine: 'lf',
  arrowParens: 'always',
};

export default config;
